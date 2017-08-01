import csv

# opens cities database and returns all major cities for a given state
# in a list
def get_cities(state):
	cities = []
	with open('cities.csv', newline='') as csvfile:
		read_file = csv.reader(csvfile)
		for row in read_file:
			if state in row:
				return row[1:]
#print(get_5_cities('OH'))

