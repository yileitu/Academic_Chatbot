# TODO: intelligence for chatbot
from ner.entity_recognizer import EntityRecognizer

class Brain:
    # initialize brain class
    def __init__(self, text: str):
        self.ner = self.ner(text)
        # self.intent = self.intent()
        # self.response = self.response()

    # named entity recognition
    def ner(self, text: str) -> list:
        # entities from entity recognizer
        movie_ner = EntityRecognizer()
        entities = movie_ner.extract_entities(text)
        return entities

    # intent recognition
    def intent(self, text: str) -> str:
        pass

    # response generation
    def response(self, text: str) -> str:
        pass

if __name__ == '__main__':
    # test brain
    text = input('Enter text: ')
    brain = Brain(text.rstrip("?"))
    print(text)
    print(brain.ner)
    # print(brain.intent)
    # print(brain.response)