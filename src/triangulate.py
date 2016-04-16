import parse

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
