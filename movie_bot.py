import time
import atexit
import getpass
import requests  # install the package via "pip install requests"
from collections import defaultdict
import threading
import queue
import json

from movie_agent import MovieAgent
from Response.response import ResponseFormatter

# url of the speakeasy server
url = 'https://speakeasy.ifi.uzh.ch'
listen_freq = 0.2  # seconds


class MovieBot:
    def __init__(self, username, password):
        movie_agent = MovieAgent()
        self.movie_agent = movie_agent
        self.agent_details = self.login(username, password)
        self.session_token = self.agent_details['sessionToken']
        self.chat_state = defaultdict(lambda: {'messages': defaultdict(dict), 'responses': defaultdict(dict), 'initiated': False, 'my_alias': None})
        #self.history = []
        self.reactions = {}
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
                                    self.post_message(room_id=room_id, session_token=self.session_token, message='Thanks for the feedback! \U0001F600')
                                    #get message that was reacted to
                                    #message = self.chat_state[room_id]['responses'][react['messageOrdinal']] # TODO: messages or responses?
                                    # print(message)
                                    # # post the response message from the agent
                                    # self.agent_response(message, room_id, True)
                                # check whether the reaction is a thumbs down
                                elif react['type'] == 'THUMBS_DOWN':
                                    self.post_message(room_id=room_id, session_token=self.session_token, message='Thanks for the feedback! Since you seem to be an expert, could you tell me what was wrong with my answer? \U0001F600')
                                # check whether the reaction is a star
                                elif react['type'] == 'STAR':
                                    self.post_message(room_id=room_id, session_token=self.session_token, message='Thanks for the feedback! \U0001F600')
                                    # # get message that was reacted to
                                    # message = self.chat_state[room_id]['responses'][react['messageOrdinal']] # TODO: messages or responses?
                                    # print(message)
                                    # # post the response message from the agent
                                    # self.agent_response(message, room_id, True)
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
                                    # post the response message from the agent
                                    self.agent_response(message, room_id)
                                except Exception as e:
                                    print(e)
                                    self.post_message(room_id=room_id, session_token=self.session_token, message=ResponseFormatter.natural_response_unknown(self=ResponseFormatter))
                        # else:
                        #     # check if the message is new
                        #     if message['ordinal'] not in self.chat_state[room_id]['responses']:
                        #         self.chat_state[room_id]['responses'][message['ordinal']] = message
                                                           
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

    def get_time(self):
        return time.strftime("%H:%M:%S, %d-%m-%Y", time.localtime())

    def logout(self):
        if requests.get(url=url + "/api/logout", params={"session": self.session_token}).json()['description'] == 'Logged out':
            print('- Session \'{}\' successfully logged out!'.format(self.session_token))
            # when logout save the reactions
            print(self.reactions)
            with open('data/reactions/reactions_' + f'{self.get_time()}' + '.json', 'w') as f:
                json.dump(self.reactions, f)

    def agent_response(self, message, room_id, insights=False):
        """This function is used to post the agent response to Speakeasy."""
        try:
            #query = message['message']
            # print start message
            self.post_message(room_id=room_id, session_token=self.session_token, message='Thinking...') #TODO: how to implement?
            t = self.multi_thread(message, insights, room_id)
            print(t)
            if not t:
                return
            # response, match, intent = t
            # print(response)
            # # check if question was already asked and get answer from history
            # multi = ""
            # response = response[0].upper() + response[1:]
            # if match is not None and intent is not None:
            #     if (match, intent, room_id, self.session_token) in self.history:
            #         multi = natural_response_msg_history()
            #         response = multi + response
            #     else: 
            #         self.history.append((match, intent, room_id, self.session_token))
            # self.post_message(room_id=room_id, session_token=self.session_token, message=response)
        except Exception as e:
            self.post_message(room_id=room_id, session_token=self.session_token, message=ResponseFormatter.natural_response_unknown(self=ResponseFormatter))
            print('Error: {}'.format(e)) # TODO: better exceptions

    def answer(self, message, queue, insights, room_id):
        """Get the answer from the agent and put it into the queue."""
        try:
            query = message['message']
            ordinal = message['ordinal']
            print(f"New thread: {query}")
            if insights:
                response = self.movie_agent.user_insights(query)
            else: response = self.movie_agent.user_wish(query)
            a, b, c = response
            response = (a, b, c, room_id, ordinal)
            queue.put(response)
            print(f"Thread finished: {query}")
            print(queue)
            print(threading.active_count())
        except Exception as e:
            print("Error:", e)
            return ResponseFormatter.natural_response_unknown(self=ResponseFormatter)

    def multi_thread(self, text, insights, room_id):
        """This function is used to run the movie_chat function in a separate thread."""
        #q = queue.Queue()
        try:
            t = threading.Thread(target=self.answer, args=(text, self.message_queue, insights, room_id), daemon=True)
            t.start()
            #t.join()
            #response = q.get(block=False)
            #return response
        # except queue.Empty:
        #     print("Error: queue is empty")
        #     return
        except Exception as e:
            print("Error:", e)
            return ResponseFormatter.natural_response_unknown(self=ResponseFormatter)

    def worker(self):
        while True:
            try:
                item = self.message_queue.get()
                print(f'Working on {item}')
                print(f'Finished {item}')
                response, match, intent, room_id, msg_ordinal = item
                print("Response:", response)
                # check if question was already asked and get answer from history
                multi = ""
                response = response[0].upper() + response[1:]
                # check if question was asked before
                if match is not None and intent is not None:
                    if (match, intent, room_id, self.session_token) in self.chat_state[room_id]['responses'].values():
                        multi = ResponseFormatter.natural_response_msg_history(self=ResponseFormatter)
                        response = multi + response
                # store new response
                if msg_ordinal + 1 not in self.chat_state[room_id]['responses']:
                    self.chat_state[room_id]['responses'][msg_ordinal + 1] = (match, intent, room_id, self.session_token)
                # if match is not None and intent is not None:
                #     if (match, intent, room_id, self.session_token) in self.history:
                #         multi = ResponseFormatter.natural_response_msg_history()
                #         response = multi + response
                #     else: 
                #         self.history.append((match, intent, room_id, self.session_token))
                self.post_message(room_id=room_id, session_token=self.session_token, message=response)
                self.message_queue.task_done()
            except Exception as e:
                print("Error:", e)
                return ResponseFormatter.natural_response_unknown(self=ResponseFormatter)


if __name__ == '__main__':
    username = 'noah.mamie_bot'
    #password = getpass.getpass('Password of the movie bot >>> ')
    pwd_file = open('Credentials/pass.txt', 'r')
    password = pwd_file.read().replace('\n', '')
    moviebot = MovieBot(username, password)
    moviebot.movie_chat()