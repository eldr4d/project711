import sys
sys.path.insert(0, '../src/')

import json
import triangulate as tri
from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def evaluate_triangulate():

	pp = PdfPages('accuracy_tri.pdf')

	with open('test_tri_config.json') as config_file:
		configs = json.load(config_file)

	cfg = 1
	for config in configs["tests"]:
		accuracy = []
		error = []

		t = tri.TriangulationNet()
		clients = config['clients']
		servers = config['servers']
		t.bootstrap(servers[0], servers[1], servers[2])
		total_num = len(servers)
		i = 3
		numbers = []
		for c in clients:
			print "Client: " + c
			t.add_client(c)
		a, e = t.calculate_accuracy()
		accuracy.append(a)
		error.append(e)
		numbers.append(i)

		servers = servers[3:len(servers)]

		for s in servers:
			print "Server: " + s
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
		plt.title("Accuracy During Server Addition Config: " + str(cfg))
		plt.xlabel("Number of i3 Servers")
		plt.ylabel("Accuracy (Green) / Relative Error (Red)")
		plt.axis([3, total_num, 0, 1])
		# plt.show()
		plt.savefig(pp, format='pdf')

		cfg = cfg + 1

	pp.close()



evaluate_triangulate()
