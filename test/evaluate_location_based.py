import sys
sys.path.insert(0, '../src/')

import json
import parse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def evaluate_location():
	pp = PdfPages('accuracy_loc.pdf')

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
	plt.title("Average Zipcode Accuracy")
	plt.xlabel("Number of i3 Servers")
	plt.ylabel("Accuracy (Green) / Relative Error (Red)")
	plt.axis([3, total_num, 0, 1])
	# plt.show()
	plt.savefig(pp, format='pdf')
	
	
	
	az = np.polyfit(numbers, accuracy, 2)
	af = np.poly1d(az)
	density = af(numbers)

	
	ez = np.polyfit(numbers, error, 2)
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
	plt.savefig(pp, format='pdf')
	
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
	plt.savefig(pp, format='pdf')

	pp.close()
	
	return af, ef

evaluate_location()



"""

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
"""


