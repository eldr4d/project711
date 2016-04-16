import psycopg2
import sys

try:
    conn=psycopg2.connect("dbname='king' user='cmsc711' host='localhost' password='cmsc711'") 
except Exception as e:
    print("I am unable to connect to the database.")
    print(e)

cur = conn.cursor()

try:
	cur.execute("DROP TABLE Measurements;")
	print("dropped existing Measurements table")
except:
	print("There was no existing Measurements table to drop")


try:
	cur.execute("CREATE TABLE Measurements (src varchar, dest varchar, time integer);")
	print("created table Measurements")
except Exception as e:
	print("Could not create table Measurements")
	print(e)

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



limit=100000


with open('../Data/measurements', 'r') as f:
    for line in f:
		if limit > 0:
			tokens = line.split()
			src=tokens[0]
			dest=tokens[2]
			t1 = int(tokens[4])
			t2 = int(tokens[5])
			if t1 > 0 and t2 > 0:
				limit = limit-1
				time= t1 - t2
				time=str(time)
				cur.execute("INSERT INTO Measurements (src, dest, time) VALUES (%s, %s, %s)", (src, dest, time))
		else:
			break
			



conn.commit()
cur.close()
conn.close()
