class SPARQL:
    def __init__(self, graph, ent2lbl, lbl2ent, rel2lbl, WDT, WD):
        self.graph = graph
        self.ent2lbl = ent2lbl
        self.lbl2ent = lbl2ent
        self.rel2lbl = rel2lbl
        self.WDT = WDT
        self.WD = WD
        print("SPARQL initialized")

    def get_answer(self, result: tuple):
        """
        SPARQL query to get answer from the Knowledge Graph
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
                print(self.ent2lbl[row.x])
                answer = self.ent2lbl[row.x]
            # parse intent to only keep the last part of the URI
            intent_uri = intent.split('/')[-1]
            # intent to wikidata property
            answer_template = "Hi, the {} of {} is {}.".format(self.rel2lbl[self.WDT[intent_uri]], self.ent2lbl[ent], answer)
            return "\n{}".format(answer_template)
        except:
            return "Sorry, I don't know the answer to that question."