# -*- coding: utf-8 -*-
import pickle

SPARQL_URL2TITLE = """
PREFIX dc: <http://purl.org/dc/terms/>

SELECT ?title
WHERE {
  <{url}> dc:title ?title .
}
"""

SPARQL_URL2AUTHOR = """
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?name
WHERE {
  <{url}}> foaf:name ?name .
}
"""

SPARQL_URL2AFF = """
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?name
WHERE {
  <{url}}> foaf:name ?name .
}
"""

# Read pickle file
with open("node2ind.pkl", "rb") as f:
	node2ind = pickle.load(f)

print(node2ind)
