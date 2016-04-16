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
	cur.execute("SELECT * FROM Measurements WHERE src = %s", (src,))
	results = []
	for record in cur:
		results.append(Edge(record[0], record[1], int(record[2])))
	return results
	
def match_on_dest(dest, cur):
	cur.execute("SELECT * FROM Measurements WHERE dest = %s", (dest,))
	results = []
	for record in cur:
		results.append(Edge(record[0], record[1], int(record[2])))
	return results
	
def get_edges(x, y, cur):
	cur.execute("SELECT * FROM Measurements WHERE (src = %s AND dest = %s) OR (src = %s AND dest = %s)", (x, y, y, x, ))
	results = []
	for record in cur:
		results.append(Edge(record[0], record[1], int(record[2])))
	return results
