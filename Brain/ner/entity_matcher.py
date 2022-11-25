import os
import pandas as pd

from Brain.ner.utils.utils import match_entities, check_entity_types

class EntityMatcher:
    def __init__(self, graph, ent2lbl, WD):
        self.graph = graph
        self.ent2lbl = ent2lbl
        self.WD = WD
        #self.entities = pd.read_csv('data/entities/graph_entities.csv')
        self.actors = pd.read_csv('data/entities/graph_actors.csv')
        self.directors = pd.read_csv('data/entities/graph_directors.csv')
        self.movies = pd.read_csv('data/entities/graph_movies.csv')
        self.genres = pd.read_csv('data/entities/graph_genres.csv')
        self.characters = pd.read_csv('data/entities/graph_characters.csv')
        print("EntityMatcher initialized")


    def match(self, entities: dict) -> dict:
        exact_match = {}
        for key, ent in entities.items():
            if type(ent) == list:
                for e in ent:
                    exact_match = match_entities(key, e, exact_match, self.ent2lbl, self.WD, self.actors, self.directors, self.characters, self.genres, self.movies)
            else:
                exact_match = match_entities(key, ent, exact_match, self.ent2lbl, self.WD, self.actors, self.directors, self.characters, self.genres, self.movies)
        return exact_match