import psycopg2

try:
    conn=psycopg2.connect("dbname='king' user='postgres' host='localhost' password='postgres'") #lol such bad practice
except:
    print("I am unable to connect to the database.")


