# responsed for different types of requests
import random

def natural_response_factual(results):
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
        responses = [
            f"The {results[0]} of {results[1]} is {results[2]}.",
            f"The answer is {results[2]}.",
            f"{results[2]} is the {results[0]} of {results[1]}.",
            f"{results[2]} is the answer.",
            f"{results[2]} is the correct answer.",
            f"{results[2]} is the right answer.",
            f"That would be {results[2]}."   
        ]
    return random.choice(responses)

def natural_response_crowd(results):
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
        responses = [
            f"With an inter-rate agreement of {results[0]} in this batch and a support of {results[1]} out of 3 votes, the answer is {results[2]}.",
            f"The answer is {results[2]} with an inter-rate agreement of {results[0]} in this batch and a support of {results[1]} out of 3 votes.",
            f"{results[2]} is the answer, with an inter-rate agreement of {results[0]} in this batch and a support of {results[1]} out of 3 votes.",
            f"{results[2]} is the correct answer with an inter-rate agreement of {results[0]} in this batch and a support of {results[1]} out of 3 votes.",
            f"The crowd, with an inter-rate agreement of {results[0]} in this batch and a support of {results[1]} out of 3 votes, thinks the answer is {results[2]}.",
            f"It is {results[2]}, according to the crowd with an inter-rate agreement of {results[0]} in this batch and a support of {results[1]} out of 3 votes."
        ]
    return random.choice(responses)

def natural_response_embedding_one(results):
    """Returns a natural language string response to an embedding question."""
    # several options for natural language responses
    responses = [
        f"I feel that the answer should be {results}.",
        f"I think it should be {results}.",
        f"I would say it should be {results}.",
        f"I would guess it is actually {results}.",
        f"in my opinion, the answer is actually {results}.",
        f"I would say it should rather be {results}."
    ]
    return random.choice(responses)

def natural_response_embedding_several(results):
    """Returns a natural language string response (several) to an embedding question."""
    # several options for natural language responses
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
    return random.choice(responses)

def natural_response_embedding_recommender(results):
    """Returns a natural language string response to recommend embedding answers."""
    # several options for natural language responses
    responses = [
        f"Similar movies are {results[0]}, {results[1]} and {results[2]}.",
        f"Based on your preferences, I would recommend you to watch {results[0]}, {results[1]} and {results[2]}.",
        f"You should watch {results[0]}, {results[1]} and {results[2]}.",
        f"I would recommend you to watch {results[0]}, {results[1]} and {results[2]}.",
        f"Your next movies should be {results[0]}, {results[1]} and {results[2]}.",
        f"Definitely consider watching {results[0]}, {results[1]} and {results[2]}.",
        f"A good choice would be {results[0]}, {results[1]} and {results[2]}."
    ]
    return random.choice(responses)


def natural_response_recommender(results): # TODO: answers based on response time (also images)
    """Returns a natural language string response to recommend movies."""
    # several options for natural language responses
    responses = [
        f"Similar movies are {results[0]}, {results[1]} and {results[2]}. Based on the ratings of {results[3]} IMDb users I would recommend you to watch {results[4]} with an overall rating of {results[5]}.",
        f"I would say it should be {results[0]}, {results[1]} or {results[2]}. Based on the ratings of {results[3]} IMDb users I would recommend you to watch {results[4]} with an overall rating of {results[5]}.",
        f"Based on the ratings of {results[3]} IMDb users I would recommend you to watch {results[4]} with an overall rating of {results[5]}.",
        f"Seeing that {results[3]} IMDb users rated {results[4]} with an overall rating of {results[5]}, I would recommend you to watch {results[4]}.",
        f"You will probably like {results[0]}, {results[1]} and {results[2]}. Based on the ratings of {results[3]} IMDb users your top pick is {results[4]} with an overall rating of {results[5]}.",
        f"You have good taste. Based on the ratings of {results[3]} IMDb users I would recommend you to watch {results[4]} with an overall rating of {results[5]}.",
        f"Nice, you definitely know your movies. Based on the ratings of {results[3]} IMDb users I would recommend you to watch {results[4]} with an overall rating of {results[5]}."
    ]
    return random.choice(responses)

def natural_response_negative():
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
        "You seem to be an expert. Even my knowledge is not sufficient to answer this question."
    ]
    return random.choice(responses)

def natural_response_unknown():
    """Returns a natural language string response to 
    a misunderstood question."""
    # several options for natural language responses
    responses = [
        "Could you rephrase that?",
        "I'm sorry, I don't understand.",
        "I don't understand.",
        "I'm afraid I don't understand.",
        "I'm sorry, I don't know.",
        "Sorry, I have no clue..."
    ]
    return random.choice(responses)

def natural_response_no_picture():
    """Returns a natural language string response to 
    a misunderstood question or where the answer is not known (pictures)."""
    # several options for natural language responses
    responses = [
        "I'm sorry, I didn't manage to find a picture.",
        "Uups, it seems that this picture is missing.",
        "Someone burned all their pictures.",
        "They never took a picture.",
        "Damn, this person seems to be not very photogenic."
    ]
    return random.choice(responses)

def natural_response_msg_history():
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
    return random.choice(responses)

if __name__ == "__main__":
    print(natural_response_factual(("nationality", "Brad Pitt", "American")))
    print(natural_response_crowd((0.8, 2, "American")))
    print(natural_response_embedding_one("American"))
    print(natural_response_embedding_several(("nationality", "Brad Pitt", "American", "French", "German")))
    print(natural_response_embedding_recommender(("Top Gun", "Harry Potter", "Guardians of the Galaxy")))
    print(natural_response_recommender(("Top Gun", "Harry Potter", "Guardians of the Galaxy", 100, "Pirates of the Carribean", 8.5)))
    print(natural_response_negative())
    print(natural_response_unknown())
    print(natural_response_no_picture())
    print(natural_response_msg_history())