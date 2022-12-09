import numpy as np
from sklearn.metrics import pairwise_distances


class EmbeddingSimilarity:
    def __init__(self, entity_emb, relation_emb, ent2lbl, lbl2ent, ent2id, id2ent, rel2id, WD, WDT):
        self.entity_emb = entity_emb
        self.relation_emb = relation_emb
        self.ent2lbl = ent2lbl
        self.lbl2ent = lbl2ent
        self.ent2id = ent2id
        self.id2ent = id2ent
        self.rel2id = rel2id
        self.WD = WD
        self.WDT = WDT

    def most_similar(self, subject, predicate=None, topn=10):
        """
        Returns the closest entities to the tail found by TransE
        """
        # parsing inputs
        s = list(v for v in subject.values())
        # check if first element is a list
        print(s)
        if type(s[0]) == list:
        #if type(s[0]) == list:
            lbl = s[0][0]
        else:
            lbl = s[0]
        print(lbl)
        subject = self.lbl2ent[lbl]
        # entity embedding
        head = self.entity_emb[self.ent2id[subject]]
        # relation embedding
        if predicate is not None:
            pred_uri = predicate.split('/')[-1]
            try:
                rel = self.relation_emb[self.rel2id[self.WDT[str(pred_uri)]]]
            except:
                return ['Not found']
            # combine according to the TransE scoring function
            tail = head + rel
        else:
            tail = head

        # compute distance to *any* entity
        distances = pairwise_distances(tail.reshape(1, -1), self.entity_emb).reshape(-1)

        # find most plausible tails
        most_likely = np.argsort(distances)

        # convert idx to ent
        label = []
        for idx in most_likely[:topn]:
            ent = self.id2ent[idx]
            lbl = self.ent2lbl[ent]
            label.append(lbl)

        # return the topn most plausible entities
        return label


    def most_similar_recommendation(self, rec_movies, topn=10):
        """
        Returns the closest entities to the tail found by TransE
        """
        # parsing inputs
        distances = None
        for movie in rec_movies:
            print(movie)
            movie = self.lbl2ent[movie]
            # entity embeddings
            head = self.entity_emb[self.ent2id[movie]]
            print(head)

            # compute distance to *any* entity
            if distances is None:
                distances = pairwise_distances(head.reshape(1, -1), self.entity_emb).reshape(-1)
                print(distances)
            else: distances += pairwise_distances(head.reshape(1, -1), self.entity_emb).reshape(-1)

        # average distances
        distances = distances / len(rec_movies)
        print(distances)
        
        # find most plausible tails
        most_likely = np.argsort(distances)

        # convert idx to ent
        label = []
        for idx in most_likely[:topn]:
            ent = self.id2ent[idx]
            lbl = self.ent2lbl[ent]
            label.append(lbl)

        print(label)

        # return the topn most plausible entities
        return label

if __name__ == '__main__':
    embed = EmbeddingSimilarity(None, None, None, None, None, None, None, None, None)
    embed.most_similar({'director' : ['Tony Scott'], 'title': 'Top Gun'})