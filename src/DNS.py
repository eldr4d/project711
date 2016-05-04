import json
import parse
import triangulate as tri

class DNS:
  def __init__(self, DNS_list, servers_list, cursor):
    self.dns_list = DNS_list
    self.servers_list = servers_list
    self.cursor = cursor

class DNS_triangulation:
  def __init__(self, DNS1, DNS2, DNS3, cur, servers, Top_K):
    self.dns = [DNS1, DNS2, DNS3]
    self.dns.sort()
    self.top_k = Top_K
    self.clients = []
    self.cur = cur
    self.trian = tri.TriangulationNet()

    self.initialize_triangulation(servers)

  def initialize_triangulation(self, all_servers):
    print self.dns[0]
    self.trian.bootstrap(self.dns[0], self.dns[1], self.dns[2])

    self.servers = set()
    self.all_servers = all_servers

    top_k_servers_1 = parse.get_top_N_nodes(self.dns[0],
                                            self.all_servers,
                                            self.top_k,
                                            self.cur)
    for s in top_k_servers_1:
      self.servers.add(s.dest)

    top_k_servers_2 = parse.get_top_N_nodes(self.dns[1],
                                            self.all_servers,
                                            self.top_k,
                                            self.cur)
    for s in top_k_servers_2:
      self.servers.add(s.dest)

    top_k_servers_3 = parse.get_top_N_nodes(self.dns[2],
                                            self.all_servers,
                                            self.top_k,
                                            self.cur)
    for s in top_k_servers_3:
      self.servers.add(s.dest)

    for s in self.servers:
      self.trian.add_server(s)

  def __eq__(self, other):
    return self.dns == other.dns

  def __ne__(self, other):
    return not self.__eq__(other)

  def get_closest_server_for_client(self, client):
    self.trian.add_client(client)
    return self.trian.find_closest_server(client)

  def get_actual_closest_from_subset(self, client):
    return parse.get_actual_closest_from_subset(client, self.cur, self.all_servers)

def evaluate_DNS():
  with open('../test/config2.json') as config_file:    
    configs = json.load(config_file)

  DNS_list = configs['DNS']
  Server_list = configs['servers']
  Client_list = configs['clients']
  Top_k = int(configs['TOP_K'])
  conn = parse.establish_db_connection()
  cur = conn.cursor()

  allDNS = {}

  for client in Client_list:
    top_3_DNS_edges = parse.get_top_N_nodes(client, DNS_list, 3, cur)
    top_3_DNS = [top_3_DNS_edges[0].dest, top_3_DNS_edges[1].dest, top_3_DNS_edges[2].dest].sort()
    if(not (top_3_DNS in allDNS)):
      dns_conf = DNS_triangulation(top_3_DNS_edges[0].dest,
                                   top_3_DNS_edges[1].dest,
                                   top_3_DNS_edges[2].dest,
                                   cur,
                                   Server_list,
                                   Top_k)
      allDNS[top_3_DNS] = dns_conf

    closest = allDNS[top_3_DNS].get_closest_server_for_client(client)
    true_closest = allDNS[top_3_DNS].get_actual_closest_from_subset(client)
    print '----------- ' + client + ' -------------'
    print parse.get_edge(client, closest, cur)
    print true_closest
    print '-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-'

evaluate_DNS()








