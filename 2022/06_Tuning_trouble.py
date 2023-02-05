def get_letters(filename):
    with open(filename, 'r') as file:
        while True:
            letter = file.read(1)
            if not letter: break
            yield letter


def unique_chars(buffer):
    return len(buffer) == len(set(list(buffer)))


def detect_marker(filename, buffer_length):
    buffer = ""
    i = 0
    for letter in get_letters(filename):
        i += 1
        if len(buffer) < buffer_length:
            buffer += letter
            continue

        buffer = buffer[1:] + letter

        if unique_chars(buffer):
            return i
        


def main():
    filename = 'inputs/06_input.txt'
    part_1_result = detect_marker(filename, 4)
    print(part_1_result)

    part_2_result = detect_marker(filename, 14)
    print(part_2_result)


if __name__ == "__main__":
    main()