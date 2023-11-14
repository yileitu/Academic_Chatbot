from Levenshtein import distance as ldist

from Brain.ner.entity_matcher import EntityMatcher
from Brain.ner.entity_recognizer import EntityRecognizer
from Brain.intent.intent_recognition import IntentRecognizer
from Brain.utils import detect_casing, intent_text, load_crf_model


class Brain:
    # initialize brain class
    def __init__(self, graph, ent2lbl, rel2lbl, WD, WDT):
        self.graph = graph
        self.ent2lbl = ent2lbl
        self.rel2lbl = rel2lbl
        self.WD = WD
        self.WDT = WDT
        self.matcher = EntityMatcher(self.graph, self.ent2lbl, self.WD)
        print("Brain initialized")

    # named entity recognition
    def ner(self, text: str) -> tuple:
        """
        Extracts entities from text using a CRF model.
        """
        # entities from entity recognizer
        casing = detect_casing(text)
        crf = load_crf_model(casing)
        movie_ner = EntityRecognizer(crf)
        pos, pred, entities = movie_ner.extract_entities(text)
        if entities == {}:
            if casing == 'uncased':
                crf = load_crf_model('cased')
            elif casing == 'cased':
                crf = load_crf_model('uncased')
            movie_ner = EntityRecognizer(crf)
            pos, pred, entities = movie_ner.extract_entities(text)
        print(entities)
        return pos, pred, entities

    def recommender_ner(self, text: str) -> dict:
        """
        Extracts entities from text using a BERT model.
        """
        rec_ner = EntityRecognizer()
        entities = rec_ner.extract_recommender_entities(text)
        # CRF as fallback
        if entities['title'] == [] and entities['actor'] == []:
            pos, pred, ents = self.ner(text)
            entities = {'title': [], 'actor': []} 
            for key in ents.keys():
                if key in ['title', 'actor']:
                    if type(ents[key]) == list:
                        entities[key] = ents[key]
                    else: 
                        entities[key].append(ents[key])
        print(entities)
        return entities

    # intent recognition
    def intent(self, text: str, pos: list, pred: list) -> str:
        """
        Extracts intent from text using embeddings.
        """
        int_text = intent_text(text, pos, pred)
        recognizer = IntentRecognizer()
        movie_intent = recognizer.extract_intent(int_text)
        if movie_intent[0] != None:
            user_intent = movie_intent[0][0]
        else: user_intent = "No intent found"
        return user_intent

    # find entities in Knowledge Graph
    def ent_matcher(self, entities: dict) -> dict:
        """
        Matches entities to nodes in the Knowledge Graph.
        """
        matcher = self.matcher
        entity = matcher.match(entities)
        return entity


if __name__ == '__main__':
    # test brain
    text = 'Who is the director of Top Gun: Maverick?'
    brain = Brain(text)
    print(text)
    pos, pred, entities = brain.ner(text)