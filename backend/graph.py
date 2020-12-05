from graphviz import Graph
from graphviz import Digraph
import json



def draw_graph(character, data):
	u = Digraph('unix', filename='unix.gv',
	            node_attr={'color': 'lightblue2', 'style': 'filled'})
	u.attr(size='6,6')

	predicates = []
	objects = []

	bindings = data['results']['bindings']


	for binding in bindings:
		if "predicate" in binding:
			predicates.append(binding["predicate"]["value"])

		if "object" in binding:
			objects.append(binding["object"]["value"])

	for i in range(len(predicates)):
		u.edge(character, objects[i], label=predicates[i])


	u.render();