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

-- This line uses a regex pattern to match school names with zurich in it, 
-- e.g., eth zurich, uni zurich, zurich_university_of_the_arts
-- the fuzzy match pattern can be constructed via FILTER regex(string, pattern, "flags")
-- "i" flag means case-insensitive.
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX aida:<http://aida.kmi.open.ac.uk/ontology#>
PREFIX schema: <http://schema.org/>
SELECT ?paper ?aff_name
FROM <http://aida.kmi.open.ac.uk/resource>
WHERE {
    ?paper schema:creator ?author .
    ?author schema:memberOf ?aff .
  	?aff foaf:name ?aff_name
    FILTER regex(?aff_name, "zurich", "i")
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

-- Count unique affiliations (26048450)
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX aida:<http://aida.kmi.open.ac.uk/ontology#>
PREFIX cso: <http://cso.kmi.open.ac.uk/topics/>
PREFIX schema: <http://schema.org/>
SELECT (COUNT(?aff) as ?count) 
FROM <http://aida.kmi.open.ac.uk/resource>
WHERE {
  	?aff foaf:name ?aff_name  .
}

-- Count unique papers (20850710)
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX aida:<http://aida.kmi.open.ac.uk/ontology#>
PREFIX schema: <http://schema.org/>
PREFIX dc: <http://purl.org/dc/terms/>
SELECT (COUNT(?paper) as ?count) 
FROM <http://aida.kmi.open.ac.uk/resource>
WHERE {
    ?paper dc:title ?title .
}


-- Return paper title given its uri
PREFIX dc: <http://purl.org/dc/terms/>

SELECT ?title
WHERE {
  <http://aida.kmi.open.ac.uk/resource/2885914489> dc:title ?title .
}

-- Return author name given its uri
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?name
WHERE {
  <http://aida.kmi.open.ac.uk/resource/2120300748> foaf:name ?name .
}

-- Return aff name given its uri
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?name
WHERE {
  <http://aida.kmi.open.ac.uk/resource/2990878173> foaf:name ?name .
}
