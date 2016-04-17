import psycopg2
import sys
import pyipinfodb
import time


ip_lookup = pyipinfodb.IPInfo('7bc84207e8b13e67b546b6857459aa263ffc5ce7fd9ca12af653de66015ca988')

try:
    conn=psycopg2.connect("dbname='king' user='cmsc711' host='localhost' password='cmsc711'") 
except Exception as e:
    print("I am unable to connect to the database.")
    print(e)

cur = conn.cursor()
cur2 = conn.cursor()

	
try:
	cur.execute("DROP TABLE locations;")
	print("dropped existing locations table")
except:
	print("There was no existing locations table to drop")
	
conn.commit()

try:
	cur.execute("CREATE TABLE locations (id serial PRIMARY KEY, ip varchar, country varchar," +
							" city_name varchar, zipcode varchar, longtitude varchar," +
							" latitude varchar);")
	print("created table locations")
except Exception as e:
	print("Could not create table locations")
	print(e)
	
conn.commit()

cur.execute("SELECT dest from destinations")

for record in cur:
	res =	ip_lookup.get_city(record[0])
	cur2.execute("INSERT INTO locations (ip, country, city_name, " +
							 "zipcode, longtitude, latitude) VALUES (%s, %s, %s, %s, %s, %s)",
							 (record[0], res["countryName"], res["cityName"], res["zipCode"], res["longitude"],
							  res["latitude"])
							)
	print res
	time.sleep(0.1)




conn.commit()
cur.close()
cur2.close()
conn.close()
