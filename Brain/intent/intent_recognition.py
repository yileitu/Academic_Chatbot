import numpy as np
import pandas as pd
import os
import sklearn

from sentence_transformers import SentenceTransformer
from sklearn.metrics import pairwise_distances


class IntentRecognizer:
    def __init__(self, model=None):
        self.model = [self.load_intent_model() if model is None else model][0]

    # load trained intent model
    def load_intent_model(self):
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        return model

    # extract intent from text
    def extract_intent(self, text: str) -> list:
        # load expanded graph properties
        dirname = os.path.dirname(__file__)
        properties_exp = pd.read_csv(os.path.join(
            dirname, 'model/graph_properties_expanded.csv'))
        # load intent labels
        df = pd.read_csv(os.path.join(
            dirname, 'model/properties.csv'))
        intent_labels = df['Intent'].tolist()
        # load intent vectors
        with open(os.path.join(dirname, 'model/property_embeds.npy'), 'rb') as f:
            intent_vectors = np.load(f)
        # encode text
        text_vector = self.model.encode(text)
        # compute pairwise distances
        dist = pairwise_distances(text_vector.reshape(1, -1), intent_vectors).reshape(-1)
        # extract intent
        most_likely = dist.argsort()
        # find top match
        try:
            top_matches = [
                (
                    properties_exp.loc[properties_exp['PropertyLabel']
                                    == intent_labels[index], 'Property'].values[0],
                    intent_labels[index],  # label
                    dist[index],  # score
                    rank + 1,  # rank
                )
                for rank, index in enumerate(most_likely[:5])]
            return top_matches
        except:
            return [None]

if __name__ == '__main__':
    # test intent recognition
    text = 'who is the director of'
    text1 = 'what is the genre of'
    text2 = 'who directed'
    text3 = 'What is the MPAA film rating of'
    intent = IntentRecognizer()
    intent = intent.extract_intent(text3)
    print(text3)
    print(intent)