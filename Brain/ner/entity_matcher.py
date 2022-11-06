import os
import pandas as pd

from Brain.ner.utils.utils import match_entities

class EntityMatcher:
    def __init__(self, graph, ent2lbl):
        self.graph = graph
        self.ent2lbl = ent2lbl
        self.entities = pd.read_csv('data/entities/graph_entities.csv')

    def match(self, entities: dict) -> dict:
        exact_match = {}
        for ent in entities.values():
            if type(ent) == list:
                for e in ent:
                    exact_match = match_entities(e, exact_match, self.ent2lbl, self.entities)
            else:
                exact_match = match_entities(ent, exact_match, self.ent2lbl, self.entities)
        return exact_match