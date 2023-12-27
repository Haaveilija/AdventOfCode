
from dataclasses import dataclass
from typing import List, Callable


@dataclass
class Item:
    worryLevel: int

    def __repr__(self) -> str:
        return str(self.worryLevel)

class MonkeyHerd:
    def __init__(self):
        self.monkeys = []

    def add_monkey(self, Monkey):
        self.monkeys.append(Monkey)
    
    def remove_monkey(self, id):
        self.monkeys = [monkey for monkey in self.monkeys if monkey.id != id]
    
    def toss(self, tosserId : int, targetId : int, item : Item):
        try:
            tosser = [m for m in self.monkeys if m.id == tosserId][0]
        except IndexError:
            print(f"Tosser with id {tosserId} not found")

        try:
            target = [m for m in self.monkeys if m.id == targetId][0]
        except IndexError:
            print(f"Target with id {targetId} not found")
        
        tosser.startingItems = [i for i in tosser.startingItems if i.worryLevel != item.worryLevel]
        target.startingItems.append(item)

    def round(self, n=1, verbose=False, extraWorry=False):
        for i in range(n):
            for monkey in self.monkeys:
                monkey.turn(verbose, extraWorry)

    def monkeyBusiness(self):
        # multiply two most active monkey's inspect times together
        businessLevels = [monkey.inspectedItems for monkey in self.monkeys]
        total = 1
        print(sorted(businessLevels))
        for b in sorted(businessLevels)[-2:]:
            total *= b
        return total
            

@dataclass
class Monkey:
    id              : int
    startingItems   : List[Item]
    operation       : Callable[[Item], Item]
    test            : Callable[[Item], bool]
    testTrueTarget  : int 
    testFalseTarget : int
    herd : MonkeyHerd
    inspectedItems : int = 0

    def turn(self, verbose=False, extraWorry=False):
        if verbose: print(f'Monkey {self.id}:')
        for item in self.startingItems:
            if verbose:
                print(f"    Monkey inspects an item with a worry level of {item.worryLevel}.")
            self.inspectedItems += 1
            item.worryLevel = self.operation(item.worryLevel)
            if not extraWorry:
                if verbose: print(f'        Worry level increases to {item.worryLevel}')
                item.worryLevel = item.worryLevel // 3
            if verbose: print(f'        Monkey gets bored with item. Worry level is divided by 3 to {item.worryLevel}')
            if self.test(item):
                if verbose: print(f'        Item with worry level {item.worryLevel} is thrown to monkey {self.testTrueTarget}')
                self.herd.toss(self.id, self.testTrueTarget, item)
            else:
                if verbose: print(f'        Item with worry level {item.worryLevel} is thrown to monkey {self.testFalseTarget}')
                self.herd.toss(self.id, self.testFalseTarget, item)


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


def parseTarget(x: str) -> int:
    try:
        return int(x.split()[-1].strip())
    except ValueError:
        print(f"Invalid target: {x.split()[-1]}")


def read_monkeys_from_file(filename):
    herd = MonkeyHerd()
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
                monkeyId = int(head.split()[1])
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
            elif head.startswith('If true'):
                testTrueTarget = parseTarget(body)
                print(testTrueTarget)
            elif head.startswith('If false'):
                testFalseTarget = parseTarget(body)
                print(testFalseTarget)
                # if false is the last row of monkey definition
                # -> at this point we create monkey 
                herd.add_monkey(Monkey(monkeyId, startingItems, operation, test, testTrueTarget, testFalseTarget, herd))

    return herd






def main():
    herd = read_monkeys_from_file('inputs/11_example.txt')
    # herd = read_monkeys_from_file('inputs/11_input.txt')

    # for r in range(3):
    #     print(f"\n*** ROUND {r+1} ***")
    #     herd.round(verbose=False)
    #     [print(f'{m.id} | {m.inspectedItems} | {m.startingItems}') for m in herd.monkeys]

    for r in range(10000):
        herd.round(extraWorry=True)
        print(f"{r:5} | {herd.monkeyBusiness()}")
    



if __name__ == '__main__':
    main()