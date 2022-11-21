import pandas as pd
import numpy as np
import pickle

class MovieRecommender:

    def __init__(self, ent2lbl, lbl2ent, rel2lbl, lbl2rel, WD, WDT):
        self.ent2lbl = ent2lbl
        self.lbl2ent = lbl2ent
        self.rel2lbl = rel2lbl
        self.lbl2rel = lbl2rel
        self.WD = WD
        self.WDT = WDT
        self.plots = pd.read_csv('data/recommender/plots.csv')
        self.cosine_sim = pickle.load(open('data/recommender/cosine_sim.pickle', 'rb'))
        self.indices = pickle.load(open('data/recommender/indices.pickle', 'rb')) 
        print('MovieRecommender initialized')

    def recommend_movie(self, movie):
        """
        Recommend a movie based on similar plots
        """
        # check if movie is in the database
        print(movie)
        movie = self.lbl2ent[movie]
        if movie in self.plots['qid'].values:
            # get the recommendations
            rec = self.get_recommendations(movie)

            # get labels of the recommendations
            # split uri from entity
            rec_uri = []
            for r in rec:
                rec_uri.append(r.split('/')[-1])
            # get labels
            rec_lbl = [self.ent2lbl[self.WD[q]] for q in rec_uri]

            # return the recommendations
            return rec_lbl
        else:
            return 'Movie not in database'

    def get_recommendations(self, qid):
        """
        Function that takes in movie qid as input and outputs most similar movies
        """
        # get the index of the movie that matches the qid
        print(qid)
        idx = self.indices[str(qid)]

        # get the pairwsie similarity scores of all movies with that movie
        sim_scores = list(enumerate(self.cosine_sim[idx]))

        # sort the movies based on the similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # get the scores of the 10 most similar movies
        sim_scores = sim_scores[1:11]

        # get the movie indices
        movie_indices = [i[0] for i in sim_scores]

        # return the top 10 most similar movies
        return self.plots['qid'].iloc[movie_indices]

if __name__ == '__main__':
    recommender = MovieRecommender(None, None, None, None, None, None)
    # go to directory where the data is stored
    import os
    os.chdir('data/recommender')
    recommender.plots = pd.read_csv('plots.csv')
    recommender.cosine_sim = pickle.load(open('cosine_sim.pickle', 'rb'))
    recommender.indices = pickle.load(open('indices.pickle', 'rb'))
    print(recommender.get_recommendations('http://www.wikidata.org/entity/Q15270932'))