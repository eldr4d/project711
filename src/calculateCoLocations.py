import parse
import math
import psycopg2
import sys

from geopy.geocoders import Nominatim
from geopy.distance import vincenty

try:
    conn=psycopg2.connect("dbname='king' user='cmsc711' host='localhost' password='cmsc711'")
except Exception as e:
    print("I am unable to connect to the database.")
    print(e)


cur = conn.cursor()
cur2 = conn.cursor()
cur3 = conn.cursor()

try:
  cur.execute("DROP TABLE colocations;")
  print("dropped existing colocations table")
except:
  print("There was no existing colocations table to drop")

conn.commit()

try:
  cur.execute("CREATE TABLE colocations (id serial PRIMARY KEY, src varchar, dest varchar, distance numeric);")
  print("created table colocations")
except Exception as e:
  print("Could not create table colocations")
  print(e)

conn.commit()

cur.execute("SELECT id, ip, longtitude, latitude from locations;")

for record in cur:
  gloc1 = (float(record[2]), float(record[3]))
  print record[0]
  cur2.execute("SELECT id, ip, longtitude, latitude FROM locations WHERE id > %s;", (record[0],))
  for record2 in cur2:
    gloc2 = (float(record2[2]), float(record2[3]))

    dist = vincenty(gloc1, gloc2).miles
    # Add both pairs for easier lookup
    cur3.execute("INSERT INTO colocations (src, dest, distance) VALUES (%s, %s, %s)",
                 (record[1], record2[1], dist,)
                 )
    cur3.execute("INSERT INTO colocations (src, dest, distance) VALUES (%s, %s, %s)",
                 (record2[1], record[1], dist,)
                 )

conn.commit()
cur.close()
cur2.close()
cur3.close()
conn.close()
