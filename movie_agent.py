from Brain.brain import Brain
from Brain.question_types.embeddings import EmbeddingSimilarity
from Brain.question_types.multimedia import ImageQuestion
from Knowledge.graph import KnowledgeGraph
from Query.SPARQL import SPARQL
from utils import question_patterns, question_similarity, question_type, clean_text

class MovieAgent:
    def __init__(self) -> None:
        KG = KnowledgeGraph()
        self.graph = KG.get_graph()
        self.ent2lbl = KG.ent2lbl
        self.lbl2ent = KG.lbl2ent
        self.rel2lbl = KG.rel2lbl
        self.lbl2rel = {v: k for k, v in self.rel2lbl.items()}
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
        self.brain = Brain(self.graph, self.ent2lbl, self.rel2lbl, self.WDT)
        self.embedding_sim = EmbeddingSimilarity(self.entity_emb, self.relation_emb, 
            self.ent2lbl, self.lbl2ent, self.ent2id, self.id2ent, self.rel2id, self.WD, self.WDT)
        self.multimedia = ImageQuestion(self.graph, self.ent2lbl, self.lbl2ent, self.rel2lbl, self.lbl2rel, self.WD, self.WDT)
        print('Movie agent initialized')

    def user_wish(self, text: str) -> str:
        """
        Returns the answer to the user input
        """
        text_clean = clean_text(text)
        patterns = question_patterns()
        similarity = question_similarity(text, patterns)
        if similarity == 'factual':
            return self.factual_query(text_clean)
        elif similarity == 'recommendation':
            # TODO: implement recommendation
            return 'recommendation'
            #return self.recommendation(text)
        elif similarity == 'multimedia':
            return self.image_query(text_clean)
        elif similarity == 'crowdsourcing':
            #TODO: implement crowdsourcing
            return 'crowdsourcing'
            #return self.crowdsourcing(text)
        elif similarity == 'embedding':
            return self.embedding_query(text_clean)
        else:
            return "unknown"

    def factual_query(self, text: str) -> str:
        """
        Returns the answer to a factual question
        """
        pos, pred, entities = self.brain.ner(text) # TODO: parse input text
        intent = self.brain.intent(text, pos, pred) # TODO: clean parsed text to identify intent more easily
        classification = self.brain.ent_classifier(entities)
        match = self.brain.ent_matcher(entities)
        sparql = SPARQL(self.graph, self.ent2lbl, self.lbl2ent, self.rel2lbl, self.WDT, self.WD)
        answer = sparql.get_answer((pred, entities, intent, classification, match)) # TODO: answer formatter
        return answer

    def embedding_query(self, text: str) -> str:
        """
        Returns the answer to an embedding question
        """
        pos, pred, entities = self.brain.ner(text)
        intent = self.brain.intent(text, pos, pred)
        answer = self.embedding_sim.most_similar(entities, intent, 3)
        return f"The {self.ent2lbl[self.WDT[intent.split('/')[-1]]]} of {list(entities.values())[0]} is {answer}."

    def image_query(self, text: str) -> str:
        """
        Returns the answer to an embedding question
        """
        pos, pred, entities = self.brain.ner(text)
        intent = self.brain.intent(text, pos, pred)
        answer = self.multimedia.image_finder(entities, intent)
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