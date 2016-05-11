import json
import parse
import triangulate as tri
import itertools
import copy
import DNS_triangulation as DNS_tri


class DNS:
  def __init__(self, DNS_list, Top_k):
    self.dns_list = DNS_list
    self.DNS_configurations = {}
    self.mapping_top_5_to_used = {}
    self.servers_list = []
    self.clients_conf = {}
    self.top_k = Top_k

    conn = parse.establish_db_connection()
    self.cursor = conn.cursor()

  def add_client(self, client):
    top_5_DNS_edges = parse.get_top_N_nodes(client, self.dns_list, 5, self.cursor)
    top_5_DNS = [top_5_DNS_edges[0].dest,
                 top_5_DNS_edges[1].dest,
                 top_5_DNS_edges[2].dest,
                 top_5_DNS_edges[3].dest,
                 top_5_DNS_edges[4].dest]

    if(str(top_5_DNS) not in self.mapping_top_5_to_used):
      # print "Mpika: " + str(top_5_DNS)
      # print "Mpika: " + str(self.mapping_top_5_to_used.keys())
      dns_conf = DNS_tri.DNS_triangulation(top_5_DNS,
                                   self.cursor,
                                   self.servers_list,
                                   self.top_k)
      dns_key = copy.deepcopy(dns_conf.dns)
      dns_key.sort()
      dns_key = str(dns_key)

      self.mapping_top_5_to_used[str(top_5_DNS)] = dns_key
      if(dns_key not in self.DNS_configurations):
        self.DNS_configurations[dns_key] = dns_conf

    self.clients_conf[client] = self.mapping_top_5_to_used[str(top_5_DNS)]
    self.DNS_configurations[self.clients_conf[client]].add_client(client)
    if(client not in self.DNS_configurations[self.clients_conf[client]].trian.clients):
      print "Error for: " + client


  def add_server(self, server):
    self.servers_list.append(server)
    for key in self.DNS_configurations.iterkeys():
      self.DNS_configurations[key].add_server(server)

  def calculate_accuracy(self):
    """returns the percentage of closest server approximations that were correct"""
    total = 0.0
    correct = 0.0
    error = 0.0
    for client, conf in self.clients_conf.iteritems():

      # print "\n\n--------------" + client + "--------------"
      closest = self.DNS_configurations[conf].get_closest_server_for_client(client)

      true_closest = self.DNS_configurations[conf].get_actual_closest_from_subset(client)
      # print self.DNS_configurations[conf].trian.i3servers
      # print self.DNS_configurations[conf].trian.clients
      # print client + " " + str(closest)
      # print true_closest
      # print "----------------------------"
      # print closest + " " + true_closest[1]
      if closest == true_closest[1]:
        total = total + 1.0
        correct = correct + 1.0
      else:
        e1 = parse.get_edge(client, closest, self.cursor)
        if len(e1) > 0:
          total = total + 1.0
          t1 = e1.time
          e2 = parse.get_edge(client, true_closest[1], self.cursor)
          t2 = e2.time
          error = error + (t1-t2)/t1

    if total == 0.0:
      return 1, 1
    else:
      return (correct / total), (error / total)


# def evaluate_DNS():
#   with open('../test/config2.json') as config_file:
#     configs = json.load(config_file)


#   DNS_list = configs['DNS']
#   Server_list = configs['servers']
#   Client_list = configs['clients']
#   Top_k = int(configs['TOP_K'])
#   conn = parse.establish_db_connection()
#   cur = conn.cursor()

#   dns_prot = DNS(DNS_list, Top_k)

#   for client in Client_list:
#     dns_prot.add_client(client)

#   # for client in Client_list:
#   #   print client
#   #   print dns_prot.DNS_configurations[dns_prot.clients_conf[client]].trian.clients
#   # for client, value in dns_prot.clients_conf.iteritems():
#   #   print client + ": " + value
#   for server in Server_list:
#     dns_prot.add_server(server)

#     print "*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*"
#     print dns_prot.calculate_accuracy()
#     print "*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*"
#     # break
#     # closest = allDNS[str(top_5_DNS)].get_closest_server_for_client(client)
#     # true_closest = allDNS[str(top_5_DNS)].get_actual_closest_from_subset(client)
#     # print '----------- ' + client + ' -------------'
#     # print parse.get_edge(client, closest, cur)
#     # print true_closest
#     # print '-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-'

#   # print DNS.calculate_accuracy()
# evaluate_DNS()