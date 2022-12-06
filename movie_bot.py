import time
import atexit
import getpass
import requests  # install the package via "pip install requests"
from collections import defaultdict
import threading
import queue

from movie_agent import MovieAgent
from Response.response import natural_response_msg_history, natural_response_unknown

# url of the speakeasy server
url = 'https://speakeasy.ifi.uzh.ch'
listen_freq = 3


class MovieBot:
    def __init__(self, username, password):
        movie_agent = MovieAgent()
        self.movie_agent = movie_agent
        self.agent_details = self.login(username, password)
        self.session_token = self.agent_details['sessionToken']
        self.chat_state = defaultdict(lambda: {'messages': defaultdict(dict), 'initiated': False, 'my_alias': None})
        self.history = []
        self.reactions = {}

        atexit.register(self.logout)

    def movie_chat(self):
        while True:
            # check for all chatrooms
            current_rooms = self.check_rooms(session_token=self.session_token)['rooms']
            for room in current_rooms:
                # ignore finished conversations
                if room['remainingTime'] > 0:
                    room_id = room['uid']
                    if not self.chat_state[room_id]['initiated']:
                        # send a welcome message and get the alias of the agent in the chatroom
                        self.post_message(room_id=room_id, session_token=self.session_token, message='Hi, I am a movie bot. Ask me about movies! Also I love feedback, so be sure to react to my messages (thumbs up, thumbs down, star) \U0001F600')
                        self.chat_state[room_id]['initiated'] = True
                        self.chat_state[room_id]['my_alias'] = room['alias']

                    # check for all messages
                    all_messages = self.check_room_state(room_id=room_id, since=0, session_token=self.session_token)['messages']

                    # you can also use ["reactions"] to get the reactions of the messages: STAR, THUMBS_UP, THUMBS_DOWN
                    new_reacts = self.check_room_state(room_id=room_id, since=0, session_token=self.session_token)['reactions']
                    # check whether there are new reactions
                    if room_id not in self.reactions.keys():
                        self.reactions[room_id] = []
                    if new_reacts != self.reactions[room_id]:
                        # check for all reactions
                        for react in new_reacts:
                            # check whether the reaction is new
                            if react not in self.reactions[room_id]:
                                # check whether the reaction is a thumbs up
                                if react['type'] == 'THUMBS_UP':
                                    self.post_message(room_id=room_id, session_token=self.session_token, message='Thanks for the feedback! \U0001F600\n Do you want additional information?')
                                # check whether the reaction is a thumbs down
                                elif react['type'] == 'THUMBS_DOWN':
                                    self.post_message(room_id=room_id, session_token=self.session_token, message='Thanks for the feedback! Since you seem to be an expert, could you tell me what was wrong with my answer? \U0001F600')
                                # check whether the reaction is a star
                                elif react['type'] == 'STAR':
                                    self.post_message(room_id=room_id, session_token=self.session_token, message='Thanks for the feedback! Wanna know more? \U0001F600')
                        self.reactions[room_id] = new_reacts

                    #[{'messageOrdinal': 0, 'type': 'THUMBS_DOWN'}]
                    # for reaction in reactions:
                    #     self.post_message(room_id=room_id, session_token=self.session_token, message='Got your message: \'{}\' at {}.'.format(reaction, self.get_time()))

                    for message in all_messages:
                        if message['authorAlias'] != self.chat_state[room_id]['my_alias']:

                            # check if the message is new
                            if message['ordinal'] not in self.chat_state[room_id]['messages']:
                                self.chat_state[room_id]['messages'][message['ordinal']] = message
                                print('\t- Chatroom {} - new message #{}: \'{}\' - {}'.format(room_id, message['ordinal'], message['message'], self.get_time()))

                                ##### Call agent here and get the response message #####

                                try:
                                    time_before = time.localtime()
                                    query = message['message']
                                    # print apology if it takes longer than 2 seconds to get a response
                                    time_diff = time.mktime(time.localtime()) - time.mktime(time_before)
                                    print(time_diff)
                                    if time_diff > 1.5:
                                        self.post_message(room_id=room_id, session_token=self.session_token, message='That\'s a tough one, let me think...')
                                    response, match, intent = self.multi_thread(query)
                                    # check if question was already asked and get answer from history
                                    multi = ""
                                    response = response[0].upper() + response[1:]
                                    if match is not None and intent is not None:
                                        if (match, intent, room_id, self.session_token) in self.history:
                                            multi = natural_response_msg_history()
                                            response = multi + response
                                        else: 
                                            self.history.append((match, intent, room_id, self.session_token))
                                    self.post_message(room_id=room_id, session_token=self.session_token, message=response)
                                except Exception as e:
                                    self.post_message(room_id=room_id, session_token=self.session_token, message=natural_response_unknown())
                                    print('Error: {}'.format(e)) # TODO: better exceptions
                                                           
                else:
                    # delete the history of the chatroom
                    for msg in self.history:
                        if msg[2] == room['uid']:
                            self.history.remove(msg)
            # wait for 1 second to avoid spamming the server
            time.sleep(1)
                                
                                ########################################################################


    def login(self, username: str, password: str):
        agent_details = requests.post(url=url + "/api/login", json={"username": username, "password": password}).json()
        print('- User {} successfully logged in with session \'{}\'!'.format(agent_details['userDetails']['username'], agent_details['sessionToken']))
        return agent_details

    def check_rooms(self, session_token: str):
        return requests.get(url=url + "/api/rooms", params={"session": session_token}).json()

    def check_room_state(self, room_id: str, since: int, session_token: str):
        return requests.get(url=url + "/api/room/{}/{}".format(room_id, since), params={"roomId": room_id, "since": since, "session": session_token}).json()

    def post_message(self, room_id: str, session_token: str, message: str):
        tmp_des = requests.post(url=url + "/api/room/{}".format(room_id),
                                params={"roomId": room_id, "session": session_token}, data=message.encode('utf-8')).json()
        if tmp_des['description'] != 'Message received':
            print('\t\t Error: failed to post message: {}'.format(message))

    def get_time(self):
        return time.strftime("%H:%M:%S, %d-%m-%Y", time.localtime())

    def logout(self):
        if requests.get(url=url + "/api/logout", params={"session": self.session_token}).json()['description'] == 'Logged out':
            print('- Session \'{}\' successfully logged out!'.format(self.session_token))

    def answer(self, query, queue):
        """Get the answer from the agent and put it into the queue."""
        print(f"New thread: {query}")
        response = self.movie_agent.user_wish(query)
        queue.put(response)
        print(f"Thread finished: {query}")

    def multi_thread(self, text):
        """This function is used to run the movie_chat function in a separate thread."""
        q = queue.Queue()
        try:
            t = threading.Thread(target=self.answer, args=(text, q))
            t.start()
            t.join()
            response = q.get()
            return response
        except Exception as e:
            print("Error:", e)
            return natural_response_unknown()


if __name__ == '__main__':
    username = 'noah.mamie_bot'
    #password = getpass.getpass('Password of the movie bot >>> ')
    pwd_file = open('Credentials/pass.txt', 'r')
    password = pwd_file.read().replace('\n', '')
    moviebot = MovieBot(username, password)
    moviebot.movie_chat()