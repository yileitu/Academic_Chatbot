class SPARQL:
    def __init__(self, graph, ent2lbl, lbl2ent, rel2lbl, WDT, WD):
        self.graph = graph
        self.ent2lbl = ent2lbl
        self.lbl2ent = lbl2ent
        self.rel2lbl = rel2lbl
        self.WDT = WDT
        self.WD = WD
        print("SPARQL initialized")

    def get_factual_answer(self, result: tuple):
        """
        SPARQL query to get a factual answer from the Knowledge Graph
        """
        try:
            pred, entities, intent, classification, match = result
            for val in match.values():
                ent = self.lbl2ent[val]
            print(ent)
            query_template = "SELECT DISTINCT ?x ?y WHERE {{ <{}> <{}> ?x . }}".format(ent, intent)
            print("--- sparql query: {}".format(query_template))
            qres = self.graph.query(query_template)
            answer = ""
            for row in qres:
                if row.x in self.ent2lbl.keys():
                    print(self.ent2lbl[row.x])
                    answer = self.ent2lbl[row.x]
                else:
                    print(str(row.x))
                    answer = str(row.x)
            # if no answer is found, try to find a similar answer from embeddings
            if answer == "":
                return 'None'
            # parse intent to only keep the last part of the URI
            intent_uri = intent.split('/')[-1]
            # intent to wikidata property
            answer_template = f"Hi, the {self.rel2lbl[self.WDT[intent_uri]]} of {self.ent2lbl[ent]} is {answer}."
            return "\n{}".format(answer_template)
        except:
            return "Sorry, I don't know the answer to that question."
        
    def get_crowd_answer(self, result: tuple):
        """
        SPARQL query to get a factual answer from the Knowledge Graph
        """
        try:
            pred, entities, intent, classification, match, crowd = result
            for val in match.values():
                ent = self.lbl2ent[val]
            print(ent)
            query_template = "SELECT DISTINCT ?x ?y WHERE {{ <{}> <{}> ?x . }}".format(ent, intent)
            print("--- sparql query: {}".format(query_template))
            qres = self.graph.query(query_template)
            answer = ""
            for row in qres:
                if row.x in self.ent2lbl.keys():
                    print(self.ent2lbl[row.x])
                    answer = self.ent2lbl[row.x]
                else:
                    print(str(row.x))
                    answer = str(row.x)
            # if no answer is found, try to find a similar answer from embeddings
            if answer == "":
                return 'None'
            # intent to wikidata property
            answer_template = f"According to the crowd, with an inter-rate agreement of {crowd[0]} and a support of {int(crowd[1])} out of 3 votes, the answer is {answer}."
            return "\n{}".format(answer_template)
        except:
            return "Sorry, I don't know the answer to that question."