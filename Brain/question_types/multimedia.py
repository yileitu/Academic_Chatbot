import pickle
import random

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

    def image_finder(self, entities, relation): # TODO: how to use relation? Introduce time limit?
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

        # query the graph for the corresponding IMDB id
        try:
            image_url = self.query_graph(actors, movies, relation)
        except:
            # show error
            print("Error: Problem with the query")
            image_url = None

        # return the image url if not None
        if image_url != None:
            print("Image URL: {}".format(image_url))
            return f"image:{image_url}"
        else:
            return "Image not found"

    def query_graph(self, actors, movies, relation):
        """
        Query the graph for the find the corresponding IMDB id
        and the image in the JSON file
        """
        # initialize arrays for the actors and movies
        actor_rdfs = []
        movie_rdfs = []
        actor_ids = []
        movie_ids = []
        
        # find actor and movie rdfs and ids
        for actor in actors:
            actor_rdfs.append(actor.split('/')[-1])
        for actor_rdf in actor_rdfs:
            query_template_actor = "SELECT DISTINCT ?x WHERE {{ <{}> <{}> ?x . }}".format(self.WD[actor_rdf], self.lbl2rel["IMDb ID"])
            qres = self.graph.query(query_template_actor)
            for row in qres:
                actor_ids.append(str(row.x))
        for movie in movies:
            movie_rdfs.append(movie.split('/')[-1])
        for movie_rdf in movie_rdfs:
            query_template_movie = "SELECT DISTINCT ?x WHERE {{ <{}> <{}> ?x . }}".format(self.WD[movie_rdf], self.lbl2rel["IMDb ID"])
            qres = self.graph.query(query_template_movie)
            for row in qres:
                movie_ids.append(str(row.x))

        print(actor_ids)
        print(movie_ids)

        # catch if no actors or movies are found
        if len(actor_ids) == 0 and len(movie_ids) == 0:
            return None


        # find the image in the JSON file
        # check if an image is there
        image_url_vague = None
        for image in self.images:
            if self.contains_list(actor_ids, image["cast"]) and self.contains_list(movie_ids, image["movie"]):
                image_url_vague = image["img"].replace(".jpg", "")
                break
        if image_url_vague == None:
            return None

        # while loop to find a random image if there are multiple
        image_url = None
        while image_url == None:
            image = random.choice(self.images)
            # exact match image url
            if self.contains_list(actor_ids, image["cast"]) and len(image["cast"]) == len(actor_ids) and self.contains_list(movie_ids, image["movie"]):
                image_url = image["img"].replace(".jpg", "")
            # return the image url if not None
            if image_url != None:
                return image_url
        # else return the vague image url
        return image_url_vague


    def contains_list(self, list1, list2):
        """
        Check if list1 is contained in list2
        """
        for item in list1:
            if item not in list2:
                return False
        return True

    def load_images(self):
        with open("data/Multimedia/images.pickle", "rb") as f:
            images = pickle.load(f)
        return images