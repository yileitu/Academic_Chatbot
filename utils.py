from scipy import spatial
from sentence_transformers import SentenceTransformer
from nltk import word_tokenize

def question_similarity(text: str, patterns: dict) -> str:
    """
    Returns the question type of the user input based on sentence similarity
    """
    highest_similarity = 0
    best_match = ''
    for key, value in patterns.items():   
        for pattern in value:
            # return highest similarity
            similarity = sentence_similarity(text, pattern)
            if similarity > highest_similarity:
                highest_similarity = similarity
                best_match = key
    return best_match

def sentence_similarity(text1: str, text2: str) -> float:
    """
    Returns the similarity between two sentences
    """
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    sentence1 = model.encode(text1)
    sentence2 = model.encode(text2)
    return 1 - spatial.distance.cosine(sentence1, sentence2)

def sentence_similarity1(text1: str, text2: str) -> float:
    """
    Returns the similarity between two sentences
    """
    sentence1 = [word.lower() for word in word_tokenize(text1)]
    sentence2 = [word.lower() for word in word_tokenize(text2)]
    all_words = list(set(sentence1 + sentence2))
    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)
    for word in sentence1:
        vector1[all_words.index(word)] += 1
    for word in sentence2:
        vector2[all_words.index(word)] += 1
    return 1 - spatial.distance.cosine(vector1, vector2)    

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

def question_patterns() -> dict:
    """
    Returns a dictionary of question patterns for all types of movie questions
    """
    patterns = {"factual": ["Who is the director of Good Will Hunting?", 
                            "Who directed The Bridge on the River Kwai?", 
                            "Who is the director of Star Wars: Episode VI - Return of the Jedi?"], 
                "embedding": ["Who is the screenwriter of The Masked Gang: Cyprus?",
                                "What is the MPAA film rating of Weathering with You?",
                                "What is the genre of Good Neighbors?"],
                "recommendation": ["Hi, given that I like movies that Al Pacino starred in, what movies would you recommend?",
                                    "Recommend movies similar to Hamlet and Othello.",
                                    "Given that I like The Lion King, Pocahontas, and The Beauty and the Beast, can you recommend some movies?",
                                    "Recommend movies like Nightmare on Elm Street, Friday the 13th, and Halloween."],
                "multimedia": ["Show me a picture of Halle Berry.",
                                "What does Julia Roberts look like?",
                                "Let me know what Sandra Bullock looks like."],
                "crowdsourcing": ["What is the box office of The Princess and the Frog?",
                                    "Can you tell me the publication date of Tom Meets Zizou?",
                                    "Who is the executive producer of X-Men: First Class?"]}
    return patterns

def clean_text(text: str) -> str:
        text = text.replace('?', '')
        text = text.replace('!', '')
        text = text.replace('.', '')
        text = text.replace(',', '') # TODO: What to remove?
        return text
        
if __name__ == '__main__':
    text = "I like movies that Al Pacino starred in"
    text1 = "I wonder what Al Pacino looks like"
    text2 = "What is the IMDB film rating for Top Gun: Maverick?"
    sim = question_similarity(text2, question_patterns())
    print(sim)