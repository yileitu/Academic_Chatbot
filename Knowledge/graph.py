import os
import pickle
import numpy as np
import rdflib
import csv

class KnowledgeGraph(object):
    def __init__(self):
        # load the knowledge graph
        with open ('data/fixed_graph.pickle', 'rb') as f:
            self.graph = pickle.load(f)
        # load the embeddings
        self.entity_emb = np.load('data/ddis-graph-embeddings/entity_embeds.npy')
        self.relation_emb = np.load('data/ddis-graph-embeddings/relation_embeds.npy')
        self.entity_file = 'data/ddis-graph-embeddings/entity_ids.del'
        self.relation_file = 'data/ddis-graph-embeddings/relation_ids.del'
        # load the entity and relation dictionaries
        with open(self.entity_file, 'r') as ifile:
            self.ent2id = {rdflib.term.URIRef(ent): int(idx) for idx, ent in csv.reader(ifile, delimiter='\t')}
            self.id2ent = {v: k for k, v in self.ent2id.items()}
        with open(self.relation_file, 'r') as ifile:
            self.rel2id = {rdflib.term.URIRef(rel): int(idx) for idx, rel in csv.reader(ifile, delimiter='\t')}
            self.id2rel = {v: k for k, v in self.rel2id.items()}
        # define prefixes
        self.WD = rdflib.Namespace('http://www.wikidata.org/entity/')
        self.WDT = rdflib.Namespace('http://www.wikidata.org/prop/direct/')
        self.DDIS = rdflib.Namespace('http://ddis.ch/atai/')
        self.RDFS = rdflib.namespace.RDFS
        self.SCHEMA = rdflib.Namespace('http://schema.org/')
        # link the entity by finding its corresponding node in the knowledge graph
        self.ent2lbl = {ent: str(lbl) for ent, lbl in self.graph.subject_objects(self.RDFS.label)}
        self.lbl2ent = {lbl: ent for ent, lbl in self.ent2lbl.items()}
        self.rel2lbl = {rel: str(lbl) for rel, lbl in self.graph.subject_objects(self.RDFS.label)}
        print('Knowledge graph, embeddings and dictionaries loaded')

    # get the knowledge graph   
    def get_graph(self):
        return self.graph

    # get a specific entity
    def get_node(self, node):
        return self.graph[node]

    # get a specific relation
    def get_edge(self, node1, node2):
        return self.graph[node1][node2]
    
    def graph2pickle(self):
        dirname = os.path.dirname(__file__)
        with open (os.path.join(dirname, 'data/KG.pickle'), 'wb') as f:
            pickle.dump(self.graph, f)