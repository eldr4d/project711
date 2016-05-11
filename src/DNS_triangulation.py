import json
import parse
import triangulate as tri
import itertools
import copy

class DNS_triangulation:
  def __init__(self, allDNS, cur, servers, Top_K):
    self.all_dns = allDNS
    self.dns = []
    self.top_k = Top_K
    self.cur = cur
    self.trian = tri.TriangulationNet()

    self.comb = self.generate_permutations()

    self.initialize_triangulation(servers)

  # def __del__(self):
  #   print "I am dying: " + str(self.dns)
  #   print self.trian.clients

  def initialize_triangulation(self, allServers):
    for setup in self.comb:
      self.dns = []

      self.dns.append(self.all_dns[setup[0]])
      self.dns.append(self.all_dns[setup[1]])
      self.dns.append(self.all_dns[setup[2]])
      tri_holds = self.trian.bootstrap(self.dns[0],
                                       self.dns[1],
                                       self.dns[2],
                                       use_bootstraps_as_servers=False)

      if(tri_holds):
        break

    self.servers = set()
    self.all_servers = copy.deepcopy(allServers)

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

  def generate_permutations(self):
    l = list(itertools.permutations(range(5),3))
    ll = set()
    for x in l:
      y = list(x)
      y.sort()
      yy = tuple(y)
      ll.add(yy)
    lll = list(ll)
    lll.sort()
    return lll

  def add_client(self, client):
    self.trian.add_client(client)

  def add_server(self, server):
    old_servers = self.servers
    self.servers = set()

    self.all_servers.append(server)

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

    # new server inside the top ones
    if(server in self.servers):
      for s1 in old_servers:
        self.trian.remove_server(s1)
      for s in self.servers:
        self.trian.add_server(s)

  def __eq__(self, other):
    return self.dns == other.dns

  def __ne__(self, other):
    return not self.__eq__(other)

  def get_closest_server_for_client(self, client):
    # self.trian.add_client(client)
    return self.trian.find_closest_server(client)

  def get_actual_closest_from_subset(self, client):
    return parse.get_actual_closest_from_subset(client, self.all_servers, self.cur)











