import pickle
import os

from nltk import word_tokenize, pos_tag
from Brain.ner.utils.utils import pred2entity, sent2features

class EntityRecognizer:
    def __init__(self, crf=None):
        self.crf = [self.load_crf_model() if crf is None else crf][0]

    # load trained crf model
    def load_crf_model(self):
        dirname = os.path.dirname(__file__)
        with open(os.path.join(dirname, 'model/mycrf.pickle'), 'rb') as f:
            crf = pickle.load(f)
        return crf

    # TODO: different crf models depending on input (upper/lower case, etc.)   
    # extract entities from text
    def extract_entities(self, text: str) -> tuple:
        # tokenize text
        tokens = word_tokenize(text)
        # tag tokens
        tagged = pos_tag(tokens)
        # extract features
        features = sent2features(tagged)
        # predict entities
        y_pred = self.crf.predict([features])
        pred = []
        for i, t in enumerate(tokens):
            pred.append((t, y_pred[0][i]))
        entities = pred2entity(pred)
        return pred, entities

if __name__ == '__main__':
    # test entity recognizer
    text = 'Who is the director of Top Gun: Maverick?'
    ner = EntityRecognizer()
    pred, entities = ner.extract_entities(text)
    print(text)
    print(pred)
    print(entities)