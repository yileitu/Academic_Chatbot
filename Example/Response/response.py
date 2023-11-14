# responsed for different types of requests
import random

class ResponseFormatter:

    def __init__(self, ent2lbl, lbl2ent, rel2lbl, lbl2rel, WD, WDT):
        self.ent2lbl = ent2lbl
        self.lbl2ent = lbl2ent
        self.rel2lbl = rel2lbl
        self.lbl2rel = lbl2rel
        self.WD = WD
        self.WDT = WDT

    def natural_response_factual(self, results, check, truth):
        """Returns a natural language string response to a factual question."""
        # several options for natural language responses
        if type(results[2]) == list:
            # format list elements to string with commas
            conc = ", ".join([str(member) for member in results[2][:-1]]) + " and " + str(results[2][-1])
            results = results[0], results[1], conc
            responses = [
                f"The cast members of {results[1]} are {results[2]}.",
                f"The cast members are {results[2]}.",
                f"{results[2]} are the cast members of {results[1]}.",
                f"{results[2]} are the cast members.",
                f"{results[2]} is the correct answer.",
                f"{results[2]} is the right answer.",
                f"That would be {results[2]}."  
            ]
        else:
            if check:
                if truth:
                    responses = [
                        f"That is correct.",
                        f"Your are right.",
                        f"Correct.",
                        f"You seem to know your facts, that is indeed correct.",
                        f"Well, that is correct.",
                        f"Hmm, that is right.",
                        f"You are completely right."   
                    ]
                else:
                    results = results[0], results[1], f"{results[2]} (wd:{self.lbl2ent[results[2]].split('/')[-1]})"
                    responses = [
                            f"That is wrong. It is actually {results[2]}.",
                            f"Your are wrong. The correct answer is {results[2]}.",
                            f"Incorrect. It is actually {results[2]}.",
                            f"Well, that's wrong actually. It is {results[2]}.",
                            f"Well, that is incorrect. The correct answer is {results[2]}.",
                            f"Hmm, that doesn't seem to be right. Correct would be {results[2]}.",
                            f"You seem to be wrong there. That would be {results[2]}."   
                        ]
            else:
                try:
                    results = results[0], results[1], f"{results[2]} (wd:{self.lbl2ent[results[2]].split('/')[-1]})"
                except Exception as e:
                    print(e)
                responses = [
                    f"The {results[0]} of {results[1]} is {results[2]}.",
                    f"The answer is {results[2]}.",
                    f"{results[2]} is the {results[0]} of {results[1]}.",
                    f"{results[2]} is the answer.",
                    f"{results[2]} is the correct answer.",
                    f"{results[2]} is the right answer.",
                    f"That would be {results[2]}."   
                ]
        response = random.choice(responses)
        return response[0].upper() + response[1:]

    def natural_response_crowd(self, results, check, truth):
        """Returns a natural language string response to a crowd question."""
        # several options for natural language responses
        if type(results[2]) == list:
            # format list elements to string with commas
            conc = ", ".join([str(member) for member in results[2][:-1]]) + " and " + str(results[2][-1])
            results = results[0], results[1], conc
            responses = [
            f"With an inter-rate agreement of {results[0]} in this batch and a support of {results[1]} out of 3 votes, the cast members are {results[2]}.",
            f"The cast members are {results[2]} with an inter-rate agreement of {results[0]} in this batch and a support of {results[1]} out of 3 votes.",
            f"{results[2]} are the cast members, with an inter-rate agreement of {results[0]} in this batch and a support of {results[1]} out of 3 votes.",
            f"{results[2]} is the correct answer with an inter-rate agreement of {results[0]} in this batch and a support of {results[1]} out of 3 votes.",
            f"The crowd, with an inter-rate agreement of {results[0]} in this batch and a support of {results[1]} out of 3 votes, thinks the cast members are {results[2]}.",
            f"The cast members are {results[2]}, according to the crowd with an inter-rate agreement of {results[0]} in this batch and a support of {results[1]} out of 3 votes."
        ]
        else:
            if check:
                if truth:
                    responses = [
                        f"That is correct, according to the crowd with an inter-rate agreement of {results[0]} in this particular batch and a support of {results[1]} out of 3 votes.",
                        f"You are right, according to the crowd with an inter-rate agreement of {results[0]} in this batch and a support of {results[1]} out of 3 votes.",
                        f"Well that is correct, with an inter-rate agreement of {results[0]} in this batch of the crowd and a support of {results[1]} out of 3 votes.",
                        f"Correct, according to the crowd with an inter-rate agreement of {results[0]} in this batch and a support of {results[1]} out of 3 votes.",
                        f"The crowd, with an inter-rate agreement of {results[0]} in this batch and a support of {results[1]} out of 3 votes agrees with you.",
                        f"You're good, the crowd with an inter-rate agreement of {results[0]} in this batch and a support of {results[1]} out of 3 votes agrees."
                    ]
                else:
                    responses = [
                        f"That is wrong, according to the crowd with an inter-rate agreement of {results[0]} in this particular batch and a support of {results[1]} out of 3 votes. The correct answer is {results[2]}.",
                        f"You are incorrect, according to the crowd with an inter-rate agreement of {results[0]} in this batch and a support of {results[1]} out of 3 votes. It is actually {results[2]}.",
                        f"Well that is wrong, with an inter-rate agreement of {results[0]} in this batch of the crowd and a support of {results[1]} out of 3 votes. The answer is {results[2]}.",
                        f"False, according to the crowd with an inter-rate agreement of {results[0]} in this batch and a support of {results[1]} out of 3 votes. Correct would be {results[2]}.",
                        f"The crowd, with an inter-rate agreement of {results[0]} in this batch and a support of {results[1]} out of 3 votes disagrees with you. The correct answer is {results[2]}.",
                        f"This is incorrect, according to the crowd with an inter-rate agreement of {results[0]} in this batch and a support of {results[1]} out of 3 votes. In reality, it is {results[2]}."
                    ]
            else:
                try:
                    results = results[0], results[1], f"{results[2]} (wd:{self.lbl2ent[results[2]].split('/')[-1]})"
                except Exception as e:
                    print(e)
                responses = [
                    f"With an inter-rate agreement of {results[0]} in this batch and a support of {results[1]} out of 3 votes, the answer is {results[2]}.",
                    f"The answer is {results[2]} with an inter-rate agreement of {results[0]} in this batch and a support of {results[1]} out of 3 votes.",
                    f"{results[2]} is the answer, with an inter-rate agreement of {results[0]} in this batch and a support of {results[1]} out of 3 votes.",
                    f"{results[2]} is the correct answer with an inter-rate agreement of {results[0]} in this batch and a support of {results[1]} out of 3 votes.",
                    f"The crowd, with an inter-rate agreement of {results[0]} in this batch and a support of {results[1]} out of 3 votes, thinks the answer is {results[2]}.",
                    f"It is {results[2]}, according to the crowd with an inter-rate agreement of {results[0]} in this batch and a support of {results[1]} out of 3 votes."
                ]
        response = random.choice(responses)
        return response[0].upper() + response[1:]

    def natural_response_embedding_one(self, results):
        """Returns a natural language string response to an embedding question."""
        # several options for natural language responses
        try:
            results = f"{results} (wd:{self.lbl2ent[results].split('/')[-1]})"
        except Exception as e:
            print(e)
        responses = [
            f"I feel that the answer could also be {results}.",
            f"I think it might also be {results}.",
            f"I would say {results} might also be a correct answer.",
            f"I would guess it might actually be {results}.",
            f"in my opinion, the answer could also be {results}.",
            f"my gut feeling tells me it might also be {results}."
        ]
        response = random.choice(responses)
        return response[0].upper() + response[1:]

    def natural_response_embedding_several(self, results):
        """Returns a natural language string response (several) to an embedding question."""
        # several options for natural language responses
        try:
            results = results[0], results[1], f"{results[2]} (wd:{self.lbl2ent[results[2]].split('/')[-1]})", f"{results[3]} (wd:{self.lbl2ent[results[3]].split('/')[-1]})", f"{results[4]} (wd:{self.lbl2ent[results[4]].split('/')[-1]})"
        except Exception as e:
            print(e)
        responses = [
            f"The {results[0]} of {results[1]} is most likely {results[2]}, {results[3]} or {results[4]}.",
            f"The answer is most likely {results[2]}, {results[3]} or {results[4]}.",
            f"{results[2]}, {results[3]} or {results[4]} are most likely to be the {results[0]} of {results[1]}.",
            f"{results[2]}, {results[3]} or {results[4]} are most likely to be the answer.",
            f"{results[2]}, {results[3]} or {results[4]} are most likely to be the correct answer.",
            f"Gosh, I'm not sure. I would say it is most likely {results[2]}, {results[3]} or {results[4]}.",
            f"I'm not sure. I would say it is most likely {results[2]}, {results[3]} or {results[4]}.",
            f"Good question. I would say the {results[0]} of {results[1]} is most likely {results[2]}, {results[3]} or {results[4]}.",
            f"That's a tough one. I would say the {results[0]} of {results[1]} is probably {results[2]}, {results[3]} or {results[4]}."
        ]
        response = random.choice(responses)
        return response[0].upper() + response[1:]

    def natural_response_embedding_recommender(self, results):
        """Returns a natural language string response to recommend embedding answers."""
        # several options for natural language responses
        try:
            results = f"{results[0]} (wd:{self.lbl2ent[results[0]].split('/')[-1]})", f"{results[1]} (wd:{self.lbl2ent[results[1]].split('/')[-1]})", f"{results[2]} (wd:{self.lbl2ent[results[2]].split('/')[-1]})"
        except Exception as e:
            print(e)
        responses = [
            f"Similar movies are {results[0]}, {results[1]} or {results[2]}.",
            f"Based on your preferences, I would recommend you to watch {results[0]}, {results[1]} or {results[2]}.",
            f"You should watch {results[0]}, {results[1]} or {results[2]}.",
            f"I would recommend you to watch {results[0]}, {results[1]} or {results[2]}.",
            f"Your next movies should be {results[0]}, {results[1]} or {results[2]}.",
            f"Definitely consider watching {results[0]}, {results[1]} or {results[2]}.",
            f"A good choice would be {results[0]}, {results[1]} or {results[2]}."
        ]
        response = random.choice(responses)
        return response[0].upper() + response[1:]


    def natural_response_recommender(self, results):
        """Returns a natural language string response to recommend movies."""
        # several options for natural language responses
        try:
            results = f"{results[0]} (wd:{self.lbl2ent[results[0]].split('/')[-1]})", f"{results[1]} (wd:{self.lbl2ent[results[1]].split('/')[-1]})", f"{results[2]} (wd:{self.lbl2ent[results[2]].split('/')[-1]})", results[3], f"{results[4]} (wd:{self.lbl2ent[results[4]].split('/')[-1]})", results[5]
        except Exception as e:
            print(e)
        responses = [
            f"Similar movies are {results[0]}, {results[1]} or {results[2]}. Based on the ratings of {results[3]} IMDb users I would recommend you to watch {results[4]} with an overall rating of {results[5]}.",
            f"I would say it should be {results[0]}, {results[1]} or {results[2]}. Based on the ratings of {results[3]} IMDb users I would recommend you to watch {results[4]} with an overall rating of {results[5]}.",
            f"Based on the ratings of {results[3]} IMDb users I would recommend you to watch {results[4]} with an overall rating of {results[5]}.",
            f"Seeing that {results[3]} IMDb users rated {results[4]} with an overall rating of {results[5]}, I would recommend you to watch {results[4]}.",
            f"You will probably like {results[0]}, {results[1]} or {results[2]}. Based on the ratings of {results[3]} IMDb users your top pick is {results[4]} with an overall rating of {results[5]}.",
            f"You have good taste. Based on the ratings of {results[3]} IMDb users I would recommend you to watch {results[4]} with an overall rating of {results[5]}.",
            f"Nice, you definitely know your movies. Based on the ratings of {results[3]} IMDb users I would recommend you to watch {results[4]} with an overall rating of {results[5]}."
        ]
        response = random.choice(responses)
        return response[0].upper() + response[1:]

    def natural_response_recommender_multi(self, results):
        """Returns a natural language string response to recommend movies for multiple user preferences."""
        # several options for natural language responses
        try:
            results = f"{results[0]} (wd:{self.lbl2ent[results[0]].split('/')[-1]})", f"{results[1]} (wd:{self.lbl2ent[results[1]].split('/')[-1]})", f"{results[2]} (wd:{self.lbl2ent[results[2]].split('/')[-1]})", results[3], f"{results[4]} (wd:{self.lbl2ent[results[4]].split('/')[-1]})", results[5]
        except Exception as e:
            print(e)
        responses = [
            f"I had to think about that one for a bit. Similar movies are {results[0]}, {results[1]} or {results[2]}. Based on the ratings of {results[3]} IMDb users I would recommend you to watch {results[4]} with an overall rating of {results[5]}.",
            f"Mmmh, difficult to say but I think you might like {results[0]}, {results[1]} or {results[2]}. Based on the ratings of {results[3]} IMDb users I would recommend you to watch {results[4]} with an overall rating of {results[5]}.",
            f"That's not an easy one. Based on the ratings of {results[3]} IMDb users I would recommend you to watch {results[4]} with an overall rating of {results[5]}.",
            f"Sorry to keep you waiting. Seeing that {results[3]} IMDb users rated {results[4]} with an overall rating of {results[5]}, I would recommend you to watch {results[4]}.",
            f"Damn you're challenging me quite a bit. You will probably like {results[0]}, {results[1]} or {results[2]}. Based on the ratings of {results[3]} IMDb users your top pick is {results[4]} with an overall rating of {results[5]}.",
            f"You have good taste. Based on the ratings of {results[3]} IMDb users I would recommend you to watch {results[4]} with an overall rating of {results[5]}.",
            f"Nice, you definitely know your movies. Based on the ratings of {results[3]} IMDb users I would recommend you to watch {results[4]} with an overall rating of {results[5]}."
        ]
        response = random.choice(responses)
        return response[0].upper() + response[1:]

    def natural_response_multimedia(self, results, media):
        """Returns a natural language string response to show pictures."""
        # several options for natural language responses
        try:
            if media == "both":
                actor_string, movie_string, image_url = results
                responses = [
                    f"This took a while. But look, I found an image of {actor_string} in {movie_string} \U0001F600 image:{image_url}",
                    f"Nice, I found a great shot of {actor_string} in {movie_string} \U0001F600 image:{image_url}",
                    f"Great, I found the image of {actor_string} in {movie_string} you were seeking \U0001F600 image:{image_url}",
                    f"Well, the effort paid of and I found this image of {actor_string} in {movie_string} \U0001F600 image:{image_url}",
                ]
            elif media == "actor":
                actor_string, image_url = results
                responses = [
                    f"Look, I found an image of {actor_string} \U0001F600 image:{image_url}",
                    f"Nice, I found a great shot of {actor_string} \U0001F600 image:{image_url}",
                    f"Great, I found the image of {actor_string} you were seeking \U0001F600 image:{image_url}",
                    f"Well, I found this image of {actor_string} \U0001F600 image:{image_url}"
                ]
            elif media == "movie":
                movie_string, image_url = results
                responses = [
                    f"Look, I found an image of {movie_string} \U0001F600 image:{image_url}",
                    f"Nice, I found a great shot of {movie_string} \U0001F600 image:{image_url}",
                    f"Great, I found the image of {movie_string} you were seeking \U0001F600 image:{image_url}",
                    f"Well, I found this image of {movie_string} \U0001F600 image:{image_url}"
                ]
            else:
                image_url = results
                responses = [
                    f"Look, I found the image you were looking for \U0001F600 image:{image_url}",
                    f"Nice, I found a great shot \U0001F600 image:{image_url}",
                    f"Great, I found an image you were seeking \U0001F600 image:{image_url}",
                    f"Well, this one was in the very back of my camera roll \U0001F600 image:{image_url}"
                ]
            response = random.choice(responses)
            return response[0].upper() + response[1:]
        except Exception as e:
            print(e)
            return "Sorry, I couldn't find any images."


    def natural_response_negative(self):
        """Returns a natural language string response to 
        a question where the answer is not known."""
        # several options for natural language responses
        responses = [
            "I'm sorry, I don't know the answer to that.",
            "I don't know the answer to that.",
            "I'm afraid I don't know the answer to that.",
            "Really sorry, I don't know the answer to that.",
            "I don't know the answer to that. I'm sorry.",
            "Wow that's a tough one. I don't know the answer to that.",
            "You're asking me a tough one. I don't know the answer to that.",
            "You seem to be an expert. Even my knowledge is not sufficient to answer this question.",
            "Sorry, I have no clue..."
        ]
        response = random.choice(responses)
        return response[0].upper() + response[1:]

    def natural_response_unknown(self):
        """Returns a natural language string response to 
        a misunderstood question."""
        # several options for natural language responses
        responses = [
            "Could you rephrase that?",
            "I'm sorry, I don't understand. What do you mean?",
            "I don't understand. Could you repeat that?",
            "I'm afraid I don't understand. Please rephrase that.",
            "I'm sorry, I don't know. What exactly are you referring to?",
            "Maybe I am misunderstanding you. Could you rephrase that?"          
        ]
        response = random.choice(responses)
        return response[0].upper() + response[1:]

    def natural_response_unknown_fact(self):
        """Returns a natural language string response to 
        a misunderstood question (factual)."""
        # several options for natural language responses
        responses = [
            "Hmm, in case you have an answer in mind I can check if it is true.",
            "Sorry, not sure I understand. Should you already have a guess, I can check if it is true :)",
            "Could you repeat that? Or even better, do you have a guess? I can check if it is true :)",
            "I'm afraid I don't understand. Maybe a guess would help to kickstart my memory to check if it is true :)",
            "What exactly are you referring to? Maybe you already have a guess I could confirm?"        
        ]
        response = random.choice(responses)
        return response[0].upper() + response[1:]

    def natural_response_no_picture(self):
        """Returns a natural language string response to 
        a misunderstood question or where the answer is not known (pictures)."""
        # several options for natural language responses
        responses = [
            "I'm sorry, I didn't manage to find a picture.",
            "Uups, it seems that this picture is missing.",
            "Someone burned all their pictures.",
            "They never took a picture.",
            "Damn, someone seems to be not very photogenic."
        ]
        response = random.choice(responses)
        return response[0].upper() + response[1:]

    def natural_response_msg_history(self):
        """Returns a natural language string response to 
        a question that is in the message history of the chatbot."""
        # several options for natural language responses
        responses = [
            "Well, you already asked me that \U0001F609\n",
            "I already told you that \U0001F609\n",
            "Sure, I'll gladly remind you again \U0001F609\n",
            "No worries, I'm happy to remind you again \U0001F609\n",
            "I have all the time in the world to tell you again \U0001F609\n"
        ]
        response = random.choice(responses)
        return response[0].upper() + response[1:]

    def natural_response_feedback_thumbs_star(self):
        """Returns a natural language string response to 
        a thumbs up or star reaction to get feedback."""
        # several options for natural language responses
        responses = [
            "Thanks for the feedback! What has made this answer so special? \U0001F600",
            "Thanks for the feedback! What specifically did you like from my response? \U0001F600",
            "Thanks a lot, I'm happy to hear that! What sparked your curiosity from this response? \U0001F600",
            "Great to hear that! What did you like from my response? \U0001F600",
            "Thanks a lot, I'm happy to hear that! What has made this answer so special? \U0001F600"
        ]
        response = random.choice(responses)
        return response[0].upper() + response[1:]

    def natural_response_feedback_thumbs_down(self):
        """Returns a natural language string response to 
        a negative reaction to get feedback."""
        # several options for natural language responses
        responses = [
            "Thanks for the feedback! Since you seem to be an expert, could you tell me what was wrong with my answer? \U0001F648",
            "Thanks for the feedback! What specifically did you not like from my response? \U0001F648",
            "That's unfortunate, I'm sorry to hear that! What was wrong with my response? \U0001F648",
            "I'm sorry to hear that! How can I improve? \U0001F648",
            "Thanks for the feedback! What has made this answer so bad? \U0001F648"
        ]
        response = random.choice(responses)
        return response[0].upper() + response[1:]

    def natural_response_feedback_pos(self):
        """Returns a natural language string response to 
        a positive feedback."""
        # several options for natural language responses
        responses = [
            "You're a great person! \U0001F60D",
            "Thank you for your feedback! \U0001F60A",
            "I'm glad you liked it! \U0001F60D",
            "I'm happy to hear that! \U0001F60D",
            "I'm glad you enjoyed it! \U0001F60A",
            "I'm happy to hear that you enjoyed it! \U0001F60D"
        ]
        response = random.choice(responses)
        return response[0].upper() + response[1:]
    
    def natural_response_feedback_neg(self):
        """Returns a natural language string response to 
        a negative feedback."""
        # several options for natural language responses
        responses = [
            "I'm sorry you didn't like it. I'll try my best to improve! \U0001F61E",
            "I'm sorry you didn't like it. I'll try to improve! \U0001F61E",
            "I'll try to do better next time! \U0001F61E",
            "Sorry about that, I'll try to do better next time! \U0001F61E",
            "Your feedback is very important to me. I'll try to do better next time! \U0001F61E",
            "I will improve my performance next time! \U0001F61E"
        ]
        response = random.choice(responses)
        return response[0].upper() + response[1:]

if __name__ == "__main__":
    response = ResponseFormatter(None, None, None, None, None, None)
    print(response.natural_response_factual(("nationality", "Brad Pitt", "American"), True, False))
    print(response.natural_response_crowd((0.8, 2, 'American'), True, False))
    print(response.natural_response_embedding_one("American"))
    print(response.natural_response_embedding_several(("nationality", "Brad Pitt", "American", "French", "German")))
    print(response.natural_response_embedding_recommender(("Top Gun", "Harry Potter", "Guardians of the Galaxy")))
    print(response.natural_response_recommender(("Top Gun", "Harry Potter", "Guardians of the Galaxy", 100, "Pirates of the Carribean", 8.5)))
    print(response.natural_response_negative())
    print(response.natural_response_unknown())
    print(response.natural_response_no_picture())
    print(response.natural_response_msg_history())