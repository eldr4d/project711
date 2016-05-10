import psycopg2
import sys
import json

try:
    conn=psycopg2.connect("dbname='king' user='cmsc711' host='localhost' password='cmsc711'") 
except Exception as e:
    print("I am unable to connect to the database.")
    print(e)

cur = conn.cursor()

try:
	cur.execute("DROP TABLE measurements;")
	print("dropped existing measurements table")
except:
	print("There was no existing measurements table to drop")

conn.commit()

try:
	cur.execute("DROP TABLE sources;")
	print("dropped existing sources table")
except:
	print("There was no existing sources table to drop")

conn.commit()

try:
	cur.execute("DROP TABLE destinations;")
	print("dropped existing destinations table")
except:
	print("There was no existing destinations table to drop")

conn.commit()

try:
	cur.execute("CREATE TABLE measurements (id serial PRIMARY KEY, src varchar, dest varchar, time numeric);")
	print("created table measurements")
except Exception as e:
	print("Could not create table measurements")
	print(e)

conn.commit()

try:
	cur.execute("CREATE TABLE sources (id serial PRIMARY KEY, src varchar);")
	print("created table sources")
except Exception as e:
	print("Could not create table sources")
	print(e)

conn.commit()

try:
	cur.execute("CREATE TABLE destinations (id serial PRIMARY KEY, dest varchar);")
	print("created table destinations")
except Exception as e:
	print("Could not create table destinations")
	print(e)

conn.commit()

ip_map = {}
with open('../Data/mapping_ip_to_row.txt') as mapping_file:
	for line in mapping_file:
		tokens = line.split()
		ip_map[int(tokens[0])] = tokens[1]

with open('../Data/matrix.txt', 'r') as f:
	cur_row = 0
	for line in f:
		destinations = line.split()
		cur_col = 0

		cur.execute("INSERT INTO sources (src) VALUES (%s);", (ip_map[cur_row],))
		cur.execute("INSERT INTO destinations (dest) VALUES (%s);", (ip_map[cur_row],))

		for time in destinations:
			if(time == -1):
				time = 99999999999.0
			if(cur_row != cur_col):
				cur.execute("INSERT INTO measurements (src, dest, time) VALUES (%s, %s, %s)", (ip_map[cur_row], ip_map[cur_col], float(time)))
			cur_col = cur_col + 1
		cur_row = cur_row + 1

conn.commit()


try:
	cur.execute("CREATE INDEX src_index ON measurements (src);")
	cur.execute("CREATE INDEX dest_index ON measurements (dest);")
	cur.execute("CREATE INDEX src_dest_index ON measurements (src, dest);")
	print("created indexes")
except Exception as e:
	print("Could not create indexes")
	print(e)
conn.commit()

cur.close()
conn.close()
