import parse
import math
import numpy




"""
The core functionality is defined in bootstrap, and then the following functions are available to call
add_server
add_client
remove_server
remove_client

All of these functions (including bootstrap) take ip addresses in string form as their parameters. 
Additionally, there is a calculate accuracy function that determines what percentage of the server
selection based on triangulation was actually the best possible server

A simple usage is shown at the bottom in the simple_test function

TODO:
Add new bootstraping when bootstrap gets deleted
"""


class TriangulationNet:
	def __init__(self):
		self.i3servers = {} #dictionary of all registered servers
		self.clients = {} #dictionary of all registered self.clients
		self.bootstraps = [] #to be triangulated from when adding a node
		self.conn = parse.establish_db_connection()
		self.cur = self.conn.cursor()


	#this is the function that needs to be called before anything else. it is essentially setup.
	def bootstrap(self, first, second, third):
		"""Set up a cartesian coordinate system from 3 initial servers. the first argument will be at (0,0)"""
		e12 = parse.get_edge(first, second, self.cur)
		d12 = 0.0
		if len(e12) > 0:
			d12 = e12.time
		else:
			print("ERROR: No edges exist between the first and second nodes")
			return

		e13 = parse.get_edge(first, third, self.cur)
		d13 = 0.0
		if len(e13) > 0:
			d13 = e13.time
		else:
			print("ERROR: No edges exist between the first and third nodes")
			return

		e23 = parse.get_edge(second, third, self.cur)
		d23 = 0.0
		if len(e23) > 0:
			d23 = e23.time
		else:
			print("ERROR: No edges exist between the second and third nodes")
			return

		cos1 = (d12*d12 + d13*d13 - d23*d23) / (2*d12*d13)
		if cos1 > 1:
			cos1 = 1
		elif cos1 < -1:
			cos1 = -1

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

		self.i3servers[first] = origin
		self.i3servers[second] = secondary
		self.i3servers[third] = ternary
		self.bootstraps.append(origin);
		self.bootstraps.append(secondary);
		self.bootstraps.append(ternary);


	def triangulate(self, times):
		"""given times to the bootsrap servers, return the coordinates"""
		DistA = times.get(0)
		DistB = times.get(1)
		DistC = times.get(2)
		xA = self.bootstraps[0].get('x')
		yA = self.bootstraps[0].get('y')
		xB = self.bootstraps[1].get('x')
		yB = self.bootstraps[1].get('y')
		xC = self.bootstraps[2].get('x')
		yC = self.bootstraps[2].get('y')

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

	def time_to_bootstraps(self, s):
		"""returns the times from a given server to the bootstrap servers"""
		times = {}

		for idx, val in enumerate(self.bootstraps):
			edge = parse.get_edge(s, val.get('ip'), self.cur)
			if len(edge) > 0:
				times[idx] = edge.time
			else:
				print("WARNING: No edges exist between the new server bootstrap" + str(idx))
		if len(times) < 3:
			print("ERROR: Couldn't find 3 or more bootstrapping servers");
			return None

		return times


	def distance(self, x1, y1, x2, y2):
		"""computes the euclidean distance between two coordinates"""
		return math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2))

########################################################################

	def find_client_coords(self, c):
		"""given a client, determine its coordinates based on triangulation"""
		times = self.time_to_bootstraps(c)
		if times == None:
			print("ERROR: Couldn't update client "+c)
			return None, None
		return self.triangulate(times)

	def get_client_coords(self, c):
		"""given a client, return the x, y coordinates that it is currently registered to"""
		return self.clients.get(c).get('x'), self.clients.get(c).get('y')

	def update_client_coords(self, c):
		"""given a client, recompute its coordinates and set them"""
		x, y = self.find_client_coords(c)
		(self.clients.get(c))['x'] = x
		(self.clients.get(c))['y'] = y

########################################################################

	def find_closest_server(self, c):
		"""given a client, returns the ip of the closest i3 server"""
		x,y = self.get_client_coords(c)
		if x==None or y==None:
			print("ERROR: in find_closest_server, client " + c + "was missing coordinates")
			return None

		closest = None
		mindist = 1000000000.0
		for key, value in self.i3servers.iteritems():
			sx = value.get('x')
			sy = value.get('y')
			#print("("+str(sx)+", "+str(sy)+")")
			dist = self.distance(x, y, sx, sy)
			if dist < mindist:
				mindist = dist
				closest = key

		return closest

	def get_closest_server(self, c):
		"""given a client ip, returns the server that is currently registered as its closest based on triangulation"""
		return self.clients.get(c).get('server')

	def update_closest_server(self, c):
		"""given a client, update the closest triangulation based server"""
		s = self.find_closest_server(c)
		(self.clients.get(c))['server'] = s
		return s

########################################################################

	def find_true_closest(self, client):
		"""given a client, find the server that is actually closest"""
		closest = None
		mindist = 1000000000.0
		for key, value in self.i3servers.iteritems():
			edge = parse.get_edge(client, key, self.cur)
			if len(edge) > 0:
				t = edge.time
				if t < mindist:
					mindist = t
					closest = key

		return closest

	def get_true_closest(self, c):
		"""given a client ip, returns the server that is its closest based on measurements"""
		return self.clients.get(c).get('true')

	def update_true_closest(self, client):
		"""updates the true closest server for a client"""
		s = self.find_true_closest(client)
		(self.clients.get(client))['true'] = s
		return s

########################################################################

	def update_client(self, c):
		"""given a client, updates the coordinates, closest server based on triangulation, and the true closest server"""
		self.update_client_coords(c)
		self.update_closest_server(c)
		self.update_true_closest(c)

	def update_all_clients(self):
		"""updates the true closest values of all the self.clients"""
		for key, value in self.clients.iteritems(): 
			self.update_client(key)

	def update_all_closest(self):
		for key, value in self.clients.iteritems(): 
			self.update_closest_server(key)

	def update_all_true(self):
		for key, value in self.clients.iteritems(): 
			self.update_true_closest(key)

########################################################################

	def add_server(self, s):
		"""adds an i3 server with coordinates based on triangulation from the bootsrap servers""" 
		x,y = self.find_client_coords(s) #sic. find_client_coords returns coordinates regardless of whether its a client or not
		if x==None or y==None:
			print("ERROR: Couldn't add server " + s)
			return
		news = {}
		news['ip'] = s
		news['x'] = x
		news['y'] = y
		self.i3servers[s] = news
		self.update_all_closest()
		#print("New server " + s + " is at ("+str(x)+", "+str(y)+")")

	def remove_server(self, s):
		"""given a server, removes it from the list of servers and self.bootstraps if applicable. updates any affected self.clients"""
		delete = None
		#check to see if the server to remove is a bootstrap server
		for b in self.bootstraps:
			if b.get('ip') == s:
				delete = b
				break

		del self.i3servers[s]

		#the server to remove was a bootstrap server
		if delete != None:
			#remove the server from the list of self.bootstraps
			added = 0 #a check to make sure that we actually add a new node into the list of self.bootstraps
			self.bootstraps.remove(delete)
			for key, value in self.i3servers.iteritems():
				#add the next i3 server that is not a bootstrap into the list of self.bootstraps
				if value not in self.bootstraps:
					self.bootstraps.append(value)
					added = 1
					break
			if added == 0:
				print("WARNING: A server was removed from the list of self.bootstraps, but there wasn't another available server to replace it")

		#update any self.clients who had their server set to the server that was removed
		for key, value in self.clients.iteritems():
			if value.get('server') == s:
				self.update_client(key)

########################################################################

	def add_client(self, c):
		"""computes the coordinates of a new client, and the closest server"""

		x,y = self.find_client_coords(c)
		if x==None or y==None:
			print("ERROR: Couldn't add client " + c)
			return

		newc = {}
		newc['ip'] = c
		newc['x'] = x
		newc['y'] = y

		self.clients[c] = newc
		s = self.update_closest_server(c)
		t = self.update_true_closest(c)

		#print("New client " + c + " is at ("+str(x)+", "+str(y)+")")
		#print("Registered server to " + c + " is " + s)
		#print("Closest server to " + c + " is " + t)

	def remove_client(self, c):
		del self.client[c]

########################################################################

	def calculate_accuracy(self):
		"""returns the percentage of closest server approximations that were correct"""
		total = 0.0
		correct = 0.0
		error = 0.0
		self.update_all_true()
		for key, value in self.clients.iteritems():

			if value.get('true') == value.get('server'):
				total = total + 1.0
				correct = correct + 1.0
			else:
				e1 = parse.get_edge(key, value.get('server'), self.cur)
				if len(e1) > 0:
					total = total + 1.0
					t1 = e1.time
					e2 = parse.get_edge(key, value.get('true'), self.cur)
					t2 = e2.time
					error = error + (t1-t2)/t1

		if total == 0.0:
			return 1, 1
		else:
			return (correct / total), (error / total)

	def print_status(self):
		print(self.bootstraps)
		print("servers:")
		for key, value in self.i3servers.iteritems():
			print(key)
		print("\nclients:")
		for key, value in self.clients.iteritems():
			print(key)

########################################################################
######################## END LIBRARY BEGIN MAIN ########################
########################################################################

	def simple_test(self):
		"""just a simple test function before i write more extensive tests"""

		primary = "195.195.56.2"
		secondary = "133.16.26.30"
		ternary = "170.147.45.164"
		client = "61.114.80.2"
		add = "193.243.229.111"
		self.bootstrap(primary, secondary, ternary)
		self.add_server(add)
		self.add_client(client)
		print(self.clients.get(client))
		self.remove_server(secondary)
		print(self.clients.get(client))
		print(self.calculate_accuracy())


