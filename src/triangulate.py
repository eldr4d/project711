import parse
import math

from geopy.geocoders import Nominatim
from geopy.distance import vincenty


i3servers = {}
clients = {}
bootstraps = [] #to be triangulated from when adding a node
conn = parse.establish_db_connection()
cur = conn.cursor()

#TODO:
#come up with outlier tolerance
#remove client
#remove server
#change bootstraps
#update closest upon server removal/entry




def mean_time(edges):
	"""given a list of Edge objects, return the mean time""" 
	t=0.0
	for e in edges:
		t = t + e.time
	t = t / len(edges)
	return t


def bootstrap(first, second, third):
	"""Set up a cartesian coordinate system from 3 initial servers. the first argument will be at (0,0)"""
	e12 = parse.get_edges(first, second, cur)
	d12 = 0.0
	if len(e12) > 0:
		d12 = mean_time(e12) 	
	else:
		print("ERROR: No edges exist between the first and second nodes")
		return
	
	e13 = parse.get_edges(first, third, cur)
	d13 = 0.0
	if len(e13) > 0:
		d13 = mean_time(e13)
	else:
		print("ERROR: No edges exist between the first and third nodes")
		return
		
	e23 = parse.get_edges(second, third, cur)
	d23 = 0.0
	if len(e23) > 0:
		d23 = mean_time(e23)
	else:
		print("ERROR: No edges exist between the second and third nodes")
		return
	
	
	
	cos1 = (d12*d12 + d13*d13 - d23*d23) / (2*d12*d13)
	theta = math.acos(cos1)
	
	origin = {}
	origin['ip'] = first
	origin['x'] = 0.0
	origin['y'] = 0.0
	
	secondary = {}
	secondary['ip'] = second
	secondary['x'] = d12
	secondary['y'] = 0.0
	
	ternary = {}
	ternary['ip'] = third
	ternary['x']=cos1*d13
	ternary['y']=math.sin(theta)*d13
		
	i3servers[first] = origin
	i3servers[second] = secondary
	i3servers[third] = ternary
	bootstraps.append(origin);
	bootstraps.append(secondary);
	bootstraps.append(ternary);

	


def triangulate(times):
	"""given times to the bootsrap servers, return the coordinates"""
	r1 = times.get(0)
	r2 = times.get(1)
	r3 = times.get(2)
	d = bootstraps[1].get('x')
	i = bootstraps[2].get('x')
	j = bootstraps[2].get('y')
	x = (r1*r1 - r2*r2 + d*d) / (2*d)
	y = (r1*r1 - r3*r3 + i*i +j*j) / (2*j) - (i*x/j)
	return x,y
	
def time_to_bootstraps(s):
	"""returns the times from a given server to the bootstrap servers"""
	times = {}
	
	for idx, val in enumerate(bootstraps):
		edges = parse.get_edges(s, val.get('ip'), cur)
		if len(edges) > 0:
			t = mean_time(edges)
			times[idx] = t
		else:
			print("WARNING: No edges exist between the new server bootstrap" + str(idx))
	if len(times) < 3:
		print("ERROR: Couldn't find 3 or more bootstrapping servers");
		return None
	
	return times
				

def add_server(s):
	"""adds an i3 server with coordinates based on triangulation from the bootsrap servers""" 
	times = time_to_bootstraps(s)
	if times == None:
		return
	x,y = triangulate(times)
	news = {}
	news['ip'] = s
	news['x'] = x
	news['y'] = y
	i3servers[s] = news
	
def distance(x1, y1, x2, y2):
	"""computes the euclidean distance between two coordinates"""
	return math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2))
	
def find_closest_server(x, y):
	"""given a coordinate, returns the ip of the closest i3 server"""
	closest = None
	mindist = 1000000000.0
	for key, value in i3servers.iteritems():
		sx = value.get('x')
		sy = value.get('y')
		#print("("+str(sx)+", "+str(sy)+")")
		dist = distance(x, y, sx, sy)
		if dist < mindist:
			mindist = dist
			closest = key
	
	return closest	

	
def add_client(c):
	"""computes the coordinates of a new client, and the closest server"""
	times = time_to_bootstraps(c)
	if times == None:
		return
	x,y = triangulate(times)
	#print("New client is at ("+str(x)+", "+str(y)+")")
	s = find_closest_server(x, y)
	newc = {}
	newc['ip'] = c
	newc['x'] = x
	newc['y'] = y
	newc['server'] = s
	clients[c] = newc
	#print("Closest server to " + c + " is " + s)

def find_true_closest(client):
	"""given a client, find the server that is actually closest"""
	closest = None
	mindist = 1000000000.0
	for key, value in i3servers.iteritems():
		edges = parse.get_edges(client, key, cur)
		t = mean_time(edges)
		if t < mindist:
			mindist = t
			closest = key
	
	return closest

def update_true_closest(client):
	"""updates the true closest server for a client"""
	(clients.get(client))['true'] = find_true_closest(client)
	

def update_all_true_closest():
	"""updates the true closest values of all the clients"""
	for key, value in clients.iteritems(): 
		update_true_closest(key)

def calculate_accuracy():
	"""returns the percentage of closest server approximations that were correct"""
	total = 0.0
	correct = 0.0
	for key, value in clients.iteritems(): 
		total = total + 1
		if value.get('true') == value.get('server'):
			correct = correct + 1
	
	return correct / total
			
	
	
primary = "195.195.56.2"
secondary = "133.16.26.30"
ternary = "170.147.45.164"

client = "61.114.80.2"

add = "193.243.229.111"

bootstrap(primary, secondary, ternary)

add_server(add)

add_client(client)

update_all_true_closest()

print(calculate_accuracy())




	

	
	



















