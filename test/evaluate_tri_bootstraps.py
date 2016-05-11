
import sys
sys.path.insert(0, '../src/')
import triangulate as tri
import json
import parse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def evaluate_bootstraps():


	with open('test_bootstraps.json') as config_file:
		configs = json.load(config_file)


	preaccuracy = 0.0
	preerror = 0.0
	
	postaccuracy = 0.0
	posterror = 0.0
	
	for config in configs["tests"]:
		t = tri.TriangulationNet()
		clients = config['clients']
		servers = config['servers']
		t.bootstrap(servers[0], servers[1], servers[2])
		
		for c in clients:
			print "Client: " + c
			t.add_client(c)
		a, e = t.calculate_accuracy()
		
		
		preaccuracy = preaccuracy + a
		preerror = preerror + e

		
		t.add_server(servers[3])
		t.add_server(servers[4])
		t.add_server(servers[5])
		
		t.remove_server(servers[0])
		t.remove_server(servers[1])
		t.remove_server(servers[2])
		
		
		a, e = t.calculate_accuracy()
		
		postaccuracy = postaccuracy + a
		posterror = posterror + e
	
	
	numconfigs = len(configs["tests"])
	
	preaccuracy = preaccuracy / numconfigs
	preerror = preerror / numconfigs
	
	postaccuracy = postaccuracy / numconfigs
	posterror = posterror / numconfigs
	
	print("Preaccuracy: "+str(preaccuracy)+", Preerror: "+str(preerror))
	print("Postaccuracy: "+str(postaccuracy)+", Posterror: "+str(posterror))
		
evaluate_bootstraps()
