import sys
sys.path.insert(0, '../src/')

import json
import parse
import numpy as np
# import matplotlib.pyplot as plt

def evaluate_location():
  accuracy = []
  error = []
  with open('config_location.json') as config_file:    
    configs = json.load(config_file)

  clients = configs['clients']
  servers = configs['servers']

  conn = parse.establish_db_connection()
  cur = conn.cursor()
  

  for client in clients:
    dist_min = parse.get_closest_geo_from_subset(client, servers, cur)
    actual_min = parse.get_actual_closest_from_subset(client, servers, cur)
    print "*********************************"
    print ("Client Ip = " + client + "\nClosest Distance\nIp = " + dist_min[1] +
           "\tLatency = " + str(dist_min[3]) + "\tdist = " + str(dist_min[2]) + 
          "\nActual Closest\nIp = " + actual_min[1] + "\tLatency = " +
          str(actual_min[2]) + "\n")
    print "--------------------"
  
  
  


evaluate_location()
