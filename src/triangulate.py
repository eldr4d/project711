import parse
import math
import numpy

from geopy.geocoders import Nominatim
from geopy.distance import vincenty


i3servers = {} #dictionary of all registered servers
clients = {} #dictionary of all registered clients
bootstraps = [] #to be triangulated from when adding a node
conn = parse.establish_db_connection()
cur = conn.cursor()

#TODO:
#come up with outlier tolerance
#run through some tests to determine accuracy


def bootstrap(first, second, third):
	"""Set up a cartesian coordinate system from 3 initial servers. the first argument will be at (0,0)"""
	e12 = parse.get_edges(first, second, cur)
	d12 = 0.0
	if len(e12) > 0:
		d12 = parse.mean_time(e12) 	
	else:
		print("ERROR: No edges exist between the first and second nodes")
		return
	
	e13 = parse.get_edges(first, third, cur)
	d13 = 0.0
	if len(e13) > 0:
		d13 = parse.mean_time(e13)
	else:
		print("ERROR: No edges exist between the first and third nodes")
		return
		
	e23 = parse.get_edges(second, third, cur)
	d23 = 0.0
	if len(e23) > 0:
		d23 = parse.mean_time(e23)
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
	DistA = times.get(0)
	DistB = times.get(1)
	DistC = times.get(2)
	xA = bootstraps[0].get('x')
	yA = bootstraps[0].get('y')
	xB = bootstraps[1].get('x')
	yB = bootstraps[1].get('y')
	xC = bootstraps[2].get('x')
	yC = bootstraps[2].get('y')
	
	P1 = numpy.array([xA, yA])
	P2 = numpy.array([xB, yB])
	P3 = numpy.array([xC, yC])
	
	#from wikipedia
	#transform to get circle 1 at origin
	#transform to get circle 2 on x axis
	ex = (P2 - P1)/(numpy.linalg.norm(P2 - P1))
	i = numpy.dot(ex, P3 - P1)
	ey = (P3 - P1 - i*ex)/(numpy.linalg.norm(P3 - P1 - i*ex))
	ez = numpy.cross(ex,ey)
	d = numpy.linalg.norm(P2 - P1)
	j = numpy.dot(ey, P3 - P1)
	
	#from wikipedia
	#plug and chug using above values
	x = (pow(DistA,2) - pow(DistB,2) + pow(d,2))/(2*d)
	y = ((pow(DistA,2) - pow(DistC,2) + pow(i,2) + pow(j,2))/(2*j)) - ((i/j)*x)
	
	return x,y

def time_to_bootstraps(s):
	"""returns the times from a given server to the bootstrap servers"""
	times = {}
	
	for idx, val in enumerate(bootstraps):
		edges = parse.get_edges(s, val.get('ip'), cur)
		if len(edges) > 0:
			t = parse.mean_time(edges)
			times[idx] = t
		else:
			print("WARNING: No edges exist between the new server bootstrap" + str(idx))
	if len(times) < 3:
		print("ERROR: Couldn't find 3 or more bootstrapping servers");
		return None
	
	return times
				
	
def distance(x1, y1, x2, y2):
	"""computes the euclidean distance between two coordinates"""
	return math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2))

########################################################################

def find_client_coords(c):
	"""given a client, determine its coordinates based on triangulation"""
	times = time_to_bootstraps(c)
	if times == None:
		print("ERROR: Couldn't update client "+c)
		return None, None
	return triangulate(times)
	
def get_client_coords(c):
	"""given a client, return the x, y coordinates that it is currently registered to"""
	return clients.get(c).get('x'), clients.get(c).get('y')

def update_client_coords(c):
	"""given a client, recompute its coordinates and set them"""
	x, y = find_client_coords(c)
	(clients.get(c))['x'] = x
	(clients.get(c))['y'] = y

########################################################################

def find_closest_server(c):
	"""given a client, returns the ip of the closest i3 server"""
	x,y = get_client_coords(c)
	if x==None or y==None:
		print("ERROR: in find_closest_server, client " + c + "was missing coordinates")
		return None
		
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
	
def get_closest_server(c):
	"""given a client ip, returns the server that is currently registered as its closest based on triangulation"""
	return clients.get(c).get('server')

def update_closest_server(c):
	"""given a client, update the closest triangulation based server"""
	s = find_closest_server(c)
	(clients.get(c))['server'] = s
	return s
	
########################################################################

def find_true_closest(client):
	"""given a client, find the server that is actually closest"""
	closest = None
	mindist = 1000000000.0
	for key, value in i3servers.iteritems():
		edges = parse.get_edges(client, key, cur)
		t = parse.mean_time(edges)
		if t < mindist:
			mindist = t
			closest = key
	
	return closest

def get_true_closest(c):
	"""given a client ip, returns the server that is its closest based on measurements"""
	return clients.get(c).get('true')


def update_true_closest(client):
	"""updates the true closest server for a client"""
	s = find_true_closest(client)
	(clients.get(client))['true'] = s
	return s

########################################################################

def update_client(c):
	"""given a client, updates the coordinates, closest server based on triangulation, and the true closest server"""
	update_client_coords(c)
	update_closest_server(c)
	update_true_closest(c)
	

def update_all_clients():
	"""updates the true closest values of all the clients"""
	for key, value in clients.iteritems(): 
		update_client(c)
	
########################################################################

def add_server(s):
	"""adds an i3 server with coordinates based on triangulation from the bootsrap servers""" 
	x,y = find_client_coords(s) #sic. find_client_coords returns coordinates regardless of whether its a client or not
	if x==None or y==None:
		print("ERROR: Couldn't add server " + s)
		return
	news = {}
	news['ip'] = s
	news['x'] = x
	news['y'] = y
	i3servers[s] = news
	#print("New server " + s + " is at ("+str(x)+", "+str(y)+")")

def remove_server(s):
	"""given a server, removes it from the list of servers and bootstraps if applicable. updates any affected clients"""
	delete = None
	#check to see if the server to remove is a bootstrap server
	for b in bootstraps:
		if b.get('ip') == s:
			delete = b
			break
	
	del i3servers[s] 
	
	#the server to remove was a bootstrap server
	if delete != None:
		#remove the server from the list of bootstraps
		added = 0 #a check to make sure that we actually add a new node into the list of bootstraps
		bootstraps.remove(delete)
		for key, value in i3servers.iteritems():
			#add the next i3 server that is not a bootstrap into the list of bootstraps
			if value not in bootstraps:
				bootstraps.append(value)
				added = 1
				break
		if added == 0:
			print("WARNING: A server was removed from the list of bootstraps, but there wasn't another available server to replace it")
	
	#update any clients who had their server set to the server that was removed		
	for key, value in clients.iteritems(): 
		if value.get('server') == s:
			update_client(key)

########################################################################

def add_client(c):
	"""computes the coordinates of a new client, and the closest server"""

	x,y = find_client_coords(c)
	if x==None or y==None:
		print("ERROR: Couldn't add client " + c)
		return
	
	
	newc = {}
	newc['ip'] = c
	newc['x'] = x
	newc['y'] = y

	clients[c] = newc
	s = update_closest_server(c)
	t = update_true_closest(c)
	
	#print("New client " + c + " is at ("+str(x)+", "+str(y)+")")
	#print("Registered server to " + c + " is " + s)
	#print("Closest server to " + c + " is " + t)


def remove_client(c):
	del client[c]

########################################################################

def calculate_accuracy():
	"""returns the percentage of closest server approximations that were correct"""
	total = 0.0
	correct = 0.0
	for key, value in clients.iteritems(): 
		total = total + 1
		if value.get('true') == value.get('server'):
			correct = correct + 1
	
	return correct / total

########################################################################
######################## END LIBRARY BEGIN MAIN ########################
########################################################################

def simple_test():
	"""just a simple test function before i write more extensive tests"""	

	primary = "195.195.56.2"
	secondary = "133.16.26.30"
	ternary = "170.147.45.164"
	client = "61.114.80.2"
	add = "193.243.229.111"
	bootstrap(primary, secondary, ternary)
	add_server(add)
	add_client(client)
	print(clients.get(client))
	remove_server(secondary)
	print(clients.get(client))
	print(calculate_accuracy())

