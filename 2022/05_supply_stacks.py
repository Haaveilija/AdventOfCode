def determine_number_of_stacks(indexstring):
    return (len(indexstring)+1)//4


def extract_items(row, stack_count):
    items = {}
    for i in range(stack_count):
        item = row[i*4+1]
        if item == " ":
            continue
        items[i+1] = item
    return items


def insert_items(stacks, items):
    for key, value in items.items():
        if key not in stacks:
            stacks[key] = [value]
        else:
            stacks[key] += value

    return stacks




def starting_position_from_file(filename):
    startpos = []
    with open(filename, 'r') as file:
        for row in file:
            if row.rstrip() == "":
                break
            else:
                startpos.append(row.rstrip('\n'))
    
    stack_count = determine_number_of_stacks(startpos[-1])

    stacks = {}
    for row in reversed(startpos[:-1]):
        items = extract_items(row, stack_count)
        stacks = insert_items(stacks, items)

    return stacks


def encapsule_with_brackets(value):
    return f"[{value}]"


def prettyprint_stacks(stacks):
    for key, value in stacks.items():
        print(f"{key} {value}")



def commands_from_file(filename):
    with open(filename, 'r') as file:

        instructions_started = False
        commands = []
        for row in file:
            if instructions_started:
                words = row.split()
                (count, source, destination) = (int(words[1]), int(words[3]), int(words[5]))
                commands.append((count, source, destination))
            if row.rstrip() == '':
                instructions_started = True

    return commands



def execute_commands(stacks, commands):
    for (count, source, destination) in commands:
        for i in range(count):
            stacks[destination].append(stacks[source].pop())


def get_top_items(stacks):
    tops = ""
    for key, stack in stacks.items():
        tops += stack[-1]
    return tops

def crateMover9000(filename):
    print("CrateMover 9000")
    stacks = starting_position_from_file(filename)
    commands = commands_from_file(filename)

    print("Stacks at the beginning:")
    prettyprint_stacks(stacks)

    execute_commands(stacks, commands)
    print("\nStacks in the end:")
    prettyprint_stacks(stacks)

    top_items = get_top_items(stacks)
    print(top_items)


def crateMover9001(filename):
    print("\n CrateMover 9001")
    stacks = starting_position_from_file(filename)
    commands = commands_from_file(filename)

    print("Stacks at the beginning:")
    prettyprint_stacks(stacks)

    execute_commands_9001(stacks, commands)
    print("\nStacks in the end:")
    prettyprint_stacks(stacks)

    top_items = get_top_items(stacks)
    print(top_items)


def execute_commands_9001(stacks, commands):
    for (count, source, destination) in commands:
        movables = []
        for i in range(count):
            movables.append(stacks[source].pop())
        movables = list(reversed(movables))
        stacks[destination] += (movables)

    


def main():
    filename = 'inputs/05_input.txt'
    
    crateMover9000(filename)
    crateMover9001(filename)
    

if __name__ == "__main__":
    main()