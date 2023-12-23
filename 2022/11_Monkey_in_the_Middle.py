
from dataclasses import dataclass
from typing import List, Callable


@dataclass
class Item:
    worryLevel: int

    def __repr__(self):
        return str(self.worryLevel)


class Monkey:
    id              : int
    startingItems   : List[Item]
    operation       : Callable[[Item], Item]
    test            : Callable[[Item], bool]
    testTrueTarget  : int 
    testFalseTarget : int



""" !!!
After each monkey inspects an item 
but before it tests your worry level, 
your relief that the monkey's inspection didn't damage the item 
causes your worry level to be 
divided by three and 
rounded down to the nearest integer.
"""



def parseStartingItems(x : str) -> List[int]:
    items = x.split(',')
    return [Item(worryLevel=int(item.strip())) for item in items]


def parseOperation(x : str) -> Callable[[Item], Item]:
    sides = x.split("=")
    parts = sides[1].split()

    first = None
    operator = None
    last = None
    try:
        first = int(parts[0])
        def firstfun(old):
            return first
    except:
        first = 'old'
        def firstfun(old):
            return old
    
    if parts[1] == '+':
        def operator(a, b):
            return a + b
    elif parts[1] == '*':
        def operator(a, b):
            return a * b
    else:
        raise ValueError("Operator must be + or *")
    
    try:
        last = int(parts[2])
        def lastfun(old):
            return last
    except:
        last = 'old'
        def lastfun(old):
            return old

    def operation(old):
        return operator(firstfun(old), lastfun(old))
    
    return operation


def parseTest(x: str) -> Callable[[Item], bool]:
    if not x.startswith('divisible by'):
        raise ValueError(f'Unknown test type: {x}')
    parts = x.split()
    last = parts[-1].strip()
    try:
        divisor = int(last)
    except ValueError:
        print("Invalid divisor: {last}")
    
    def test(item: Item):
        return item.worryLevel % divisor == 0
    
    return test




def read_monkeys_from_file(filename):
    monkeys = []
    with open(filename, 'r') as f:
        monkeyId = None
        startingItems = None
        operation = None
        test = None
        testTrueTarget = None
        testFalseTarget = None
        for row in f:
            parts = row.split(':')
            if row.strip() == "":
                print("---")
                continue
            
            head = parts[0].strip()
            body = parts[1].strip()

            if head.startswith('Monkey'):
                monkeyId = head.split()[1]
                print(f"{monkeyId=}")
            elif head.startswith('Starting items'):
                startingItems = parseStartingItems(body)
                print(f"{startingItems=}")
            elif head.startswith('Operation'):
                operation = parseOperation(body)
                print(operation)
                print(operation(4))
            elif head.startswith('Test'):
                test = parseTest(body)
                print(test)
                print(test(Item(23)))







def main():
    read_monkeys_from_file('inputs/11_example.txt')
    #read_monkeys_from_file('inputs/11_input.txt')



if __name__ == '__main__':
    main()