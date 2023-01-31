def file_to_list(filename):
    """
    In each row of the file there is either a number or an empty row.
    Empty rows separate different elves.
    """
    max_calories = 0
    max_calories_elf = None
    with open(filename, 'r') as file:
        calories = 0
        elf = 0
        for row in file:
            row = row.rstrip()
            if row == "":
                if calories > max_calories:
                    max_calories = calories
                    max_calories_elf = elf
                calories = 0
            else:
                calories += int(row)
            elf += 1

        # This is needed because the file does not end in an empty row
        if calories > max_calories:
            max_calories = calories
            max_calories_elf = elf
    
    return max_calories, max_calories_elf

def top_three_calories(filename):
    elves = []
    with open(filename, 'r') as file:
        calories = 0
        for row in file:
            row = row.rstrip()
            if row == "":
                elves.append(calories)
                calories = 0
            else:
                calories += int(row)
    return sum(sorted(elves, reverse=True)[0:3])

def main():
    filename = input("Give filename: ")
    if filename == "":
        filename = 'inputs/01_input.txt'
    max_calories, max_calories_elf = file_to_list(filename)
    print(f"Elf {max_calories_elf} was carrying the most calories, {max_calories} cal")
    top_three = top_three_calories(filename)
    print(f"The top three elves were carrying {top_three} calories")


if __name__ == "__main__":
    main()