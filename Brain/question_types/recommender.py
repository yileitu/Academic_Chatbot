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
        self.plots = pd.read_csv('data/recommender/plots_expanded.csv')
        self.cosine_sim = pickle.load(open('data/recommender/cosine_sim.pickle', 'rb'))
        self.indices = pickle.load(open('data/recommender/indices.pickle', 'rb')) 
        print('MovieRecommender initialized')

    def recommend_movie(self, movies: dict):
        """
        Recommend a movie based on similar plots
        """
        rec_movies = []
        for movie in movies['title']:
            # check if movie is in the database
            movie = self.lbl2ent[movie]
            if movie in self.plots['qid'].values:
                rec_movies.append(movie)

        # if no movies are found, return none
        if len(rec_movies) > 0:    
            # get the recommendations
            rec = self.get_recommendations(rec_movies)
            # get labels of the recommendations
            # # split uri from entity
            # rec_uri = []
            # for r in rec['qid']:
            #     rec_uri.append(r.split('/')[-1])
            # # get labels
            # rec_lbl = [self.ent2lbl[self.WD[q]] for q in rec_uri]

            sim_movies = []
            for i, r in rec.iterrows():
                sim_movies.append({'title': r['Title'], 'rating': r['IMDb Rating'], 'nr_voters': r['Num Votes']})

            # return the recommendations
            return sim_movies
        else:
            return 'Movie not in database'

    def get_recommendations(self, qids):
        """
        Function that takes in movie qid as input and outputs most similar movies
        """
        # get the index of the movie that matches the qid
        sim_scores = 0
        for qid in qids:
            idx = self.indices[str(qid)]
            if sim_scores == 0:
                # get the pairwsie similarity scores of all movies with that movie
                sim_scores = list(self.cosine_sim[idx])
            else:
                score = list(self.cosine_sim[idx])
                for i, s in enumerate(sim_scores):
                    sim_scores[i] += score[i]
        # enumerate the scores
        sim_scores = list(enumerate(sim_scores))

        # average the individual scores
        sim_scores = [(i, s/len(qids)) for i, s in sim_scores]

        # sort the movies based on the similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # get the scores of the 10 most similar movies
        sim_scores = sim_scores[1:11]

        # get the movie indices
        movie_indices = [i[0] for i in sim_scores]

        # return the top 10 most similar movies
        sim_movies = self.plots.iloc[movie_indices]
        return sim_movies

        # # sort the movies based on the imdb rating from file
        # sim_movies_rated = sorted(sim_movies, key=lambda x: self.plots[self.plots['qid'] == x]['IMDb Rating'].values[0], reverse=True) # TODO: enable/disable rating-based filtering (surprise)?
        # return sim_movies_rated # TODO: return top 10 similar movies and the movie that is best rated (inkl. rating and nr voters)

if __name__ == '__main__':
    recommender = MovieRecommender(None, None, None, None, None, None)
    # go to directory where the data is stored
    import os
    os.chdir('data/recommender')
    recommender.plots = pd.read_csv('plots_expanded.csv')
    recommender.cosine_sim = pickle.load(open('cosine_sim.pickle', 'rb'))
    recommender.indices = pickle.load(open('indices.pickle', 'rb'))
    print(recommender.get_recommendations(['http://www.wikidata.org/entity/Q161678', 'http://www.wikidata.org/entity/Q232009']))