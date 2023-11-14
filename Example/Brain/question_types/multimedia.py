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
        self.actors = self.load_actor_dict()
        self.movies = self.load_movie_dict()
        print('ImageQuestion initialized')

    def image_finder(self, entities):
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
                        movies.append(self.lbl2ent[m])
                else:
                    movies.append(self.lbl2ent[entities[ent]])
        
        print(actors)
        print(movies)        

        # query the graph for the corresponding IMDB id
        try:
            image_url, actor_ids, movie_ids = self.query_graph(actors, movies)
        except:
            # show error
            print("Error: Problem with the query")
            image_url = None

        # return the image url if not None
        if image_url != None:
            print("Image URL: {}".format(image_url))
            # build string with all actors      
            actor_string = ""
            if len(actor_ids) > 0:
                if len(actor_ids) == 1:
                    actor_string = self.ent2lbl[actors[0]] + f" (imdb:{actor_ids[0]})"
                else:
                    for idx, actor in enumerate(actor_ids[:-1]):
                        actor_string += self.ent2lbl[actors[idx]] + f" (imdb:{actor})" + ", "
                    actor_string = actor_string[:-2] + " and " + self.ent2lbl[actors[-1]] + f" (imdb:{actor_ids[-1]})"
            # build string with all movies
            movie_string = ""
            if len(movie_ids) > 0:
                if len(movie_ids) == 1:
                    movie_string = self.ent2lbl[movies[0]] + f" (imdb:{movie_ids[0]})"
                else:
                    for idx, movie in enumerate(movie_ids[:-1]):
                        movie_string += self.ent2lbl[movies[idx]] + f" (imdb:{movie})" + ", "
                    movie_string = movie_string[:-2] + " and " + self.ent2lbl[movies[-1]] + f" (imdb:{movie_ids[-1]})"
            if actor_string != "" and movie_string != "":
                return (actor_string, movie_string, image_url), "both"
            elif actor_string != "":
                return (actor_string, image_url), "actor"
            elif movie_string != "":
                return (movie_string, image_url), "movie"
            return (image_url), "image"
        else:
            return "not found", "image"

    def query_graph(self, actors, movies):
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
        image_url = None
        if len(movie_ids) > 1:
            return None
        elif len(actor_ids) == 0 and len(movie_ids) == 0:
            return None
        # if only actors are found
        elif len(actor_ids) > 0 and len(movie_ids) == 0:
            # find image in actor dict where all actors are in the actor list
            pot_img = None
            for actor_id in actor_ids:
                if actor_id in self.actors:
                    if pot_img == set():
                        return None
                    elif pot_img is None:
                        pot_img = self.actors[actor_id]
                    else:
                        pot_img = set(pot_img).intersection(set(self.actors[actor_id]))
                else:
                    return None
            if pot_img is not None and pot_img != set():
                pot_img_len = [img for img in pot_img if img[1] == str(len(actor_ids))]
                if pot_img_len != []:
                    image = random.choice([img[0] for img in pot_img_len])
                else:
                    image = random.choice([img[0] for img in pot_img])
                image_url = image.replace(".jpg", "")
        # if only movies are found
        elif len(actor_ids) == 0 and len(movie_ids) > 0:
            # find image in movie dict where all movies are in the movie list
            pot_img = None
            for movie_id in movie_ids:
                if movie_id in self.movies:
                    if pot_img == set():
                        return None
                    elif pot_img is None:
                        pot_img = self.movies[movie_id]
                    else:
                        pot_img = set(pot_img).intersection(set(self.movies[movie_id]))
                else:
                    return None
            if pot_img is not None and pot_img != set():
                image = random.choice([img[0] for img in pot_img])
                image_url = image.replace(".jpg", "")
        else:
            # find image in actor and movie dicts where all actors and movies are in the actor and movie list
            pot_img = None
            for movie_id in movie_ids:
                if movie_id in self.movies:
                    if pot_img == set():
                        return None
                    elif pot_img is None:
                        pot_img = self.movies[movie_id]
                    else:
                        pot_img = set(pot_img).intersection(set(self.movies[movie_id]))
                else:
                    return None
            if pot_img is not None and pot_img != set():
                pot_img = set(pot_img).intersection(set(self.actors[actor_ids[0]]))
                for actor_id in actor_ids[1:]:
                    if pot_img == set():
                        return None
                    pot_img = pot_img.intersection(set(self.actors[actor_id]))
                if pot_img is not None and pot_img != set():
                    pot_img_len = [img for img in pot_img if img[1] == str(len(actor_ids))]
                    if pot_img_len != []:
                        image = random.choice([img[0] for img in pot_img_len])
                    else:
                        image = random.choice([img[0] for img in pot_img])
                    image_url = image.replace(".jpg", "")
        # Finally, return the image url
        return image_url, actor_ids, movie_ids

    def contains_list(self, list1, list2):
        """
        Check if list1 is contained in list2
        """
        for item in list1:
            if item not in list2:
                return False
        return True

    def load_actor_dict(self):
        with open("data/Multimedia/actor_dict.pickle", "rb") as f:
            actor_dict = pickle.load(f)
        return actor_dict

    def load_movie_dict(self):
        with open("data/Multimedia/movie_dict.pickle", "rb") as f:
            movie_dict = pickle.load(f)
        return movie_dict


    def load_images(self):
        with open("data/Multimedia/images.pickle", "rb") as f:
            images = pickle.load(f)
        return images

    def create_actor_dict(self):
        """
        Create a dictionary with the actor names as keys and the corresponding
        images as value
        """
        actor_dict = {}
        for image in self.images:
            for actor in image["cast"]:
                if actor not in actor_dict:
                    actor_dict[actor] = []
                actor_dict[actor].append((image["img"], len(image["cast"])))
        # actor_dict to pickle
        with open("data/Multimedia/actor_dict.pickle", "wb") as f:
            pickle.dump(actor_dict, f)
        return actor_dict

    def create_movie_dict(self):
        """
        Create a dictionary with the movie names as keys and the corresponding
        images as value
        """
        movie_dict = {}
        for image in self.images:
            for movie in image["movie"]:
                if movie not in movie_dict:
                    movie_dict[movie] = []
                movie_dict[movie].append((image["img"], len(image["cast"])))
        # movie_dict to pickle
        with open("data/Multimedia/movie_dict.pickle", "wb") as f:
            pickle.dump(movie_dict, f)
        return movie_dict 

if __name__ == "__main__":
    # initialize the class
    image = ImageQuestion(None, None, None, None, None, None, None)
    # load the images
    image.images = image.load_images()
    # create the actor dictionary
    image.create_actor_dict()
    # create the movie dictionary
    image.create_movie_dict()