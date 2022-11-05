# Utils for Named Entity Recognition
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