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

def intent_text(text: str, pos: list, ner_pred: list) -> str:
    for tag in pos:
        if tag[1] not in ['IN', 'NN', 'NNS', 'NNP', 'NNPS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
            text = text.replace(tag[0], "")
    for token in ner_pred:
        if token[1] != 'O':
            text = text.replace(token[0], "")
    text = text.lower()
    text = text.strip()
    return text