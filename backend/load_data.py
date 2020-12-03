import requests
import json
from SPARQLWrapper import SPARQLWrapper, JSON, XML

sparql = SPARQLWrapper("http://3.101.82.158:3030/SER531")


prefix_template = "<http://www.semanticweb.org/swarnalatha/ontologies/2020/10/untitled-ontology-28#{0}>"

clause_template = '''

  {subject} {predicate} {object} .

'''

main_template = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT {var1} {var2} {var3}
WHERE {{ {where_clause} }}

"""

def clean_data(data={}):
	vars = data['head']['vars']
	bindings = data['results']['bindings']

	for binding in bindings:
		for var in vars:
			if var in binding:
				if binding[var]['type'] == 'uri':
					binding[var]['value'] = binding[var]['value'].split('#')[1]
	return data

def get_predicates(data={}):
	predicates = []
	bindings = data['results']['bindings']

	for binding in bindings:
		if "predicate" in binding:
			if binding["predicate"]["type"] == 'uri':
				val = binding["predicate"]['value'].split('#')[1]
				if val != 'type':
					predicates.append(binding["predicate"]['value'].split('#')[1])
	return list(set(predicates))

'''
	result Fuseki endpoint.
'''
def load_data(query):
	sparql.setQuery(query)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	return results

'''
	getting predicates 
'''
def form_query(character, filter="?predicate"):
	prefix_subject = prefix_template.format(character)
	query = main_template.format(where_clause=clause_template.format(subject=prefix_subject, predicate=filter, object="?object"), var1="?subject", var2="?predicate", var3="?object")
	return query


'''
	one character multi filters
'''
def form_query2(character, filters=[], vars=[]):
	where = []
	prefix_subject = prefix_template.format(character)
	for i in range(len(filters)):
		where.append(clause_template.format(subject=prefix_subject,object=vars[i] ,predicate=prefix_template.format(filters[i])))
	query = main_template.format(where_clause=''.join(where),var1=vars[0], var2=vars[1], var3=vars[2] )
	print(query)
	return query