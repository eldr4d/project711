

with open('../Data/measurements', 'r') as f:
    first_line = f.readline()
    print(first_line.split( )[0])
