from flask import Flask
import load_data
from flask import request

app = Flask(__name__)

@app.route('/')
def hello_world():
	response.headers['Access-Control-Allow-Origin'] = '*'
	response.data= {'head': {'vars': ['object1', 'object2', 'object3']}, 'results': {'bindings': [{'object1': {'type': 'uri', 'value': 'http://www.semanticweb.org/swarnalatha/ontologies/2020/10/untitled-ontology-28#Cronus'}, 'object2': {'type': 'uri', 'value': 'http://www.semanticweb.org/swarnalatha/ontologies/2020/10/untitled-ontology-28#Rhea'}}]}}
	return load_data.clean_data(d)

@app.route('/character/<character>')
def show_dropdown_list(character):
    query = load_data.form_query(character)
    data = load_data.load_data(query)
    data = load_data.clean_data(data)
    return data



    



@app.route('/process/', methods=["POST"])
def process():
    req = request.get_json()
    print(req)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.content_type = "application/json"
    response.data = req
    return response



@app.route('/show/')
def show_result():
	character = request.args.get('character')
	filters = []
	vars = []
	filters.append(request.args.get('filter1'))
	filters.append(request.args.get('filter2'))
	vars.append(request.args.get('var1'))
	vars.append(request.args.get('var2'))
	vars.append(request.args.get('var3'))
	query = load_data.form_query2(character, filters, vars)
	data = load_data.load_data(query)
	data = load_data.clean_data(data)
	return data