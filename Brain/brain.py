# TODO: intelligence for chatbot
from intent.intent_recognition import IntentRecognizer
from ner.entity_recognizer import EntityRecognizer

class Brain:
    # initialize brain class
    def __init__(self, text: str):
        self.pred, self.entities = self.ner(text)
        self.intent = self.intent(text)
        self.classification = self.classification(self.entities)

    # named entity recognition
    def ner(self, text: str) -> tuple:
        # entities from entity recognizer
        movie_ner = EntityRecognizer()
        pred, entities = movie_ner.extract_entities(text)
        print(entities)
        return pred, entities

    # intent recognition
    def intent(self, text: str) -> list:
        movie_intent = IntentRecognizer()
        intent = movie_intent.extract_intent(text)
        return intent

    # classify recognized entities
    def classification(self, entities: dict) -> str:
        for entity in entities.keys():
            if entity == 'title':
                return 'movie'
            elif entity == 'actor':
                return 'person'
            elif entity == 'genre':
                return 'genre'
            else:
                return 'unknown'

if __name__ == '__main__':
    # test brain
    text = 'Who is the director of Top Gun: Maverick?'
    brain = Brain(text)
    print(text)
    print(brain.classification)