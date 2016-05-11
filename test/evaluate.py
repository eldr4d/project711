import sys
sys.path.insert(0, '../src/')

import parse
import json
import triangulate as tri
from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from scipy.stats import geom


def evaluate_location():
	

	with open('test_loc_config.json') as config_file:
		configs = json.load(config_file)

	conn = parse.establish_db_connection()
	cur = conn.cursor()

	accuracy = [0]*(len(configs["tests"][0]["servers"])-2)
	error = [0]*(len(configs["tests"][0]["servers"])-2)
	for config in configs["tests"]:
		clients = config['clients']
		all_servers = config['servers']
		total_num = len(all_servers)

		servers = all_servers[0:3]

		all_servers = all_servers[3:len(all_servers)]
		i = 0


		correct = 0.0
		e = 0.0
		total = 0.0

		for client in clients:
			dist_min = parse.get_closest_geo_from_subset(client, servers, cur)
			actual_min = parse.get_actual_closest_from_subset(client, servers, cur)
			if dist_min != None and actual_min != None:
				total = total + 1
			else:
				continue

			if dist_min[1] == actual_min[1]:
				correct = correct + 1
			else:
				e = e + (float(dist_min[3]) - float(actual_min[2])) / float(dist_min[3])
		accuracy[i] = accuracy[i] + (correct / total)
		error[i] = error[i] + (e / total)
		
		i = i + 1


		for server in all_servers:
			servers.append(server)
			correct = 0.0
			e = 0.0
			total = 0.0

			for client in clients:
				dist_min = parse.get_closest_geo_from_subset(client, servers, cur)
				actual_min = parse.get_actual_closest_from_subset(client, servers, cur)
				if dist_min != None and actual_min != None:
					total = total + 1
				else:
					continue

				if dist_min[1] == actual_min[1]:
					correct = correct + 1
				else:
					e = e + (float(dist_min[3]) - float(actual_min[2])) / float(dist_min[3])
			accuracy[i] = accuracy[i] + (correct / total)
			error[i] = error[i] + (e / total)
			i = i+1

		
	
	numbers = range(3, len(accuracy)+3)
	accuracy = [a / len(configs["tests"]) for a in accuracy]
	error = [e / len(configs["tests"]) for e in error]
	
	f1 = plt.figure(1)
	p1 = plt.plot(numbers, accuracy)
	plt.setp(p1, linewidth=1, color="g")
	p2 = plt.plot(numbers, error)
	plt.setp(p2, linewidth=1, color="r")
	plt.title("Average Zipcode Performance")
	plt.xlabel("Number of i3 Servers")
	plt.ylabel("Accuracy (Green) / Relative Error (Red)")
	plt.axis([3, total_num, 0, 1])
	# plt.show()
	plt.savefig("Average_Zipcode_Performance.png")
	
	
	
	az = np.polyfit(numbers, accuracy, 3)
	af = np.poly1d(az)
	density = af(numbers)

	
	ez = np.polyfit(numbers, error, 3)
	ef = np.poly1d(ez)
	e_density = ef(numbers)
	
	f1 = plt.figure(2)
	p1 = plt.scatter(numbers, accuracy)
	plt.setp(p1, linewidth=1, color="g")
	p2 = plt.plot(numbers, density)
	plt.setp(p2, linewidth=1, color="k")
	plt.title("Average Zipcode Accuracy")
	plt.xlabel("Number of i3 Servers")
	plt.ylabel("Observed Accuracy (Green) / Fitted Accuracy (Black)")
	plt.axis([3, len(accuracy)+3, 0, 1])
	# plt.show()
	plt.savefig("Average_Zipcode_Accuracy.png")
	
	f1 = plt.figure(3)
	p1 = plt.scatter(numbers, error)
	plt.setp(p1, linewidth=1, color="r")
	p2 = plt.plot(numbers, e_density)
	plt.setp(p2, linewidth=1, color="k")
	plt.title("Average Zipcode Error")
	plt.xlabel("Number of i3 Servers")
	plt.ylabel("Observed Error (Red) / Fitted Error (Black)")
	plt.axis([3, len(accuracy)+3, 0, 1])
	# plt.show()
	plt.savefig("Average_Zipcode_Error.png")

	return numbers, density, e_density


def evaluate_triangulate():


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
	
	f1 = plt.figure(4)
	p1 = plt.plot(numbers, accuracy)
	plt.setp(p1, linewidth=1, color="g")
	p2 = plt.plot(numbers, error)
	plt.setp(p2, linewidth=1, color="r")
	plt.title("Average Triangulation Performance")
	plt.xlabel("Number of i3 Servers")
	plt.ylabel("Accuracy (Green) / Relative Error (Red)")
	plt.axis([3, total_num, 0, 1])
	# plt.show()
	plt.savefig("Average_Triangulation_Performance.png")
	
	az = np.polyfit(numbers, accuracy, 3)
	af = np.poly1d(az)
	density = af(numbers)

	
	ez = np.polyfit(numbers, error, 3)
	ef = np.poly1d(ez)
	e_density = ef(numbers)
	
	
	
	
	f1 = plt.figure(5)
	p1 = plt.scatter(numbers, accuracy)
	plt.setp(p1, linewidth=1, color="g")
	p2 = plt.plot(numbers, density)
	plt.setp(p2, linewidth=1, color="k")
	plt.title("Average Triangulation Accuracy")
	plt.xlabel("Number of i3 Servers")
	plt.ylabel("Observed Accuracy (Green) / Fitted Accuracy (Black)")
	plt.axis([3, len(accuracy)+3, 0, 1])
	# plt.show()
	plt.savefig("Average_Triangulation_Accuracy.png")
	
	f1 = plt.figure(6)
	p1 = plt.scatter(numbers, error)
	plt.setp(p1, linewidth=1, color="r")
	p2 = plt.plot(numbers, e_density)
	plt.setp(p2, linewidth=1, color="k")
	plt.title("Average Triangulation Error")
	plt.xlabel("Number of i3 Servers")
	plt.ylabel("Observed Error (Red) / Fitted Error (Black)")
	plt.axis([3, len(accuracy)+3, 0, 1])
	# plt.show()
	plt.savefig("Average_Triangulation_Error.png")
	
	
	return numbers, density, e_density
	
	

pp = PdfPages('evaluate.pdf')
numbers, loca, loce = evaluate_location()
numbers, tria, trie = evaluate_triangulate()


f1 = plt.figure(7)
p1 = plt.plot(numbers, loca)
plt.setp(p1, linewidth=1, color="b")
p2 = plt.plot(numbers, tria)
plt.setp(p2, linewidth=1, color="r")
plt.title("Average Protocol Accuracy")
plt.xlabel("Number of i3 Servers")
plt.ylabel("Accuracy")
plt.axis([numbers[0], numbers[len(numbers)-1], 0, 1])
# plt.show()
plt.savefig("Average_Protocol_Accuracy.png")


f1 = plt.figure(8)
p1 = plt.plot(numbers, loce)
plt.setp(p1, linewidth=1, color="b")
p2 = plt.plot(numbers, trie)
plt.setp(p2, linewidth=1, color="r")
plt.title("Average Protocol Error")
plt.xlabel("Number of i3 Servers")
plt.ylabel("Relative Error")
plt.axis([numbers[0], numbers[len(numbers)-1], 0, 1])
# plt.show()
plt.savefig("Average_Protocol_Error.png")

#plt.show()
pp.close()


"""total_a = sum(accuracy)
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
		e_density[i-3] = (1-((1-p)**(i-2)))"""
