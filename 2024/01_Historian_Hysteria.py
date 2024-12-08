
def read_input(filename):
	lists = [[], []]
	with open(filename, 'r') as f:
		for row in f:
			if row.strip() == "":
				continue # skip last empty line
			parts = [int(x) for x in row.split()]
			[lists[i].append(parts[i]) for i in range(len(lists))]
	[l.sort() for l in lists]
	return lists


def get_distance(lists):
	return sum([abs(lists[0][i] - lists[1][i]) for i in range(len(lists[0]))])

	
def first_part():
	filename = '01_input.txt'
	lists = read_input(filename)
	distance = get_distance(lists)
	return distance

def main():
	print(first_part())


if __name__ == "__main__":
	main()
