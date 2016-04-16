import psycopg2

try:
    conn=psycopg2.connect("dbname='king' user='cmsc711' host='localhost' password='cmsc711'") #lol such bad practice
except:
    print("I am unable to connect to the database.")


