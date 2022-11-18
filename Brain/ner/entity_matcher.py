import os
import pandas as pd

from Brain.ner.utils.utils import match_entities

class EntityMatcher:
    def __init__(self, graph, ent2lbl, WD):
        self.graph = graph
        self.ent2lbl = ent2lbl
        self.WD = WD
        self.entities = pd.read_csv('data/entities/graph_entities.csv')

    def match(self, entities: dict) -> dict:
        exact_match = {}
        for key, ent in entities.items():
            if type(ent) == list:
                for e in ent:
                    exact_match = match_entities(key, e, exact_match, self.ent2lbl, self.entities, self.WD)
            else:
                exact_match = match_entities(key, ent, exact_match, self.ent2lbl, self.entities, self.WD)
        return exact_match