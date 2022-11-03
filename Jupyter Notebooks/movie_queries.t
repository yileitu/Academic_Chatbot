
# movies as "instance of wd:Film".
PREFIX wdt: <http://www.wikidata.org/prop/direct/> 
PREFIX wd: <http://www.wikidata.org/entity/> 
SELECT ?movie ?lbl WHERE {
    ?movie wdt:P31 wd:Q11424 .
    ?movie rdfs:label ?lbl .
}


# movies as "has an IMDb ID starting with tt".
PREFIX wdt: <http://www.wikidata.org/prop/direct/> 
PREFIX wd: <http://www.wikidata.org/entity/> 
SELECT DISTINCT ?movie ?lbl WHERE {
    ?movie rdfs:label ?lbl .
    ?movie wdt:P345 ?imdb .
    FILTER( STRSTARTS(?imdb, "tt"))
}



# actors as "has wdt:occupation wd:actor".
PREFIX wdt: <http://www.wikidata.org/prop/direct/> 
PREFIX wd: <http://www.wikidata.org/entity/> 
SELECT ?actor ?lbl WHERE {
    ?actor rdfs:label ?lbl .
    ?actor wdt:P106 wd:Q33999 .
}

# actors as "has an IMDb ID starting with nm".
PREFIX wdt: <http://www.wikidata.org/prop/direct/> 
PREFIX wd: <http://www.wikidata.org/entity/> 
SELECT DISTINCT ?actor ?lbl WHERE {
    ?actor rdfs:label ?lbl .
    ?actor wdt:P345 ?imdb .
    FILTER( STRSTARTS(?imdb, "nm"))
}

