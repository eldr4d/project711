import sys
sys.path.insert(0, '../src/')

import json
import DNS as dns
from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def evaluate_triangulate():

  pp = PdfPages('accuracy_dns.pdf')

  with open('test_dns_config.json') as config_file:
    configs = json.load(config_file)

  cfg = 1
  for config in configs["tests"]:
    accuracy = []
    error = []
    numbers = []
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
