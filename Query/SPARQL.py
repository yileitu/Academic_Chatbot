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
            ent = ''
            for val in match.values():
                ent = self.lbl2ent[val]
            print(ent)
            query_template = "SELECT DISTINCT ?x ?y WHERE {{ <{}> <{}> ?x . }}".format(ent, intent)
            print("--- sparql query: {}".format(query_template))
            qres = self.graph.query(query_template)
            answer = []
            for row in qres:
                if row.x in self.ent2lbl.keys():
                    print(self.ent2lbl[row.x])
                    answer.append(self.ent2lbl[row.x])
                else:
                    print(str(row.x))
                    answer.append(str(row.x))
            # if no answer is found, try to find a similar answer from embeddings
            if answer == []:
                return 'unknown'
            # parse intent to only keep the last part of the URI
            intent_uri = intent.split('/')[-1]
            # intent to wikidata property
            return self.rel2lbl[self.WDT[intent_uri]], self.ent2lbl[ent], answer
        except:
            return "unknown"
        
    def get_crowd_answer(self, result: tuple):
        """
        SPARQL query to get a factual answer from the Knowledge Graph
        """
        try:
            pred, entities, intent, classification, match, crowd = result
            ent = ''
            print(match)
            for val in match.values():
                ent = self.lbl2ent[val]
            print(ent)
            query_template = "SELECT DISTINCT ?x ?y WHERE {{ <{}> <{}> ?x . }}".format(ent, intent)
            print("--- sparql query: {}".format(query_template))
            qres = self.graph.query(query_template)
            answer = []
            for row in qres:
                if row.x in self.ent2lbl.keys():
                    print(self.ent2lbl[row.x])
                    answer.append(self.ent2lbl[row.x])
                else:
                    print(str(row.x))
                    answer.append(str(row.x))
            # if no answer is found, try to find a similar answer from embeddings
            if answer == []:
                return "unknown"
            # intent to wikidata property
            return crowd[0], int(crowd[1]), answer
        except:
            return "unknown"