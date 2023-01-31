def read_file(filename):
    pairs = []
    with open(filename, 'r') as file:
        for row in file:
            pair = row.rstrip().split(",")
            pairs.append([
                [int(i) for i in pair[0].split('-')],
                [int(i) for i in pair[1].split('-')]
                ])
    return pairs


def fully_contains(pair):
    if pair[0][0] >= pair[1][0] and pair[0][1] <= pair[1][1] or \
       pair[1][0] >= pair[0][0] and pair[1][1] <= pair[0][1]:
        return 1
    return 0


def between(high, low, value):
    return value <= high and value >= low


def partial_overlap(pair):
    if fully_contains(pair):
        return 1
    
    # If the pairs overlap, both have a point in between the others 
    # end points, so it is enough to check only one of them having a 
    # point between the other ones endpoints.
    if between(pair[0][1], pair[0][0], pair[1][0]) or \
       between(pair[0][1], pair[0][0], pair[1][1]):
        return 1
    
    return 0


def part_1_answer(pairs):
    containments = 0
    for pair in pairs:
        containments += fully_contains(pair)
    return containments


def part_2_answer(pairs):
    overlaps = 0
    for pair in pairs:
        overlaps += partial_overlap(pair)
    return overlaps


def main():
    pairs = read_file('inputs/04_input.txt')
    print(part_1_answer(pairs))
    print(part_2_answer(pairs))


if __name__ == "__main__":
    main()