import requests
import json
from SPARQLWrapper import SPARQLWrapper, JSON, XML

# sparql = SPARQLWrapper("http://3.101.82.158:3030/SER531")
sparql = SPARQLWrapper("http://dbpedia.org/sparql")


prefix_template = "<http://www.semanticweb.org/swarnalatha/ontologies/2020/10/untitled-ontology-28#{0}>"

prefix2 = 'SER531:{0}'

clause_template = '''

  {subject} {predicate} {object} .

'''

template_3 = '''
	PREFIX dbo: <http://dbpedia.org/ontology/>
	PREFIX dbr: <http://dbpedia.org/resource/>
	PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
	PREFIX foaf: <http://xmlns.com/foaf/0.1/>
	PREFIX dbo: <http://dbpedia.org/ontology/>
	SELECT  ?predicate ?object
	WHERE {{
	 dbr:{subject} ?predicate ?object .
	}}
	

'''

main_template = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT {var1} {var2} {var3}
WHERE {{ {where_clause} }}

"""

template_2 = '''
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX SER531: <http://www.semanticweb.org/swarnalatha/ontologies/2020/10/untitled-ontology-28#> SELECT DISTINCT {object} WHERE {{ {{{where_clause1}}} UNION {{{where_clause2}}} }}
'''

def clean_data(data={}, filters=[]):
	result ={}
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


'''
	two characters one filter
'''
def form_query3(character1,character2, filter, vars):

	subject1 = prefix2.format(character1)
	subject2 = prefix2.format(character2)
	prop1 = prefix2.format(filter)
	clause1 = clause_template.format(subject=vars, predicate=prop1, object=subject1)
	clause2 = clause_template.format(subject=vars, predicate=prop1, object=subject2)
	query = template_2.format(where_clause1=clause1, where_clause2=clause2, object=vars)
	return query

'''
	dbpedia endpoint query
	'''
def form_query4(character):

	subject1 = prefix2.format(character)
	# clause1 = clause_template.format(subject=vars, predicate='?property', object='?object')
	query = template_3.format(subject=subject1)
	return query