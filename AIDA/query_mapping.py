from SPARQLWrapper import SPARQLWrapper, JSON

def map_query_to_sparql(full_query, entity, category):
    """
    Maps the user query to one of the predefined SPARQL query templates based on the full query, entity, and category.
    """
    sparql_prefix = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX dc: <http://purl.org/dc/terms/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX aida: <http://aida.kmi.open.ac.uk/ontology#>
    FROM <http://aida.kmi.open.ac.uk/resource>
    """

    query = ""
    if "similar to" in full_query or "like" in full_query:
        if category == 'Paper':
            query = f"{sparql_prefix}SELECT ?paperUri WHERE {{ ?paperUri rdf:type aida:paper . ?paperUri dc:title \"{entity}\" . }}"
        elif category == 'Author':
            query = f"{sparql_prefix}SELECT ?authorUri WHERE {{ ?authorUri rdf:type aida:author . ?authorUri foaf:name \"{entity}\" . }}"
    elif "cited" in full_query or "publications by" in full_query:
        query = f"{sparql_prefix}SELECT ?authorUri WHERE {{ ?authorUri rdf:type aida:author . ?authorUri foaf:name \"{entity}\" . }}"
    elif "belonging to" in full_query or "from" in full_query or "in" in full_query:
        query = f"{sparql_prefix}SELECT ?institutionUri WHERE {{ ?institutionUri rdf:type aida:affiliation . ?institutionUri rdfs:label \"{entity}\" . }}"

    if not query:
        query = "Unable to determine the appropriate template based on the provided query."
    return query

def execute_sparql_query(sparql_query):
    """
    Executes a SPARQL query against the AIDA SPARQL endpoint and returns the results.
    """
    sparql_endpoint = "https://aida.kmi.open.ac.uk/sparql/"
    sparql = SPARQLWrapper(sparql_endpoint)
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)

    try:
        response = sparql.query().convert()
        ids = [result[list(result.keys())[0]]["value"] for result in response["results"]["bindings"]]
        return ids
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Example usage
example_queries = [
    ("Find papers similar to 'Quantum Computing'", "Quantum Computing", "Paper"),
    ("Who are authors like 'John Doe'?", "John Doe", "Author"),
    ("List publications from 'MIT'", "MIT", "Institution")
]

for full_query, entity, category in example_queries:
    sparql_query = map_query_to_sparql(full_query, entity, category)
    result_ids = execute_sparql_query(sparql_query)
    print(f"Query: {full_query}\nSPARQL Query: {sparql_query}\nResult IDs: {result_ids}\n")
