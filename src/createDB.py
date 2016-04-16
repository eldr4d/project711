import psycopg2
import sys

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
	cur.execute("CREATE TABLE measurements (id serial PRIMARY KEY, src varchar, dest varchar, time integer);")
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

'''
try:
	cur.execute("INSERT INTO Measurements (src, dest, time) VALUES (%s, %s, %s)", ("a", "b", 3))
except Exception as e:
	print("couldnt insert into DB!")
	print(e)


try:
	cur.execute("SELECT * FROM Measurements;")
	print(cur.fetchone())
except Exception as e:
	print("couldnt query DB!")
	print(e)
'''



limit=1000
skip=1000000
mode=1


with open('../Data/measurements', 'r') as f:
    for line in f:
		if mode == 1:
			tokens = line.split()
			src=tokens[0]
			dest=tokens[2]
			t1 = int(tokens[4])
			t2 = int(tokens[5])
			if t1 > 0 and t2 > 0:
				limit = limit-1
				time= t1 - t2
				time=str(time)
				cur.execute("INSERT INTO measurements (src, dest, time) VALUES (%s, %s, %s)", (src, dest, time))
				cur.execute("INSERT INTO sources (src) SELECT %s WHERE NOT EXISTS (SELECT src FROM sources WHERE src = %s);", (src,src,))
				cur.execute("INSERT INTO destinations (dest) SELECT %s WHERE NOT EXISTS (SELECT dest FROM destinations WHERE dest = %s);", (dest,dest,))
			if limit == 0:
				limit = 1000
				mode = 0
		else:
			if skip > 0:
				skip= skip-1
			else:
				skip=1000000
				mode=1
			
			



conn.commit()
cur.close()
conn.close()
