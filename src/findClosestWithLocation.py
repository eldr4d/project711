import parse
import math
import psycopg2
import sys

conn = parse.establish_db_connection()
cur = conn.cursor()
cur2 = conn.cursor()
cur3 = conn.cursor()

dest_list = [
            "12.10.83.40",
            "12.108.132.7",
            "12.109.0.73",
            "12.150.152.253",
            "12.153.11.249",
            "61.114.80.2",
            "63.144.10.200",
            "128.59.176.4",
            "129.108.5.7",
            "130.126.101.8",
            "130.226.56.68",
            "131.123.100.7",
            "132.229.196.100",
            "133.16.26.30",
            "141.117.228.20",
            "142.137.3.49"]

cur.execute("SELECT ip from locations;")

for ips in cur:
  dist_min =  parse.get_closest_geo(ips[0], cur2)
  actual_min = parse.get_actual_closest(ips[0], cur2)
  print "*********************************"
  print ("Ip = " + ips[0] + "\nClosest Distance\nIp = " + dist_min[1] + " dist = " + str(dist_min[2]) + "\nLatency = " + str(dist_min[3]) +
        "\nActual Closest\nIp = " + actual_min[1] + "\nLatency = " + str(actual_min[2]) + "\n")
  print "--------------------"
  actual_min = parse.get_actual_closest_from_subset(ips[0], cur2, dest_list)
  print actual_min
  print "\n"
  print ("Ip = " + ips[0] + "\nClosest Distance\nIp = " + dist_min[1] + " dist = " + str(dist_min[2]) + "\nLatency = " + str(dist_min[3]) +
        "\nActual Closest\nIp = " + actual_min[1] + "\nLatency = " + str(actual_min[2]) + "\n")
  print "*********************************"
  
cur.close()
cur2.close()
cur3.close()

