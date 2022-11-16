import pickle

class ImageQuestion:
    def __init__(self, graph, ent2lbl, lbl2ent, rel2lbl, lbl2rel, WD, WDT):
        self.graph = graph
        self.ent2lbl = ent2lbl
        self.lbl2ent = lbl2ent
        self.rel2lbl = rel2lbl
        self.lbl2rel = lbl2rel
        self.WD = WD
        self.WDT = WDT
        self.images = self.load_images()
        print('ImageQuestion initialized')

    def image_finder(self, entities, relation):
        """
        Find the corresponding image based on the JSON file
        """
        # check for actors and movies in entities
        actors = []
        movies = []
        for ent in entities.keys():      
            if ent == "actor":
                if type(entities[ent]) == list:
                    for a in entities[ent]:
                        actors.append(self.lbl2ent[a])
                else:
                    actors.append(self.lbl2ent[entities[ent]])
            elif ent == "title":
                if type(entities[ent]) == list:
                    for m in entities[ent]:
                        actors.append(self.lbl2ent[m])
                else:
                    movies.append(self.lbl2ent[entities[ent]])
        
        print(actors)
        print(movies)

        

        if len(actors) == 1 and len(movies) == 1:
            actor_rdf = actors[0].split('/')[-1]
            movie_rdf = movies[0].split('/')[-1]
            # SPARQL query to find the actor's IMDB id
            query_template = "SELECT DISTINCT ?x WHERE {{ <{}> <{}> ?x . }}".format(self.WD[actor_rdf], self.lbl2rel["IMDb ID"])
            qres = self.graph.query(query_template)
            actor_id = ""
            for row in qres:
                actor_id = str(row.x)
            # SPARQL query to find the movies IMDB id
            query_template = "SELECT DISTINCT ?x WHERE {{ <{}> <{}> ?x . }}".format(self.WD[movie_rdf], self.lbl2rel["IMDb ID"])
            qres = self.graph.query(query_template)
            movie_id = ""
            for row in qres:
                movie_id = str(row.x)

            # find the image in the JSON file
            for image in self.images:
                if actor_id in image["cast"] and len(image["cast"]) == 1 and movie_id in image["movie"]:
                    image_url = image["img"].replace(".jpg", "")
                    return f"image:{image_url}"
            return None

        elif len(actors) == 1:
            actor_rdf = actors[0].split('/')[-1]
            # SPARQL query to find the actor's IMDB id
            query_template = "SELECT DISTINCT ?x WHERE {{ <{}> <{}> ?x . }}".format(self.WD[actor_rdf], self.lbl2rel["IMDb ID"])
            print(query_template)
            qres = self.graph.query(query_template)
            actor_id = ""
            for row in qres:
                actor_id = str(row.x)

            # find the image in the JSON file
            for image in self.images:
                if actor_id in image["cast"] and len(image["cast"]) == 1:
                    image_url = image["img"].replace(".jpg", "")
                    return f"image:{image_url}"
            return None
        
        elif len(movies) == 1:
            movie_rdf = movies[0].split('/')[-1]
            # SPARQL query to find the actor's IMDB id
            query_template = "SELECT DISTINCT ?x WHERE {{ <{}> <{}> ?x . }}".format(self.WD[movie_rdf], self.lbl2rel["IMDb ID"])
            qres = self.graph.query(query_template)
            movie_id = ""
            for row in qres:
                movie_id = str(row.x)

            # find the image in the JSON file
            for image in self.images:
                if movie_id in image["movie"]:
                    image_url = image["img"].replace(".jpg", "")
                    return f"image:{image_url}"
            return None

        else:
            return "Sorry, not implemented yet"

    def load_images(self):
        with open("data/Multimedia/images.pickle", "rb") as f:
            images = pickle.load(f)
        return images