import sys
sys.path.insert(0, '../src/')

import json
import triangulate as tri
from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt


def evaluate_triangulate():
	accuracy = []
	error = []
	with open('config.json') as config_file:    
		configs = json.load(config_file)
	t = tri.TriangulationNet()
	bootstraps = configs['bootstraps']
	clients = configs['clients']
	servers = configs['servers']
	t.bootstrap(bootstraps[0], bootstraps[1], bootstraps[2])
	i = 3
	numbers = []
	for c in clients:
		t.add_client(c)
	a, e = t.calculate_accuracy()
	accuracy.append(a)
	error.append(e)
	numbers.append(i)
	
	for s in servers:
		t.add_server(s)
		a, e = t.calculate_accuracy()
		accuracy.append(a)
		error.append(e)
		i = i+1
		numbers.append(i)
	
	f1 = plt.figure(1)
	p1 = plt.plot(numbers, accuracy)
	plt.setp(p1, linewidth=5, color="g", linestyle='--')
	p2 = plt.plot(numbers, error)
	plt.setp(p2, linewidth=5, color="r", linestyle='--')
	plt.title("Accuracy During Server Addition")
	plt.xlabel("Number of i3 Servers")
	plt.ylabel("Accuracy (Green) / Relative Error (Red)")
	
	#print(accuracy)
	#print(error)
	accuracy = []
	numbers = []
	error = []

	servers = [bootstraps[0], bootstraps[1], bootstraps[2]] + servers
	
	toremove = servers[:len(servers) - 3]
	
	for s in toremove:
		i=i-1
		numbers.append(i)
		t.remove_server(s)
		a, e = t.calculate_accuracy()
		accuracy.append(a)
		error.append(e)
	
	f2 = plt.figure(2)
	line = plt.plot(numbers, accuracy)
	plt.setp(line, linewidth=5, color="g", linestyle='--')
	line = plt.plot(numbers, error)
	plt.setp(line, linewidth=5, color="r", linestyle='--')
	plt.title("Accuracy During Server Removal")
	plt.xlabel("Number of i3 Servers")
	plt.ylabel("Accuracy (Green) / Relative Error (Red)")
	
	plt.show()
	
	
	
	


evaluate_triangulate()
