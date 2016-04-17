import psycopg2

class Edge:
	def __init__(self, src, dest, time):
		self.src = src
		self.dest = dest
		self.time = time
		    
	def __str__(self):
		return "Source: " + self.src +", Dest: " + self.dest + ", Time: " + str(self.time)

def establish_db_connection():
	try:
		conn=psycopg2.connect("dbname='king' user='cmsc711' host='localhost' password='cmsc711'") 
		return conn
	except Exception as e:
		print("I am unable to connect to the database.")
		print(e)

def match_on_src(src, cur):
	cur.execute("SELECT * FROM measurements WHERE src = %s;", (src,))
	results = []
	for record in cur:
		results.append(Edge(record[1], record[2], int(record[3])))
	return results
	
def match_on_dest(dest, cur):
	cur.execute("SELECT * FROM measurements WHERE dest = %s;", (dest,))
	results = []
	for record in cur:
		results.append(Edge(record[1], record[2], int(record[3])))
	return results
	
def get_edges(x, y, cur):
	cur.execute("SELECT * FROM measurements WHERE (src = %s AND dest = %s) OR (src = %s AND dest = %s);", (x, y, y, x, ))
	results = []
	for record in cur:
		results.append(Edge(record[1], record[2], int(record[3])))
	return results
	

#this gives the destination nodes that have the 
def get_highest_in_nodes(limit, cur):
	cur.execute("with t as (select distinct src, dest from measurements) select dest, count(dest) from t group by dest order by count(dest) desc limit %s;", (limit,))
	results = []
	for record in cur:
		results.append(record)
	return results

#this gives the geolocation of an ip address
def get_geolocation_lat_long(ip, cur):
	cur.execute("SELECT latitude, longtitude FROM locations WHERE ip = %s;", (ip,))
	results = []
	for record in cur:
		results.append(record)
	return results
