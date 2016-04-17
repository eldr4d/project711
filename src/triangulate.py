import parse

from geopy.geocoders import Nominatim
from geopy.distance import vincenty

conn = parse.establish_db_connection()
cur = conn.cursor()
testsrc = "12.10.83.40"
dests = parse.match_on_src(testsrc, cur);
#for d in dests:
#	print(d)

testdest = "12.10.83.40"
srcs = parse.match_on_dest(testdest, cur);
#for d in srcs:
#	print(d)

testother = "12.104.199.65"
edges = parse.get_edges(testsrc, testdest, cur)
#for d in edges:
#	print(d)

innodes = parse.get_highest_in_nodes(10, cur)
for d in innodes:
	print(d)


## Test gelocation distance
loc1 = parse.get_geolocation_lat_long("128.82.4.1", cur);
loc2 = parse.get_geolocation_lat_long("129.10.60.32", cur);

gloc1 = (float(loc1[0][0]), float(loc1[0][1]))
gloc2 = (float(loc2[0][0]), float(loc2[0][1]))

print vincenty(gloc1, gloc2).miles
