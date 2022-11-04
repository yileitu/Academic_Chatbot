import pickle
import os

from nltk import word_tokenize, pos_tag
from ner.utils.utils import sent2features

class EntityRecognizer:
    def __init__(self, crf=None):
        self.crf = [self.load_crf_model() if crf is None else crf][0]

    # load trained crf model
    def load_crf_model(self):
        dirname = os.path.dirname(__file__)
        with open(os.path.join(dirname, 'model/mycrf.pickle'), 'rb') as f:
            crf = pickle.load(f)
        return crf
        
    # extract entities from text
    def extract_entities(self, text: str) -> list:
        # entities
        entities = []
        # tokenize text
        tokens = word_tokenize(text)
        # tag tokens
        tagged = pos_tag(tokens)
        # extract features
        features = sent2features(tagged)
        # predict entities
        pred = self.crf.predict([features])[0]
        entities.append(pred)
        return entities