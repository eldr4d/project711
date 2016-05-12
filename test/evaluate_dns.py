import sys
sys.path.insert(0, '../src/')

import json
import DNS as dns
from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def evaluate_DNS():

	
	with open('test_dns_config.json') as config_file:
		configs = json.load(config_file)
	
	cfg = 1
	accuracy = [0]*(len(configs["tests"][0]["servers"]))
	error = [0]*(len(configs["tests"][0]["servers"]))
	cfg = 1
	for config in configs["tests"]:
		print("Config: "+str(cfg))
		cfg = cfg + 1
		i = 0
		
		clients = config['clients']
		servers = config['servers']
		dns_list = config['DNS']
		top_k = int(config['TOP_K'])
		total_num = len(servers)
		
		dns_prot = dns.DNS(dns_list, top_k)
		for client in clients:
			dns_prot.add_client(client)
		
		for server in servers:
			dns_prot.add_server(server)
			a, e = dns_prot.calculate_accuracy()			
			accuracy[i] = accuracy[i] + a
			error[i] = error[i] + e
			i = i+1
			
			
	
	
	
	accuracy = accuracy[2:len(accuracy)]
	error = error[2:len(error)]
	numbers = range(3, len(accuracy)+3)
	print(numbers)
	
	
	accuracy = [a / len(configs["tests"]) for a in accuracy]
	error = [e / len(configs["tests"]) for e in error]
		
	f1 = plt.figure(1)
	p1 = plt.plot(numbers, accuracy)
	plt.setp(p1, linewidth=5, color="g", linestyle='--')
	p2 = plt.plot(numbers, error)
	plt.setp(p2, linewidth=5, color="r", linestyle='--')
	plt.title("Average DNS Performance")
	plt.xlabel("Number of i3 Servers")
	plt.ylabel("Accuracy (Green) / Relative Error (Red)")
	plt.axis([3,  len(accuracy)+3, 0, 1])
	plt.savefig("Average_DNS_Performance.png")	
	
	
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
	plt.title("Average DNS Accuracy")
	plt.xlabel("Number of i3 Servers")
	plt.ylabel("Observed Accuracy (Green) / Fitted Accuracy (Black)")
	plt.axis([3, len(accuracy)+3, 0, 1])
	# plt.show()
	plt.savefig("Average_DNS_Accuracy.png")
	
	f1 = plt.figure(3)
	p1 = plt.scatter(numbers, error)
	plt.setp(p1, linewidth=1, color="r")
	p2 = plt.plot(numbers, e_density)
	plt.setp(p2, linewidth=1, color="k")
	plt.title("Average DNS Error")
	plt.xlabel("Number of i3 Servers")
	plt.ylabel("Observed Error (Red) / Fitted Error (Black)")
	plt.axis([3, len(accuracy)+3, 0, 1])
	# plt.show()
	plt.savefig("Average_DNS_Error.png")
	
	return numbers, density, e_density
	


evaluate_DNS()
