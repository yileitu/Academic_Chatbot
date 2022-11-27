# Utils for Named Entity Recognition
import os
import numpy as np
from sentence_transformers import SentenceTransformer
import pandas as pd
from sklearn.metrics import pairwise_distances


def collate(dataframe):
    agg_func = lambda s: [(w, p, t) for w, p, t in zip(s['words'].values.tolist(), s['pos'].values.tolist(), s['tags'].values.tolist())]
    grouped = dataframe.groupby('sentence_id').apply(agg_func)
    return list(grouped)

def word2features(sent, i):
    word = sent[i][0]
    postag = sent[i][1]

    features = {
        'bias': 1.0,
        'word.lower()': word.lower(),
        'word[-3:]': word[-3:],
        'word[-2:]': word[-2:],
        'word.isupper()': word.isupper(),
        'word.istitle()': word.istitle(),
        'word.isdigit()': word.isdigit(),
        'postag': postag,
        'postag[:2]': postag[:2],
    }
    if i > 0:
        word1 = sent[i-1][0]
        postag1 = sent[i-1][1]
        features.update({
            '-1:word.lower()': word1.lower(),
            '-1:word.istitle()': word1.istitle(),
            '-1:word.isupper()': word1.isupper(),
            '-1:postag': postag1,
            '-1:postag[:2]': postag1[:2],
        })
    else:
        features['BOS'] = True

    if i < len(sent)-1:
        word1 = sent[i+1][0]
        postag1 = sent[i+1][1]
        features.update({
            '+1:word.lower()': word1.lower(),
            '+1:word.istitle()': word1.istitle(),
            '+1:word.isupper()': word1.isupper(),
            '+1:postag': postag1,
            '+1:postag[:2]': postag1[:2],
        })
    else:
        features['EOS'] = True

    return features

def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]

def sent2labels(sent):
    return [label for token, postag, label in sent]

# from prediction to entity
def pred2entity(pred):
   entities = {} 
   entity = ''
   label = ''
   for i, (w, t) in enumerate(pred):
      if t != 'O':
         if pred[i-1][1][2:] != t[2:]:
            if entity != '' and label != '':
               if label in entities:
                  entities[label].append(entity)
               else:
                  entities[label] = [entity]
               entity = ''
               label = ''
            entity = w
            label = t[2:].lower()
         else:
            entity = entity + ' ' + w
   if entity != '' and label != '':
      if label in entities:
         entities[label].append(entity)
      else:
         entities[label] = entity
   return entities

# match entities to knowledge base
def match_entities(key, ent, exact_match, ent2lbl, WD, actors, directors, characters, genres, movies):
    # exact match with entity labels
    if ent in ent2lbl:
        exact_match[key] = ent2lbl[WD[ent]]
    # match with entity embeddings
    else:
        dirname = os.path.dirname(__file__)
        label_emb = np.load(os.path.join(dirname, 'labels/entity_label_embeds.npy'))
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        ent_emb = model.encode([ent])
        distances = pairwise_distances(ent_emb.reshape(1, -1), label_emb).reshape(-1)
        most_likely = np.argsort(distances)
        closest = most_likely[0]
        df = pd.read_csv(os.path.join(dirname, 'labels/entities_labels.csv'))
        # find closest match in entities
        closest_match = df.iloc[closest]['EntityLabel']
        print(f"Closest match for {ent} is {closest_match}")
        # check if entity types match
        key = check_entity_types(key, closest_match, actors, directors, characters, genres, movies)
        print(key)
        # get qid of closest match
        exact_match[key] = closest_match
    # else:
    #     fuzzy_match = entities.loc[entities['EntityLabel'].str.lower().str.contains(ent.lower(), regex=False), 'Entity'].values
    #     print(f"Fuzzy match for {ent}: {fuzzy_match}")
    #     if len(fuzzy_match) > 0:
    #         exact_match[key] = ent2lbl[WD[fuzzy_match[0]]]
    #     else:
    #         exact_match[ent] = 'unknown'
    return exact_match

def check_entity_types(key: str, closest_match: str, actors, directors, characters, genres, movies) -> str: # TODO: better engineering
    """
    Check if the entity types match with entity types in the graph
    """
    if key == 'title':
        if closest_match in movies['EntityLabel'].values:
            return key
    elif key == 'actor':
        if closest_match in actors['EntityLabel'].values:
            return key 
    elif key == 'director':
        if closest_match in directors['EntityLabel'].values:
            return key
    elif key == 'genre':
        if closest_match in genres['EntityLabel'].values:
            return key
    elif key == 'character':
        if closest_match in characters['EntityLabel'].values:
            return key
    
    # key is wrong, get correct key by checking for closest match
    if closest_match in movies['EntityLabel'].values:
        return 'title'
    elif closest_match in actors['EntityLabel'].values:
        return 'actor'
    elif closest_match in directors['EntityLabel'].values:
        return 'director'
    elif closest_match in genres['EntityLabel'].values:
        return 'genre'
    elif closest_match in characters['EntityLabel'].values:
        return 'character'
    else:
        return 'unknown'


def embed_labels():
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    dirname = os.path.dirname(__file__)
    df = pd.read_csv(os.path.join(dirname, 'labels/entities_labels.csv'))
    labels = df['EntityLabel'].values
    label_emb = model.encode(labels)
    # save pattern_emb as numpy array
    np.save(os.path.join(dirname, 'labels/entity_label_embeds.npy'), label_emb)
    return labels