-- The following query returns the papers associated with the topic Semantic Web 
-- and written in collaboration by authors from industry and academia, where those from academia are more than 80%.

PREFIX aida:<http://aida.kmi.open.ac.uk/ontology#>
PREFIX cso: <http://cso.kmi.open.ac.uk/topics/>
PREFIX schema: <http://schema.org/>
SELECT ?paper ?ind (count(?author) as ?nauthor)
FROM <http://aida.kmi.open.ac.uk/resource>
WHERE {
    ?paper aida:hasTopic cso:semantic_web .
    ?paper aida:hasIndustrialSector ?ind .
    ?paper aida:hasPercentageOfAcademia ?x .
    ?paper schema:creator ?author .
    FILTER(?x>80)
}
ORDER BY ?paper


-- Query papers from eth zurich
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX aida:<http://aida.kmi.open.ac.uk/ontology#>
PREFIX schema: <http://schema.org/>
SELECT ?paper 
FROM <http://aida.kmi.open.ac.uk/resource>
WHERE {
    ?paper schema:creator ?author .
    ?author schema:memberOf ?aff .
    ?aff foaf:name "eth_zurich" .
} 

-- Query papers from eth zurich published by andrei vancea
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX aida:<http://aida.kmi.open.ac.uk/ontology#>
PREFIX schema: <http://schema.org/>
SELECT ?paper ?author ?aff
FROM <http://aida.kmi.open.ac.uk/resource>
WHERE {
    ?paper schema:creator ?author .
    ?author schema:memberOf ?aff .
    ?aff foaf:name "eth_zurich" .
    ?author foaf:name "andrei vancea" .
} 

-- Query papers with the title "application independent rendering of scorecard metrics"
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX aida:<http://aida.kmi.open.ac.uk/ontology#>
PREFIX schema: <http://schema.org/>
PREFIX dc: <http://purl.org/dc/terms/>
SELECT ?paper ?title
FROM <http://aida.kmi.open.ac.uk/resource>
WHERE {
    ?title dc:title "application independent rendering of scorecard metrics" .
} 

-- Counts how many papers have been written by authors from an institution such as eth zurich.
PREFIX aida:<http://aida.kmi.open.ac.uk/ontology#>
PREFIX cso: <http://cso.kmi.open.ac.uk/topics/>
PREFIX schema: <http://schema.org/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?author (count(?paper) as ?npaper)
FROM <http://aida.kmi.open.ac.uk/resource>
WHERE {
    ?paper schema:creator ?author .
    ?author schema:memberOf ?aff .
    ?aff foaf:name "eth_zurich" .
}
ORDER BY DESC(?npaper)

-- This line uses a regex pattern to match variations of "eth zurich."
-- The pattern "eth\\s*zurich" is used to match "eth" followed by zero or more spaces (\\s*) and then "zurich." This allows for variations like "ethzurich," "eth zurich," "ETH Zurich," etc., since the "i" in the regex function makes the search case-insensitive.

PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX aida:<http://aida.kmi.open.ac.uk/ontology#>
PREFIX schema: <http://schema.org/>
SELECT ?paper 
FROM <http://aida.kmi.open.ac.uk/resource>
WHERE {
    ?paper schema:creator ?author .
    ?author schema:memberOf ?aff .
    FILTER regex(str(?aff), "eth\\s*zurich", "i") # Added line for fuzzy search
}

-- The following query returns the industrial sectors of all the papers having Semantic Web as a topic.
-- Useful to check the universities are written
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX aida:<http://aida.kmi.open.ac.uk/ontology#>
PREFIX cso: <http://cso.kmi.open.ac.uk/topics/>
PREFIX schema: <http://schema.org/>
SELECT ?aff ?aff_name 
FROM <http://aida.kmi.open.ac.uk/resource>
WHERE {
    ?paper aida:hasTopic cso:semantic_web .
    ?paper schema:creator ?author .
    ?author schema:memberOf ?aff .
    ?aff foaf:name ?aff_name
} GROUP BY ?aff ?aff_name
ORDER BY DESC(?count)
LIMIT 100

-- Distinct affiliations, first 100 observations
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX aida:<http://aida.kmi.open.ac.uk/ontology#>
PREFIX cso: <http://cso.kmi.open.ac.uk/topics/>
PREFIX schema: <http://schema.org/>
SELECT DISTINCT ?aff_name 
FROM <http://aida.kmi.open.ac.uk/resource>
WHERE {
    ?aff foaf:name ?aff_name
} 
LIMIT 100
