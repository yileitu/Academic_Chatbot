from sklearn.metrics import pairwise_distances
from sentence_transformers import SentenceTransformer
from nltk import word_tokenize
import pandas as pd
import numpy as np
import os

def question_similarity(text: str) -> str:
    """
    Returns the question type of the user input based on similarity to patterns
    """
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    sentence = model.encode(text)
    pattern_emb = np.load('patterns/pattern_embeds.npy')
    # find the closest question pattern
    # calculate the min distance to each key of the dictionary
    distances = pairwise_distances(sentence.reshape(1, -1), pattern_emb).reshape(-1)
    min_distance_idx = np.argmin(distances)
    df = pd.read_csv('patterns/all_patterns.csv')
    closest_pattern = df.iloc[min_distance_idx, 0]
    # get the question type
    patterns = question_patterns()
    # find the key with the lowest distance
    best_match = 'No question type found'
    for key, value in patterns.items():
        for pattern in value:
            if pattern == closest_pattern:
                best_match = key
    return best_match 

def question_type(text: str) -> str:
    """
    Returns the question type of the user input
    """
    patterns = question_patterns()
    for key, value in patterns.items():
        for pattern in value:
            if pattern == text:
                return key
    return 'unknown'

def embed_patterns():
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    patterns = question_patterns()
    all_patterns_list = [value for key, value in patterns.items()]
    all_patterns = [item for sublist in all_patterns_list for item in sublist]
    pattern_emb = model.encode(all_patterns)
    dirname = os.path.dirname(__file__)
    # save all_patterns as csv
    df = pd.DataFrame(all_patterns)
    df.to_csv(os.path.join(dirname, 'patterns/all_patterns.csv'), index=False)
    # save pattern_emb as numpy array
    np.save(os.path.join(dirname, 'patterns/pattern_embeds.npy'), pattern_emb)
    return all_patterns

def question_patterns() -> dict: # TODO: extend with more patterns
    """
    Returns a dictionary of question patterns for all types of movie questions
    """
    patterns = {"factual": ["Who is the director of X?",
                            "Who directed X Y Z?",
                            "Who directed the movie X Y Z?",
                            "Who performed in XY?", 
                            "What is the box office of The X?",
                            "Can you tell me the publication date of XY?",
                            "Who is the executive producer of X?",
                            "Who is the screenwriter of XY?",
                            "What is the MPAA film rating of XY?",
                            "What is the genre of X?",
                            "Who is the father of Z?",
                            "What is the birth date of Z?"],
                "check": ["Is it true that X directed Y?",
                            "Is it true that X performed in Y?",
                            "Is it true that X is the Y of Z?"],
                "recommendation": ["Recommend movies similar to A and B.",
                                   "Given that I like A, B and C, can you recommend some movies?",
                                   "Recommend movies like A, B and C.",
                                   "Recommend movies similar to A, B and C.",
                                   "What should I watch if I like A?",
                                   "I really like watching A, what else should I watch?",
                                   "What should I watch if I like A, B and C?",
                                   "Give me some movie recommendations similar to B."],
                "multimedia": ["Show me a picture of X.",
                                "What does Y look like?",
                                "Let me know what XY looks like.",
                                "Picture of YZ.",
                                "Show me a picture of Z.",
                                "Show me a picture of ZA.",
                                "I wonder what a A looks like."]}
    return patterns

def clean_text(text: str) -> str:
        text = text.replace('?', '')
        text = text.replace('!', '')
        text = text.replace('.', '') # TODO: What to remove?
        #text = text.replace(',', '')
        return text
        
if __name__ == '__main__':
    text = "I like movies that Al Pacino starred in"
    text1 = "I wonder what Al Pacino looks like"
    text2 = "What is the IMDB film rating for Top Gun: Maverick?"
    text3 = "What is the filming location of Avatar?"
    text4 = "Who is the father of Tom Hanks?"
    text5 = "what is the country of citizenship of Cho Geun-hyeon?"
    text6 = "Who directed The Bridge on the River Kwai?"
    print(clean_text(text6))
    #embed_patterns()
    sim = question_similarity(clean_text(text6))
    print(sim)