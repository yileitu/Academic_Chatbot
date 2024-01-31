import requests

from entity_recognition.func import NamedEntity, extract_entities

SPARQL_PREFIX = """
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX aida:<http://aida.kmi.open.ac.uk/ontology#>
PREFIX schema: <http://schema.org/>
PREFIX dc: <http://purl.org/dc/terms/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
"""
SPARQL_FROM_SENTENCE = "FROM <http://aida.kmi.open.ac.uk/resource>"


def map_query_to_sparql(full_query: str, entity: str, category: NamedEntity) -> str:
	"""
	Maps the user query to one of the predefined SPARQL query templates based on the full query, entity, and category.
	"""
	query = ""
	entity = entity.lower().strip()
	if "similar to" in full_query or "like" in full_query:
		if category == NamedEntity.paper:
			query = f"{SPARQL_PREFIX}SELECT ?paper ?title {SPARQL_FROM_SENTENCE} WHERE {{ ?title dc:title \"{entity}\" . }}"
		elif category == NamedEntity.author:
			query = f"{SPARQL_PREFIX}SELECT ?authorUri {SPARQL_FROM_SENTENCE} WHERE {{ ?authorUri rdf:type aida:author . ?authorUri foaf:name \"{entity}\" . }}"
	elif "cited" in full_query or "publications by" in full_query:
		query = f"{SPARQL_PREFIX}SELECT ?authorUri {SPARQL_FROM_SENTENCE} WHERE {{ ?authorUri rdf:type aida:author . ?authorUri foaf:name \"{entity}\" . }}"
	elif "belonging to" in full_query or "from" in full_query or "in" in full_query:
		# query = f"{SPARQL_PREFIX}SELECT ?paper {SPARQL_FROM_SENTENCE} WHERE {{?paper schema:creator ?author . ?author schema:memberOf ?aff . ?aff foaf:name \"{entity}\" . }}"
		query = f"{SPARQL_PREFIX}SELECT ?paper {SPARQL_FROM_SENTENCE} WHERE {{?paper schema:creator ?author . ?author schema:memberOf ?aff . ?aff foaf:name ?aff_name FILTER regex(?aff_name, \"{entity}\", \"i\"). }}"

	if not query:
		query = "Unable to determine the appropriate template based on the provided query."
	return query


def execute_sparql_query(sparql_query):
	"""
	Executes a SPARQL query against the AIDA SPARQL endpoint and returns the results.
	"""
	sparql_endpoint = "https://aida.kmi.open.ac.uk/sparqlendpoint"
	headers = {"Accept": "application/sparql-results+json"}  # Headers to request JSON response
	response = requests.get(sparql_endpoint, headers=headers, params={"query": sparql_query}) # Make the HTTP GET request

	# Check if the request was successful
	if response.status_code == 200:
		# Parse the JSON result
		data = response.json()
		ids = [result[list(result.keys())[0]]["value"] for result in data["results"]["bindings"]]
		return ids
	else:
		print(f"An error occurred: {response.status_code}")
		print(response.text)
		return []


if __name__ == "__main__":
	# Example usage
	# example_queries = [
	# 	("Find papers similar to 'Attention is all you need'", "Attention is all you need", "PAPER"),
	# 	("Who are authors like 'Ashish Vaswani'?", "Ashish Vaswani", "AUTHOR"),
	# 	("List publications from 'MIT'", "MIT", "INSTITUTION")
	# 	]
	#
	# for query, entity, cat in example_queries:
	# 	sparql_query = map_query_to_sparql(query, entity, cat)
	# 	result_ids = execute_sparql_query(sparql_query)
	# 	print(f"Query: {query}\nSPARQL Query: {sparql_query}\nResult IDs: {result_ids}\n")

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
