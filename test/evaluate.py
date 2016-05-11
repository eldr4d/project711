import sys
sys.path.insert(0, '../src/')

import json
import triangulate as tri
from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from scipy.stats import geom

def evaluate_triangulate():

	pp = PdfPages('accuracy_tri.pdf')

	with open('test_loc_config.json') as config_file:
		configs = json.load(config_file)


	cfg = 1
	accuracy = [0]*(len(configs["tests"][0]["servers"])-2)
	error = [0]*(len(configs["tests"][0]["servers"])-2)
	for config in configs["tests"]:
		t = tri.TriangulationNet()
		clients = config['clients']
		servers = config['servers']
		t.bootstrap(servers[0], servers[1], servers[2])
		total_num = len(servers)
		i = 0
		numbers = []
		for c in clients:
			print "Client: " + c
			t.add_client(c)
		a, e = t.calculate_accuracy()
		
		
		accuracy[i] = accuracy[i] + a
		error[i] = error[i] + e

		servers = servers[3:len(servers)]

		for s in servers:
			print "Server: " + s
			t.add_server(s)
			a, e = t.calculate_accuracy()
			i = i+1
			accuracy[i] = accuracy[i] + a
			error[i] = error[i] + e
		
		cfg = cfg + 1
		

	

	numbers = range(3, len(accuracy)+3)
	accuracy = [a / len(configs["tests"]) for a in accuracy]
	error = [e / len(configs["tests"]) for e in error]
	
	f1 = plt.figure(1)
	p1 = plt.plot(numbers, accuracy)
	plt.setp(p1, linewidth=1, color="g")
	p2 = plt.plot(numbers, error)
	plt.setp(p2, linewidth=1, color="r")
	plt.title("Average Triangulation Accuracy")
	plt.xlabel("Number of i3 Servers")
	plt.ylabel("Accuracy (Green) / Relative Error (Red)")
	plt.axis([3, total_num, 0, 1])
	# plt.show()
	plt.savefig(pp, format='pdf')
	
	
	
	
	total_a = sum(accuracy)
	accuracy = [a / total_a for a in accuracy]
	
	density = np.zeros(48)
	smallest = 1000000000
	best = -1
	possible = np.linspace(.01, .99, 100)
	for p in possible:
		for i in numbers:
			density[i-3] = p*((1-p)**(i-3))
		diff = np.linalg.norm(accuracy - density)
		if diff < smallest:
			smallest = diff
			best = p
	

	p=best
	for i in numbers:
		density[i-3] = total_a*p*((1-p)**(i-3))
	accuracy = [a * total_a for a in accuracy]
	
	print(error)
	
	#total_e = sum(error)
	#error = [e / total_e for e in error]
	
	e_density = np.zeros(48)
	smallest = 1000000000
	best = -1
	possible = np.linspace(.01, .99, 100)
	for p in possible:
		for i in numbers:
			e_density[i-3] = 1-((1-p)**(i-2))
		diff = np.linalg.norm(error - e_density)
		if diff < smallest:
			smallest = diff
			best = p
	

	p=best
	for i in numbers:
		e_density[i-3] = (1-((1-p)**(i-2)))
	#error = [e * total_e for e in error]
	
	
	
	f1 = plt.figure(2)
	p1 = plt.plot(numbers, density)
	plt.setp(p1, linewidth=1, color="g")
	p2 = plt.plot(numbers, e_density)
	plt.setp(p2, linewidth=1, color="r")
	plt.title("Average Triangulation Accuracy")
	plt.xlabel("Number of i3 Servers")
	plt.ylabel("Fitted Accuracy (Green) / Fitted Error (Red)")
	plt.axis([3, len(accuracy)+3, 0, 1])
	# plt.show()
	plt.savefig(pp, format='pdf')
	
	
	
	
	
	pp.close()



evaluate_triangulate()
