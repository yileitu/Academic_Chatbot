import pickle
import os

from nltk import word_tokenize, pos_tag
from Brain.ner.utils.utils import pred2entity, sent2features
#from utils.utils import pred2entity, sent2features
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

class EntityRecognizer:
    def __init__(self, crf=None):
        self.crf = [None if crf is None else crf][0]
        if self.crf is None:
            self.tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER-uncased")
            self.model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER-uncased")
            self.pipe = pipeline(model=self.model, tokenizer=self.tokenizer, task='ner')

    def extract_entities(self, text: str) -> tuple:
        """
        Extracts entities from text using a CRF model, NLTK tokens and POS tags.
        """
        try:
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
            return tagged, pred, entities
        except Exception as e:
            print(e)
            return {}, {}, {}

    def extract_recommender_entities(self, text: str) -> dict:
        """
        Extracts entities from text using a pretrained BERT model.
        """
        try:
            # NER pipeline
            ner = self.pipe(text)
            # concatenate the tokens to entitiesBrain.ner.
            entities = {}
            entities['title'] = []
            entities['actor'] = []
            for i in range(len(ner)):
                if ner[i]['entity'] == 'B-MISC' or ner[i]['entity'] == 'I-MISC':
                    # concatenate words with hashtags at the beginning
                    if ner[i]['word'][0] == '#':
                        entities['title'][-1] = entities['title'][-1] + (ner[i]['word']).replace('#', '')
                    else: 
                        if ner[i]['entity'] != 'B-MISC':
                            if ner[i - 1]['entity'] == 'B-MISC' or ner[i - 1]['entity'] == 'I-MISC':
                                entities['title'][-1] = entities['title'][-1] + ' ' + ner[i]['word']
                        else: entities['title'].append(ner[i]['word'])
                else:
                    if ner[i]['entity'] == 'B-PER' or ner[i]['entity'] == 'I-PER':
                        # concatenate words with hashtags at the beginning
                        if ner[i]['word'][0] == '#':
                            entities['actor'][-1] = entities['actor'][-1] + (ner[i]['word']).replace('#', '')
                        else:
                            if ner[i]['entity'] != 'B-PER':
                                if ner[i - 1]['entity'] == 'B-PER' or ner[i - 1]['entity'] == 'I-PER':
                                    entities['actor'][-1] = entities['actor'][-1] + ' ' + ner[i]['word']
                            else: entities['actor'].append(ner[i]['word'])
                    else:
                        continue
            return entities
        except Exception as e:
            print(e)
            return {}

if __name__ == '__main__':
    # test entity recognizer
    text = 'Who is the director of Top Gun: Maverick?'
    text1 = 'what does daniel craig look like'
    text2 = 'Recommend movies similar to Hamlet and Othello.'
    text3 = 'Given that I like The Lion King, Pocahontas, and The Beauty and the Beast, can you recommend some movies?'
    text4 = 'Recommend movies like Nightmare on Elm Street, Friday the 13th, and Halloween.'
    text5 = 'what is the country of citizenship of Cho Geun-hyeon'
    text6 = "Recommend movies like Forrest Gump, The Shawshank Redemption, and The Green Mile."
    text7 = 'what should I watch if I liked The Avengers: Endgame, The Dark Knight, and The Lord of the Rings: The Return of the King?'
    ner = EntityRecognizer()
    # pos, pred, entities = ner.extract_entities(text1)
    # print(text)
    # print(pos)
    # print(pred)
    # print(entities)
    entities = ner.extract_recommender_entities(text6)
    print(entities)