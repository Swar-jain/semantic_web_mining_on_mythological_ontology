from flask import Flask
import load_data
import graph
from flask import request
from flask_cors import CORS
from flask import send_file, send_from_directory, safe_join, abort

app = Flask(__name__)
CORS(app)

app.config["CLIENT_IMAGES"] = "/home/idhant96/projects/semantic_web_mining_on_mythological_ontology/backend/"



@app.route('/')
def hello_world():
	print(request.get_json())
	# response.headers['Access-Control-Allow-Origin'] = '*'
	# response.data= {'head': {'vars': ['object1', 'object2', 'object3']}, 'results': {'bindings': [{'object1': {'type': 'uri', 'value': 'http://www.semanticweb.org/swarnalatha/ontologies/2020/10/untitled-ontology-28#Cronus'}, 'object2': {'type': 'uri', 'value': 'http://www.semanticweb.org/swarnalatha/ontologies/2020/10/untitled-ontology-28#Rhea'}}]}}
	return "something"

@app.route('/dropdown/')
def show_dropdown_list():
	mythology = request.args.get('mythology')
	data = None
	response = {'result': []}
	if mythology == 'Indian' or mythology == 'Greek':
		result = []
		data = request.args.get("character0")
		print(data)
		if data:
			query = load_data.form_query(data)
			data = load_data.load_data(query, "http://3.101.82.158:3030/SER531")
			result = load_data.get_predicates(data)
		if result:
			response['result'] = result

	return response

@app.route('/nofilters/')
def nofilter():
	# response = {'result': []}
	mythology = request.args.get('mythology')
	result = {}
	character = request.args.get("character0")
	if mythology == 'Indian' or mythology == 'Greek':
		if character:
			query = load_data.form_query4(character)
			print(query)
			data = load_data.load_data(query, "http://3.101.82.158:3030/SER531")
			print(data)
			result = load_data.clean_data(data)
		# if result:
		# 	response = result
	elif mythology == "Noted Fictional Characters":
		if character:
			query = load_data.form_query5(character)
			data = load_data.load_data(query, "http://dbpedia.org/sparql")
			result = data

	elif mythology == "Chinese":
		if character:
			query = load_data.form_query4(character)
			print(query)
			data = load_data.load_data(query, "http://54.183.203.151:3030/Chinese")
			result = load_data.clean_data(data)
	return result


@app.route('/getgraph/')
def process():
    character = request.args.get('character0')
    
    query = load_data.form_query4(character)
    data = load_data.load_data(query, "http://3.101.82.158:3030/SER531")
    result = load_data.clean_data(data)
    print(result)
    graph.draw_graph(character, result)
    # return send_from_directory(app.config['CLIENT_IMAGES'],"unix.gv.pdf", as_attachment=True)
    return send_file('/home/idhant96/projects/semantic_web_mining_on_mythological_ontology/backend/unix.gv.pdf', attachment_filename='something.pdf')

@app.route('/singlecharacter/')
def show_result():
	mythology = request.args.get('mythology')
	data = None
	if mythology == 'Indian' or mythology == 'Greek':
		character = request.args.get('character0')
		filters = []
		vars = []
		filters.append(request.args.get('filter0'))
		filters.append(request.args.get('filter1'))
		vars.append(request.args.get('var1'))
		vars.append(request.args.get('var2'))
		vars.append(request.args.get('var3'))
		query = load_data.form_query2(character, filters, vars)
		data = load_data.load_data(query, "http://3.101.82.158:3030/SER531")
		data = load_data.clean_data(data)
	elif mythology == "Noted Fictional Characters":
		character1 = request.args.get('character')
		query = load_data.form_query4(character1)
		data = load_data.load_data(query, "http://dbpedia.org/sparql")
	return data

# @app.route('/multicharacter/')
# def multicharacter():
# 	character1 = request.args.get('character1')
# 	character2 = request.args.get('character2')
# 	# filters = []
# 	# vars = []
# 	filter = request.args.get('filter')
# 	vars = request.args.get('vars')
# 	# filters.append(request.args.get('filter2'))
# 	# vars.append(request.args.get('var1'))
# 	# vars.append(request.args.get('var2'))
# 	# vars.append(request.args.get('var3'))
# 	query = load_data.form_query3(character1, character2, filter, vars)
# 	data = load_data.load_data(query)
# 	data = load_data.clean_data(data)
# 	return data


# @app.route('/dbpedia/')
# def singlecharacter3():
# 	character1 = request.args.get('character')
# 	query = load_data.form_query4(character1)
# 	print(query)
# 	data = load_data.load_data(query)
# 	# data = load_data.clean_data(data)
# 	return data
