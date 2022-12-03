from Brain.brain import Brain
from Brain.question_types.crowdsourcing import CrowdSource
from Brain.question_types.embeddings import EmbeddingSimilarity
from Brain.question_types.multimedia import ImageQuestion
from Brain.question_types.recommender import MovieRecommender
from Knowledge.graph import KnowledgeGraph
from Query.SPARQL import SPARQL
from utils import question_patterns, question_similarity, question_type, clean_text
from Response.response import natural_response_factual, natural_response_crowd, natural_response_embedding_one, natural_response_embedding_several, natural_response_embedding_recommender, natural_response_negative, natural_response_no_picture, natural_response_recommender, natural_response_unknown

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
        if similarity == 'factual':
            return self.factual_query(text)
        elif similarity == 'recommendation':
            return self.movie_query(text_clean)
        elif similarity == 'multimedia':
            print("That's a tough one, let me think...") # TODO: implement submission to user
            return self.image_query(text_clean)
        else:
            return natural_response_unknown()

    def factual_query(self, text: str) -> str:
        """
        Returns the answer to a factual question
        """
        pos, pred, entities = self.brain.ner(text) # TODO: parse input text
        if entities == {}:
            return natural_response_unknown()
        match = self.brain.ent_matcher(entities)
        intent = self.brain.intent(text, pos, pred) # TODO: clean parsed text to identify intent more easily
        classification = self.brain.ent_classifier(entities) # TODO: is ent_classifier necessary?
        sparql = SPARQL(self.graph, self.ent2lbl, self.lbl2ent, self.rel2lbl, self.WDT, self.WD)
        crowd = self.crowdsourcing.ask_crowd(match, intent)
        emb_answer = self.embedding_sim.most_similar(match, intent, 10) # TODO: several matches?
        for e in emb_answer:
            if e in match.values():
                emb_answer.remove(e)
        if crowd != ('None', 'None', 'None'):
            answer = sparql.get_crowd_answer((pred, entities, intent, classification, match, crowd)) # TODO: answer formatter
            if answer == 'unknown':
                if emb_answer[0] == 'Not found':
                    return natural_response_negative()
                return natural_response_embedding_several((self.ent2lbl[self.WDT[intent.split('/')[-1]]], list(match.values())[0], emb_answer[0], emb_answer[1], emb_answer[2]))
            return natural_response_crowd(answer)
        answer = sparql.get_factual_answer((pred, entities, intent, classification, match)) # TODO: answer formatter
        if answer == 'unknown':
            return natural_response_embedding_several((self.ent2lbl[self.WDT[intent.split('/')[-1]]], list(match.values())[0], emb_answer[0], emb_answer[1], emb_answer[2]))
        for e in emb_answer:
            if e == 'Not found':
                return natural_response_factual(answer)
            elif e == answer[2]:
                emb_answer.remove(e)
        return natural_response_factual(answer) + " " + "However, " + natural_response_embedding_one(emb_answer[0])

    def image_query(self, text: str) -> str:
        """
        Returns the answer to an image question
        """
        pos, pred, entities = self.brain.ner(text)
        if entities == {}:
            return natural_response_unknown()
        match = self.brain.ent_matcher(entities)
        intent = self.brain.intent(text, pos, pred) # TODO: clean parsed text to identify intent more easily
        classification = self.brain.ent_classifier(entities)
        answer = self.multimedia.image_finder(match, intent)
        if answer != "not found":
            return answer
        else:
            return natural_response_no_picture()

    def movie_query(self, text: str) -> str:
        """
        Returns the answer to a recommendation question
        """
        entities = self.brain.recommender_ner(text)
        if entities == {}:
            return natural_response_unknown()
        match = self.brain.ent_matcher(entities)
        # user_sur = str(input("Would you like to be surprised (y/n)? ")).strip()
        # if user_sur == 'y':
        #     surprise = True # TODO: based on user interaction, active learning?
        # else: surprise = False
        if 'title' in match.keys():
            rec = self.recommender.recommend_movie(match)
            if rec != 'Movie not in database':
                rec_unique = []
                for r in rec:
                    if r['title'] not in match['title'] and r['title'] not in rec_unique:
                        rec_unique.append(r)
                # movie with highest rating
                rec_rating = sorted(rec_unique, key=lambda k: k['rating'], reverse=True)
                return natural_response_recommender((rec_unique[0]['title'], rec_unique[1]['title'], rec_unique[2]['title'], int(rec_rating[0]['nr_voters']), rec_rating[0]['title'], rec_rating[0]['rating']))
            else:
                rec = self.embedding_sim.most_similar_recommendation(match['title'], topn=10) # option to fallback on embedding similarity
                # remove movies from rec that are in match and those that are not unique
                rec_unique = []
                for r in rec:
                    if r not in match['title'] and r not in rec_unique:
                        rec_unique.append(r)
                return natural_response_embedding_recommender((rec_unique[0], rec_unique[1], rec_unique[2]))
        return natural_response_unknown()

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