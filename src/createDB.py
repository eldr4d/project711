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

values = [
 '12.10.83.40',
 '12.108.132.7',
 '12.109.0.73',
 '12.150.152.253',
 '12.153.11.249',
 '61.114.80.2',
 '63.144.10.200',
 '128.59.176.4',
 '129.108.5.7',
 '130.126.101.8',
 '130.226.56.68',
 '131.123.100.7',
 '132.229.196.100',
 '133.16.26.30',
 '139.55.194.215',
 '140.116.250.1',
 '141.117.228.20',
 '142.137.3.49',
 '146.113.32.2',
 '150.208.125.253',
 '152.158.192.50',
 '153.90.2.15',
 '158.123.187.4',
 '161.142.84.65',
 '163.118.134.1',
 '165.127.9.13',
 '168.26.193.20',
 '170.147.45.164',
 '192.100.202.8',
 '192.190.180.69',
 '192.88.242.233',
 '193.243.229.111',
 '193.254.4.34',
 '194.133.122.42',
 '194.183.64.11',
 '195.134.0.101',
 '195.195.56.2',
 '196.27.0.29',
 '198.161.96.1',
 '199.108.228.50',
 '200.43.7.2',
 '200.68.178.3',
 '200.230.190.107',
 '202.50.90.1',
 '207.179.200.10',
 '208.35.201.3',
 '208.233.32.12',
 '209.124.64.13',
 '210.188.160.3',
 '217.199.96.82'
 ]



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
