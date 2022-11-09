import pickle
import os

# detect casing of text
def detect_casing(text: str):
    if text.islower():
        return 'uncased'
    else:
        return 'cased'

# load corresponding crf model depending on casing
def load_crf_model(casing: str):
    dirname = os.path.dirname(__file__)
    if casing == 'cased':
        with open(os.path.join(dirname, 'ner/model/crf_cased.pickle'), 'rb') as f:
            crf = pickle.load(f)
    else:
        with open(os.path.join(dirname, 'ner/model/crf_uncased.pickle'), 'rb') as f:
            crf = pickle.load(f)
    return crf