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
	with open('test_tri_config.json') as config_file:
		configs = json.load(config_file)

	cfg = 1
	for config in configs["tests"]:
		t = tri.TriangulationNet()
		clients = config['clients']
		servers = config['servers']
		t.bootstrap(servers[0], servers[1], servers[2])
		total_num = len(servers)
		i = 3
		numbers = []
		for c in clients:
			t.add_client(c)
		a, e = t.calculate_accuracy()
		accuracy.append(a)
		error.append(e)
		numbers.append(i)

		servers = servers[3:len(servers)]

		for s in servers:
			t.add_server(s)
			a, e = t.calculate_accuracy()
			accuracy.append(a)
			error.append(e)
			i = i+1
			numbers.append(i)

		f1 = plt.figure(cfg)
		p1 = plt.plot(numbers, accuracy)
		plt.setp(p1, linewidth=5, color="g", linestyle='--')
		p2 = plt.plot(numbers, error)
		plt.setp(p2, linewidth=5, color="r", linestyle='--')
		plt.title("Accuracy During Server Addition" + str(cfg))
		plt.xlabel("Number of i3 Servers")
		plt.ylabel("Accuracy (Green) / Relative Error (Red)")
		plt.axis([3, total_num, 0, 1])
		plt.show()

		cfg = cfg + 1

		"""
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
		"""



evaluate_triangulate()
