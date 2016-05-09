import sys
sys.path.insert(0, '../src/')

import json
import parse
import numpy as np
import matplotlib.pyplot as plt

def evaluate_location():
	accuracy = []
	error = []
	with open('test_loc_config.json') as config_file:
		configs = json.load(config_file)

	conn = parse.establish_db_connection()
	cur = conn.cursor()

	cfg = 1
	for config in configs["tests"]:
		clients = config['clients']
		all_servers = config['servers']
		total_num = len(all_servers)

		servers = all_servers[0:3]

		all_servers = all_servers[3:len(all_servers)]
		i = 3
		numbers = []
		accuracy = []
		error = []

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
		accuracy.append(correct / total)
		error.append(e / total)
		numbers.append(i)
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
			accuracy.append(correct / total)
			error.append(e / total)
			numbers.append(i)
			i = i+1

		f1 = plt.figure(cfg)
		p1 = plt.plot(numbers, accuracy)
		plt.setp(p1, linewidth=5, color="g", linestyle='--')
		p2 = plt.plot(numbers, error)
		plt.setp(p2, linewidth=5, color="r", linestyle='--')
		plt.title("Accuracy During Server Addition config: " + str(cfg))
		plt.xlabel("Number of i3 Servers")
		plt.ylabel("Accuracy (Green) / Relative Error (Red)")
		plt.axis([3, total_num, 0, 1])
		plt.show()
		cfg = cfg + 1

evaluate_location()






