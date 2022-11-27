from Brain.brain import Brain
from Brain.question_types.crowdsourcing import CrowdSource
from Brain.question_types.embeddings import EmbeddingSimilarity
from Brain.question_types.multimedia import ImageQuestion
from Brain.question_types.recommender import MovieRecommender
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
        self.lbl2rel = KG.lbl2rel
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
        self.brain = Brain(self.graph, self.ent2lbl, self.rel2lbl, self.WD, self.WDT)
        self.embedding_sim = EmbeddingSimilarity(self.entity_emb, self.relation_emb, 
            self.ent2lbl, self.lbl2ent, self.ent2id, self.id2ent, self.rel2id, self.WD, self.WDT)
        self.multimedia = ImageQuestion(self.graph, self.ent2lbl, self.lbl2ent, self.rel2lbl, self.lbl2rel, self.WD, self.WDT)
        self.recommender = MovieRecommender(self.ent2lbl, self.lbl2ent, self.rel2lbl, self.lbl2rel, self.WD, self.WDT)
        self.crowdsourcing = CrowdSource(self.ent2lbl, self.lbl2ent, self.rel2lbl, self.lbl2rel)
        print('Movie agent initialized')

    def user_wish(self, text: str) -> str:
        """
        Returns the answer to the user input
        """
        text_clean = clean_text(text)
        patterns = question_patterns()
        similarity = question_similarity(text)
        if similarity == 'factual' or similarity == 'crowdsourcing':
            return self.factual_query(text_clean)
        elif similarity == 'recommendation':
            return self.movie_query(text_clean) # TODO: rating based?
        elif similarity == 'multimedia':
            print("That's a tough one, let me think...") # TODO: implement submission to user
            return self.image_query(text_clean)
        # elif similarity == 'crowdsourcing':
        #     return 'crowdsourcing'
        elif similarity == 'embedding':
            return self.embedding_query(text_clean)
        else:
            return "unknown"

    def factual_query(self, text: str) -> str:
        """
        Returns the answer to a factual question
        """
        pos, pred, entities = self.brain.ner(text) # TODO: parse input text
        match = self.brain.ent_matcher(entities)
        intent = self.brain.intent(text, pos, pred) # TODO: clean parsed text to identify intent more easily
        classification = self.brain.ent_classifier(entities) # TODO: is ent_classifier necessary?
        sparql = SPARQL(self.graph, self.ent2lbl, self.lbl2ent, self.rel2lbl, self.WDT, self.WD)
        crowd = self.crowdsourcing.ask_crowd(match, intent)
        if crowd != ('None', 'None', 'None'):
            #return f"With an inter-rate agreement of {crowd[0]} and a support of {int(crowd[1])} out of 3 votes, the answer is {crowd[2]}."
            answer = sparql.get_crowd_answer((pred, entities, intent, classification, match, crowd)) # TODO: answer formatter
            if answer == 'None':
                return "The crowd that answered this question unfortunately did not agree on an answer. Do you want me to try to find an answer on my own?"
            return answer
        answer = sparql.get_factual_answer((pred, entities, intent, classification, match)) # TODO: answer formatter
        if answer == 'None':
            return "Can you please rephrase this question? I don't know the answer."
        return answer

    def embedding_query(self, text: str) -> str:
        """
        Returns the answer to an embedding question
        """
        pos, pred, entities = self.brain.ner(text)
        match = self.brain.ent_matcher(entities)
        intent = self.brain.intent(text, pos, pred) # TODO: clean parsed text to identify intent more easily
        classification = self.brain.ent_classifier(entities)
        answer = self.embedding_sim.most_similar(match, intent, 3) # TODO: several matches?
        return f"The {self.ent2lbl[self.WDT[intent.split('/')[-1]]]} of {match.keys()[0]} is most likely {answer[0]}, {answer[1]} or {answer[2]}."

    def image_query(self, text: str) -> str:
        """
        Returns the answer to an image question
        """
        pos, pred, entities = self.brain.ner(text)
        match = self.brain.ent_matcher(entities)
        intent = self.brain.intent(text, pos, pred) # TODO: clean parsed text to identify intent more easily
        classification = self.brain.ent_classifier(entities)
        answer = self.multimedia.image_finder(match, intent)
        return answer

    def movie_query(self, text: str) -> str:
        """
        Returns the answer to a recommendation question
        """
        pos, pred, entities = self.brain.ner(text)
        match = self.brain.ent_matcher(entities)
        for m in match.keys():
            if m == 'title':
                rec = self.recommender.recommend_movie(match[m])
                if rec != 'Movie not in database':
                    rec_unique = []
                    for r in rec:
                        if r != match[m] and r not in rec_unique:
                            rec_unique.append(r)
                    return f"I would recommend you to watch {rec_unique[0]}, {rec_unique[1]} and {rec_unique[2]}, given that you like {match[m]}."
                else:
                    rec = self.embedding_sim.most_similar(match, topn=10) # option to fallback on embedding similarity
                    # remove movies from rec that are equal to match[m] and those that are not unique
                    rec_unique = []
                    for r in rec:
                        if r != match[m] and r not in rec_unique:
                            rec_unique.append(r)
                    return f"Similar movies to {match[m]} are {rec_unique[0]}, {rec_unique[1]} and {rec_unique[2]}."
        return "No movie found"

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
        try:
            print(movie_agent.user_wish(input_text))
        except Exception as e:
            print(f"Error: {e}")