import requests
import json
from SPARQLWrapper import SPARQLWrapper, JSON, XML

sparql = SPARQLWrapper("http://18.144.52.83:3030/ser531")

prefix_template = "<http://www.semanticweb.org/swarnalatha/ontologies/2020/10/untitled-ontology-28#{0}>"

main_template = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT ?subject ?predicate ?object
WHERE {{
  {subject} {predicate} ?object .
}}

"""




def load_data(query):
	sparql.setQuery(query)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	print (json.dumps(results))

def form_query(character, filter="?predicate"):
	prefix_str = prefix_template.format(character)
	query = template.format(subject=prefix_str, predicate=filter)
	load_data(query)
	print(query)
	return "somehting"