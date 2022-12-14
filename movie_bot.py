import time
import atexit
import requests  # install the package via "pip install requests"
from collections import defaultdict
import threading
import queue
import json

from movie_agent import MovieAgent
from Response.response import ResponseFormatter

# url of the speakeasy server
url = 'https://speakeasy.ifi.uzh.ch'
listen_freq = 0.5  # seconds


class MovieBot:
    def __init__(self, username, password):
        movie_agent = MovieAgent()
        self.movie_agent = movie_agent
        self.agent_details = self.login(username, password)
        self.session_token = self.agent_details['sessionToken']
        self.start_time = self.agent_details['startTime']
        self.chat_state = defaultdict(lambda: {'messages': defaultdict(dict), 'responses': defaultdict(dict), 'initiated': False, 'my_alias': None, 'reaction': None})
        self.reactions = {}
        self.feedback = {}
        self.message_queue = queue.Queue()
        threading.Thread(target=self.worker, daemon=True).start()

        atexit.register(self.logout)

    def movie_chat(self):
        while True:
            # check for all chatrooms
            current_rooms = self.check_rooms(session_token=self.session_token)['rooms']
            for room in current_rooms:
                # ignore finished conversations
                if room['remainingTime'] > 0:
                    room_id = room['uid']
                    room_start_time = room['startTime']
                    if not self.chat_state[room_id]['initiated']:
                        # send a welcome message and get the alias of the agent in the chatroom
                        # only if the agent was initiated before the chatroom was created
                        if room_start_time > self.start_time:
                            start_message = 'Hi, nice to meet you! I love movie trivia, so ask me about movies! \U0001F600'
                            time.sleep(2)
                            self.post_message(room_id=room_id, session_token=self.session_token, message=start_message)
                        else:
                            self.post_message(room_id=room_id, session_token=self.session_token, message='Sorry, just had a mental breakdown. I am back now! \U0001F600')
                        self.chat_state[room_id]['initiated'] = True
                        self.chat_state[room_id]['my_alias'] = room['alias']

                    # check for all messages since the agent was started
                    all_messages = self.check_room_state(room_id=room_id, since=self.start_time, session_token=self.session_token)['messages']
                    # check for all reactions since the agent was started
                    new_reacts = self.check_room_state(room_id=room_id, since=self.start_time, session_token=self.session_token)['reactions']
                    # check whether there are new reactions
                    if room_id not in self.reactions.keys():
                        self.reactions[room_id] = []
                    if new_reacts != self.reactions[room_id]:
                        # check for all reactions
                        for react in new_reacts:
                            # check whether the reaction is new
                            if react not in self.reactions[room_id] and react['messageOrdinal'] in self.chat_state[room_id]['responses'].keys():
                                # check whether the reaction is a thumbs up
                                if react['type'] == 'THUMBS_UP':
                                    self.post_message(room_id=room_id, session_token=self.session_token, message=ResponseFormatter.natural_response_feedback_thumbs_star(self=ResponseFormatter))
                                    self.chat_state[room_id]['reaction'] = 'THUMBS_UP'
                                # check whether the reaction is a thumbs down
                                elif react['type'] == 'THUMBS_DOWN':
                                    self.post_message(room_id=room_id, session_token=self.session_token, message=ResponseFormatter.natural_response_feedback_thumbs_down(self=ResponseFormatter))
                                    self.chat_state[room_id]['reaction'] = 'THUMBS_DOWN'
                                # check whether the reaction is a star
                                elif react['type'] == 'STAR':
                                    self.post_message(room_id=room_id, session_token=self.session_token, message=ResponseFormatter.natural_response_feedback_thumbs_star(self=ResponseFormatter))
                                    self.chat_state[room_id]['reaction'] = 'STAR'
                        self.reactions[room_id] = new_reacts
                    
                    for message in all_messages:
                        if message['authorAlias'] != self.chat_state[room_id]['my_alias']:

                            # check if the message is new
                            if message['ordinal'] not in self.chat_state[room_id]['messages'] and message['timeStamp'] > self.start_time:
                                self.chat_state[room_id]['messages'][message['ordinal']] = message
                                print('\t- Chatroom {} - new message #{}: \'{}\' - {}'.format(room_id, message['ordinal'], message['message'], self.get_time()))

                                ##### Call agent here and get the response message #####

                                try:
                                    # post reaction to user feedback
                                    if self.chat_state[room_id]['reaction'] != None:
                                        self.post_reaction(room_id=room_id, session_token=self.session_token, message_ordinal=react['messageOrdinal'] + 2, reaction_type='THUMBS_UP')
                                        if self.chat_state[room_id]['reaction'] == 'THUMBS_UP' or self.chat_state[room_id]['reaction'] == 'STAR':
                                            self.post_message(room_id=room_id, session_token=self.session_token, message=ResponseFormatter.natural_response_feedback_pos(self=ResponseFormatter))
                                        else:
                                            self.post_message(room_id=room_id, session_token=self.session_token, message=ResponseFormatter.natural_response_feedback_neg(self=ResponseFormatter))
                                        if message["authorAlias"] not in self.feedback.keys():
                                            self.feedback[message["authorAlias"]] = []
                                        self.feedback[message["authorAlias"]].append((self.chat_state[room_id]['reaction'], message['message']))
                                        self.chat_state[room_id]['reaction'] = None
                                    else:
                                        # post the response message from the agent
                                        self.agent_response(message, room_id)
                                except Exception as e:
                                    print(e)
                                    self.post_message(room_id=room_id, session_token=self.session_token, message=ResponseFormatter.natural_response_unknown(self=ResponseFormatter))
                                                           
                else:
                    # room id
                    room_id = room['uid']
                    # delete the responses history of the chatroom
                    self.chat_state[room_id]['responses'] = {}
            # wait for a bit to avoid spamming the server
            time.sleep(listen_freq)
                                
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

    def post_reaction(self, room_id: str, session_token: str, message_ordinal: int, reaction_type: str):
        tmp_des = requests.post(url=url + "/api/room/{}/reaction".format(room_id),
                                params={"roomId": room_id, "session": session_token}, json={"messageOrdinal": message_ordinal, "type": reaction_type}).json()
        if tmp_des['description'] != 'Message received':
            print('\t\t Error: failed to post reaction: {}'.format(reaction_type))

    def get_time(self):
        return time.strftime("%H:%M:%S, %d-%m-%Y", time.localtime())

    def logout(self):
        if requests.get(url=url + "/api/logout", params={"session": self.session_token}).json()['description'] == 'Logged out':
            print('- Session \'{}\' successfully logged out!'.format(self.session_token))
            # when logout save the reactions
            print(self.feedback)
            with open('data/feedback/feedback_' + f'{self.get_time()}' + '.json', 'w') as f:
                json.dump(self.feedback, f)

    def agent_response(self, message, room_id):
        """This function is used to post the agent response to Speakeasy."""
        try:
            # print start message
            t = self.multi_thread(message, room_id)
            print(t)
            if not t:
                return
        except Exception as e:
            self.post_message(room_id=room_id, session_token=self.session_token, message=ResponseFormatter.natural_response_unknown(self=ResponseFormatter))
            print('Error: {}'.format(e))

    def answer(self, message, queue, room_id):
        """Get the answer from the agent and put it into the queue."""
        try:
            query = message['message']
            ordinal = message['ordinal']
            print(f"New thread: {query}")
            response = self.movie_agent.user_wish(query)
            msg, match, intent, quest = response
            response = (msg, match, intent, quest, room_id, ordinal)
            queue.put(response)
            print(f"Thread finished: {query}")
            print(queue)
            print(threading.active_count())
        except Exception as e:
            print("Error:", e)
            return ResponseFormatter.natural_response_unknown(self=ResponseFormatter)

    def multi_thread(self, text, room_id):
        """This function is used to run the movie_chat function in a separate thread."""
        #q = queue.Queue()
        try:
            t = threading.Thread(target=self.answer, args=(text, self.message_queue, room_id), daemon=True)
            t.start()
        except Exception as e:
            print("Error:", e)
            return ResponseFormatter.natural_response_unknown(self=ResponseFormatter)

    def worker(self):
        while True:
            try:
                item = self.message_queue.get()
                print(f'Working on {item}')
                print(f'Finished {item}')
                response, match, intent, quest, room_id, msg_ordinal = item
                print("Response:", response)
                # check if question was already asked and get answer from history
                multi = ""
                # check if question was asked before
                if match is not None and intent is not None:
                    if (match, intent, room_id, self.session_token) in self.chat_state[room_id]['responses'].values():
                        multi = ResponseFormatter.natural_response_msg_history(self=ResponseFormatter)
                        response = multi + response
                # store new response
                if msg_ordinal + 1 not in self.chat_state[room_id]['responses']:
                    self.chat_state[room_id]['responses'][msg_ordinal + 1] = (match, intent, room_id, self.session_token)
                self.post_message(room_id=room_id, session_token=self.session_token, message=response)
                self.message_queue.task_done()
            except Exception as e:
                print("Error:", e)
                self.post_message(room_id=room_id, session_token=self.session_token, message=ResponseFormatter.natural_response_unknown(self=ResponseFormatter))
                self.message_queue.task_done()


if __name__ == '__main__':
    username = 'noah.mamie_bot'
    pwd_file = open('Credentials/pass.txt', 'r')
    password = pwd_file.read().replace('\n', '')
    moviebot = MovieBot(username, password)
    # connection loop to Speakeasy
    while True:
        try:    
            moviebot.movie_chat()
        except Exception as e:
            print('Error: {}'.format(e))
        except KeyboardInterrupt:
            print("Keyboard interrupt")
            # end loop
            break