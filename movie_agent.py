from Brain.brain import Brain
from Knowledge.graph import KnowledgeGraph
from Query.SPARQL import SPARQL
from utils import question_patterns, question_similarity, question_type

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

    def user_wish(self, text: str) -> str:
        """
        Returns the answer to the user input
        """
        patterns = question_patterns()
        similarity = question_similarity(text, patterns)
        if similarity == 'factual':
            return self.factual_query(text)
        elif similarity == 'recommendation':
            # TODO: implement recommendation
            return 'recommendation'
            #return self.recommendation(text)
        elif similarity == 'multimedia':
            # TODO: implement multimedia
            return 'multimedia'
            #return self.multimedia(text)
        elif similarity == 'crowdsourcing':
            #TODO: implement crowdsourcing
            return 'crowdsourcing'
            #return self.crowdsourcing(text)
        elif similarity == 'embedding':
            #TODO: implement embedding
            return 'embedding'
            #return self.embedding(text)
        else:
            return "unknown"

    def factual_query(self, text: str) -> str:
        """
        Returns the answer to a factual question
        """
        brain = Brain(self.graph, self.ent2lbl, text)
        pred = brain.pred
        entities = brain.entities
        intent = brain.movie_intent
        classification = brain.ent_classifier(entities)
        match = brain.ent_matcher(entities)
        sparql = SPARQL(self.graph, self.ent2lbl, self.lbl2ent, self.rel2lbl, self.WDT, self.WD)
        answer = sparql.get_answer((pred, entities, intent, classification, match))
        return answer

if __name__ == '__main__':
    #ent = {'title': 'The Godfather', 'actor': 'Al Pacino'}
    movie_agent = MovieAgent()
    text = "Hello, was Al Pacino in The Godfather"
    text1 = "hi, please tell me if al pacino was in the godfather"
    text2 = "Hi, given that I like movies that Al Pacino starred in, what movies would you recommend?"
    text3 = "Tell me the director of Good Will Hunting"
    input_text = ""
    while input_text != "exit":
        input_text = input('Enter your question: ')
        print(movie_agent.user_wish(input_text))