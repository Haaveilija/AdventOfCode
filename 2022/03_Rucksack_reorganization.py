LOWER_CASE_ALPHABETS = "abcdefghijklmnopqrstuvwxyz"
UPPER_CASE_ALPHABETS = LOWER_CASE_ALPHABETS.upper()
ALLPHABETS = LOWER_CASE_ALPHABETS + UPPER_CASE_ALPHABETS

def priority(letter):
    return ALLPHABETS.index(letter) + 1


def read_file(filename):
    rucksacks = []
    with open(filename, 'r') as file:
        for row in file:
            rucksacks.append(row)
    return rucksacks


def split_rucksack_in_half(rucksack):
    midpoint = int(len(rucksack)/2) # all rucksacks have even number of items
    return [rucksack[:midpoint], rucksack[midpoint:]]


def find_same(rucksack_halves):
    for item in rucksack_halves[0]:
        if item in rucksack_halves[1]:
            return item
        

def part_1_priority_sums(rucksacks):
    priority_sum = 0
    for rucksack in rucksacks:
        priority_sum += priority(find_same(split_rucksack_in_half(rucksack)))
    return priority_sum


def find_same_from_3(rucksacks):
    for letter in rucksacks[0]:
        if letter in rucksacks[1] and letter in rucksacks[2]:
            return letter


def part_2_priority_sums(rucksacks):
    priority_sum = 0
    i = 0
    group = []
    for rucksack in rucksacks:
        group.append(rucksack)
        if i % 3 == 2: # three rucksacks are in every group
            badge = find_same_from_3(group)
            priority_sum += priority(badge)
            group = []
        i += 1
    return priority_sum

def main():
    rucksacks = read_file('inputs/03_input.txt')

    print(part_1_priority_sums(rucksacks))
    print(part_2_priority_sums(rucksacks))


if __name__ == '__main__':
    main()