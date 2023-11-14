class SPARQL:
    def __init__(self, graph, ent2lbl, lbl2ent, rel2lbl, WDT, WD):
        self.graph = graph
        self.ent2lbl = ent2lbl
        self.lbl2ent = lbl2ent
        self.rel2lbl = rel2lbl
        self.WDT = WDT
        self.WD = WD
        print("SPARQL initialized")

    def get_factual_answer(self, result: tuple, check: bool):
        """
        SPARQL query to get a factual answer from the Knowledge Graph
        """
        try:
            pred, entities, intent, match = result
            ents = []
            for val in match.values():
                if type(val) == list:
                    for v in val:
                        ents.append(self.lbl2ent[v])
                else: ents.append(self.lbl2ent[val])
            print(ents)
            # check or not
            if not check:
                ents = [ents[0]]
            elif len(ents) != 2:
                return 'unknown'
            print(ents)
            answer = {}
            for ent in ents:
                answer[ent] = []
                query_template = "SELECT DISTINCT ?x ?y WHERE {{ <{}> <{}> ?x . }}".format(ent, intent)
                print("--- sparql query: {}".format(query_template))
                qres = self.graph.query(query_template)
                for row in qres:
                    if row.x in self.ent2lbl.keys():
                        print(self.ent2lbl[row.x])
                        answer[ent].append(self.ent2lbl[row.x])
                    else:
                        print(str(row.x))
                        answer[ent].append(str(row.x))
            # if no answer is found, try to find a similar answer from embeddings
            a = [a for a in answer.values()]
            if len(a) == 1:
                if a[0] == []:
                    return "unknown"
            else:
                if a[0] == [] and a[1] == []:
                    return "unknown"
            # parse intent to only keep the last part of the URI
            intent_uri = intent.split('/')[-1]
            # intent to wikidata property
            return self.rel2lbl[self.WDT[intent_uri]], self.ent2lbl[ent], answer
        except:
            return "unknown"
        
    def get_crowd_answer(self, result: tuple, check: bool):
        """
        SPARQL query to get a factual answer from the Knowledge Graph
        """
        try:
            pred, entities, intent, match, crowd = result
            ents = []
            for val in match.values():
                if type(val) == list:
                    for v in val:
                        ents.append(self.lbl2ent[v])
                else: ents.append(self.lbl2ent[val])
            # check or not
            if not check:
                ents = [ents[0]]
            elif len(ents) != 2:
                return 'unknown'
            print(ents)
            answer = {}
            for ent in ents:
                answer[ent] = []
                query_template = "SELECT DISTINCT ?x ?y WHERE {{ <{}> <{}> ?x . }}".format(ent, intent)
                print("--- sparql query: {}".format(query_template))
                qres = self.graph.query(query_template)
                for row in qres:
                    if row.x in self.ent2lbl.keys():
                        print(self.ent2lbl[row.x])
                        answer[ent].append(self.ent2lbl[row.x])
                    else:
                        print(str(row.x))
                        answer[ent].append(str(row.x))
            # if no answer is found, try to find a similar answer from embeddings
            a = [a for a in answer.values()]
            if len(a) == 1:
                if a[0] == []:
                    return "unknown"
            else:
                if a[0] == [] and a[1] == []:
                    return "unknown"
            # intent to wikidata property
            return crowd[0], int(crowd[1]), answer
        except:
            return "unknown"

if __name__ == "__main__":
    sparql = SPARQL(None, None, None, None, None, None)
    print(sparql.get_factual_answer(('is', 'Q5', 'P31', 'class', {'title': ['Top Gun']}), True))