import os

from SPARQLWrapper import JSON, SPARQLWrapper

from entity_recognition.func import NamedEntity, extract_entities

def map_query_to_sparql(full_query: str, entity: str, category: NamedEntity) -> str:
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
		if category == NamedEntity.paper:
			query = f"{sparql_prefix}SELECT ?paperUri WHERE {{ ?paperUri rdf:type aida:paper . ?paperUri dc:title \"{entity}\" . }}"
		elif category == NamedEntity.author:
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


if __name__ == "__main__":
	# Example usage
	example_queries = [
		("Find papers similar to 'Quantum Computing'", "Quantum Computing", "PAPER"),
		("Who are authors like 'John Doe'?", "John Doe", "AUTHOR"),
		("List publications from 'MIT'", "MIT", "INSTITUTION")
		]

	for query, entity, cat in example_queries:
		sparql_query = map_query_to_sparql(query, entity, cat)
		result_ids = execute_sparql_query(sparql_query)
		print(f"Query: {query}\nSPARQL Query: {sparql_query}\nResult IDs: {result_ids}\n")

	example_queries2 = [
		"Find papers similar to Quantum Computing",
		"Who are authors like John Doe?",
		"List publications from MIT",
		]

	for query in example_queries2:
		entities = extract_entities(query)
		for entity, cat in entities:
			sparql_query = map_query_to_sparql(query, entity, cat)
			result_ids = execute_sparql_query(sparql_query)
			print(f"Query: {query}\nSPARQL Query: {sparql_query}\nResult IDs: {result_ids}\n")
