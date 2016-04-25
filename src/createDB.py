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

values = ['133.16.26.30',
 '210.188.160.3',
 '217.199.96.82',
 '61.114.80.2',
 '163.118.134.1',
 '200.43.7.2',
 '170.147.45.164',
 '202.50.90.1',
 '130.226.56.68',
 '209.124.64.13',
 '200.230.190.107',
 '12.10.83.40',
 '195.195.56.2',
 '208.35.201.3',
 '63.144.10.200',
 '207.179.200.10',
 '208.233.32.12',
 '200.68.178.3',
 '193.243.229.111',
 '194.183.64.11']



with open('../Data/measurements', 'r') as f:
    for line in f:
		if mode == 1:
			tokens = line.split()
			try:
				src=tokens[0]
				dest=tokens[2]
				t1 = int(tokens[4])
				t2 = int(tokens[5])
			except Exception as e:
				print("Bad Line")
				print(line)
				continue
			if src in values and dest in values and t1 > 0 and t2 > 0 and (t1 - t2) > 0:
				#limit = limit-1
				time= t1 - t2
				time=str(time)
				cur.execute("INSERT INTO measurements (src, dest, time) VALUES (%s, %s, %s)", (src, dest, time))
				cur.execute("INSERT INTO measurements (src, dest, time) VALUES (%s, %s, %s)", (dest, src, time))
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
