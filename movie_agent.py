from Brain.brain import Brain
from Knowledge.graph import KnowledgeGraph

class MovieAgent:
    def __init__(self) -> None:
        KG = KnowledgeGraph()
        self.graph = KG.get_graph()
        self.ent2lbl = KG.ent2lbl
        self.lbl2ent = KG.lbl2ent
        self.rel2lbl = KG.rel2lbl
        self.ent2id = KG.ent2id
        self.id2ent =  KG.id2ent
        self.rel2id = KG.rel2id
        self.id2rel = KG.id2rel
        self.WD = KG.WD
        self.WDT = KG.WDT
        self.DDIS = KG.DDIS
        self.RDFS = KG.RDFS
        self.SCHEMA = KG.SCHEMA
        self.entity_emb = KG.entity_emb
        self.relation_emb = KG.relation_emb
        print('Movie agent initialized')

    def user_wish(self, text: str) -> tuple:
        brain = Brain(self.graph, self.ent2lbl, text)
        pred = brain.pred
        entities = brain.entities
        intent = brain.movie_intent
        classification = brain.ent_classifier(entities)
        match = brain.ent_matcher(entities)
        return pred, entities, intent, classification, match

if __name__ == '__main__':
    #ent = {'title': 'The Godfather', 'actor': 'Al Pacino'}
    movie_agent = MovieAgent()
    text = "Hello, was Al Pacino in The Godfather"
    pred, entities, intent, classification, match = movie_agent.user_wish(text)
    print(pred)
    print(entities)
    print(intent)
    print(classification)
    print(match)