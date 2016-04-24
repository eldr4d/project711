import parse
import math

from geopy.geocoders import Nominatim
from geopy.distance import vincenty


i3servers = {}
bootstraps = [] #to be triangulated from when adding a node
conn = parse.establish_db_connection()
cur = conn.cursor()

#TODO:
#come up with outlier tolerance
#given a client, find closest server




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
	
	

def add_server(s):
	"""adds an i3 server with coordinates based on triangulation from the bootsrap servers""" 
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
	
	x,y = triangulate(times)
	news = {}
	news['ip'] = s
	news['x'] = x
	news['y'] = y
	i3servers[s] = news
	
	
	
		



primary="195.195.56.2"
secondary="133.16.26.30"
ternary="170.147.45.164"

bootstrap(primary, secondary, ternary)
#print(bootstraps)

add="193.243.229.111"

add_server(add)
	

	
	



















