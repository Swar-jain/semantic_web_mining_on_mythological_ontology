from flask import Flask
import load_data
from flask import request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
	print(request.get_json())
	# response.headers['Access-Control-Allow-Origin'] = '*'
	# response.data= {'head': {'vars': ['object1', 'object2', 'object3']}, 'results': {'bindings': [{'object1': {'type': 'uri', 'value': 'http://www.semanticweb.org/swarnalatha/ontologies/2020/10/untitled-ontology-28#Cronus'}, 'object2': {'type': 'uri', 'value': 'http://www.semanticweb.org/swarnalatha/ontologies/2020/10/untitled-ontology-28#Rhea'}}]}}
	return "something"

@app.route('/dropdown/')
def show_dropdown_list():
	response = {'result': []}
	result = []
	data = request.get_json()
	if data:
		query = load_data.form_query(data["characters"][0])
		data = load_data.load_data(query)
		result = load_data.get_predicates(data)
	if result:
		response['result'] = result
	return response


@app.route('/process/', methods=["POST"])
def process():
    req = request.get_json()
    print(req)
    # response.headers['Access-Control-Allow-Origin'] = '*'
    # response.content_type = "application/json"
    # response.data = req
    return req



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