import parse
import math
import psycopg2
import sys

conn = parse.establish_db_connection()
cur = conn.cursor()
cur2 = conn.cursor()
cur3 = conn.cursor()

cur.execute("SELECT ip from locations;")

for ips in cur:
  dist_min =  parse.get_closest_geo(ips[0], cur2)
  actual_min = parse.get_actual_closest(ips[0], cur2)
  print ("Ip = " + ips[0] + "\nClosest Distance\nIp = " + dist_min[1] + " dist = " + str(dist_min[2]) + "\nLatency = " + str(dist_min[3]) +
        "\nActual Closest\nIp = " + actual_min[1] + "\nLatency = " + str(actual_min[2]) + "\n")

cur.close()
cur2.close()
cur3.close()

