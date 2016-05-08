import psycopg2

class Edge:
  def __init__(self, src, dest, time):
    self.src = src
    self.dest = dest
    self.time = time

  def __str__(self):
    return ("Source: " + self.src +", Dest: " + self.dest +
           ", Time: " + str(self.time))

  def __len__(self):
    return 1

def establish_db_connection():
  try:
    conn=psycopg2.connect("dbname='king' user='cmsc711' host='localhost' " +
                          " password='cmsc711'")
    return conn
  except Exception as e:
    print("I am unable to connect to the database.")
    print(e)

def match_on_src(src, cur):
  cur.execute("SELECT * FROM measurements WHERE src = %s;", (src,))
  results = []
  for record in cur:
    results.append(Edge(record[1], record[2], float(record[3])))
  return results

def match_on_dest(dest, cur):
  cur.execute("SELECT * FROM measurements WHERE dest = %s;", (dest,))
  results = []
  for record in cur:
    results.append(Edge(record[1], record[2], float(record[3])))
  return results

def get_edge(x, y, cur):
  cur.execute("SELECT src, dest, time FROM measurements WHERE src = %s " +
              " AND dest = %s;", (x, y, ))
  results = cur.fetchall()

  if(len(results) == 1):
    return Edge(results[0][0], results[0][1], float(results[0][2]))
  else:
    return []

def get_top_N_nodes(src, dest_list, top_N, cur):
  cur.execute("SELECT src, dest, time FROM measurements WHERE src = %s " +
              " AND dest = ANY(%s) order by time limit %s;",
              (src, dest_list, top_N))
  edges = []
  for result in cur:
    edges.append(Edge(result[0], result[1], float(result[2])))
  return edges

#this gives the destination nodes that have the
# BROKEN
# def get_highest_in_nodes(limit, cur):
#   cur.execute("with t as (select distinct src, dest from measurements) " +
#               "select dest, count(dest) from t group by dest order by " +
#               "count(dest) desc limit %s;", (limit,))
#   results = []
#   for record in cur:
#     results.append(record)
#   return results

#this gives the geolocation of an ip address
def get_geolocation_lat_long(ip, cur):
  cur.execute("SELECT latitude, longtitude FROM locations WHERE ip = %s;",
              (ip,))
  results = []
  for record in cur:
    results.append(record)
  return results

# Given an IP address it returns an array containing the closest geographically
# server and the latency to that server
# The latency is calculated by taking the mean of all the latencies inside
# the dataset
# Return type -> [origin_ip, dest_ip, distance_in_miles, latency]
def get_closest_geo(x, cur):
  cur.execute("SELECT src, dest, distance from colocations where src = %s " +
              " order by distance limit 1", (x, ));
  result = cur.fetchall()
  cur.execute("select time from measurements where src = %s and dest = %s",
              (x, result[0][1]))
  dist_min =  cur.fetchall()
  return [x, result[0][1], result[0][2], dist_min[0][0]]

# Given an IP address it returns an array containing the closest geographically
# server, for a subset of servers, and the latency to that server.
# The latency is calculated by taking the mean of all the latencies inside
# the dataset
# Return type -> [origin_ip, dest_ip, distance_in_miles, latency]
def get_closest_geo_from_subset(x, destinations, cur):
  cur.execute("SELECT src, dest, distance from colocations where src = %s " +
              "and dest = ANY(%s) order by distance limit 4",
              (x, destinations, ));
  results = cur.fetchall()
  for result in results:
    cur.execute("select time from measurements where src = %s and dest = %s",
                (x, result[1]))
    latency_min =  cur.fetchall()
    if(len(latency_min) == 0):
      continue
    else:
      return [x, result[1], result[2], float(latency_min[0][0])]

# Given an IP address it returns an array containing the closest server by means
# of latency
# The latency is calculated by taking the mean of all the latencies inside
# the dataset
#Return type -> [origin_ip, dest_ip, latency]
def get_actual_closest(x, cur):
  cur.execute("select src, dest, time from measurements where src = %s " +
              "order by time limit 1", (x,))
  actual_min = cur.fetchall()
  return actual_min[0]

# Given an IP address it returns an array containing the closest server by
# means of latency
# The latency is calculated by taking the mean of all the latencies inside
# the dataset
# Return type -> [origin_ip, dest_ip, latency]
def get_actual_closest_from_subset(x, destinations, cur):
  cur.execute("select src, dest, time from measurements where src = %s and " +
              " dest = ANY(%s) order by time limit 1",
              (x, destinations,))
  actual_min = cur.fetchall()
  return actual_min[0]
