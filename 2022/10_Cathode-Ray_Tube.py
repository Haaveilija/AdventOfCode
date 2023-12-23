from dataclasses import dataclass

class AnswerCapturer:
    def __init__(self):
        self.v = []

    def values(self):
        return self.v

    def addValue(self, value):
        self.v.append(value)
    
    def total(self):
        return sum(self.v)
    

class CPU:
    def __init__(self, x=1, cycle=0, verbose=True, captureCondition=lambda cycle: True, answerCapturer = AnswerCapturer()):
        self.x = x
        self.cycle = cycle
        self.verbose = verbose
        self.lastCommand = 'noop'
        self.captureCondition = captureCondition
        self.answerCapturer = answerCapturer
        self.buffer = []

    def printState(self):
        if self.verbose:
            print(f"{self.lastCommand:8}    x: {self.x:3}    cycle: {self.cycle:3}    signal strength: {self.signalStrength():4}")
        if self.captureCondition(self.cycle):
            self.answerCapturer.addValue(self.signalStrength())
    
    def noop(self):
        self.cycle += 1
        self.lastCommand = 'noop'
        self.printState()
        

    def addx(self, a):
        self.cycle += 1
        self.lastCommand = f'addx {a}'
        self.printState()
        self.cycle += 1
        self.lastCommand = f'(wait)'
        self.printState()
        self.x += a
        

    def signalStrength(self):
        return self.x * self.cycle
    

    def runCommand(self, command, a):
        if command == 'noop':
            self.noop()
        elif command == 'addx':
            self.addx(a)


    
    

@dataclass
class Command:
    command: str = 'noop'
    value: int = 0


class User:
    def __init__(self, cpu = CPU()):
        self.cpu = cpu
        self.commands = []

    def runCommand(self, command, a):
        if command == 'noop':
            self.cpu.noop()
        elif command == 'addx':
            self.cpu.addx(a)
            

    def readCommandFile(self, filename):
        with open(filename, 'r') as f:
            for row in f:
                values = row.split()
                command = values[0]
                if len(values) == 1:
                    value = 0
                else:
                    value = int(values[1])
                self.commands.append(Command(command, value))

    def runAllCommands(self):
        for command in self.commands:
            self.runCommand(command.command, command.value)


class CRT:
    def __init__(self, width, height, state = None):
        self.width = width
        self.height = height
        self.total = width*height
        if state == None:
            self.state = [False for _ in range(self.total)]
        else:
            self.state = state

    def show(self):
        for i in range(self.total):
            if self.state[i]:
                print("#", end="")
            else:
                print(".", end="")
            if i % self.width == self.width-1:
                print("")

    def pixelBrightness(self, cycle, x):
        if (cycle-1) in [x-1, x, x+1]:
            return True
        return False

    def update(self, cycle, x):
        self.state[cycle-1] = self.pixelBrightness(cycle, x)


def readCommandFile(filename):
    commands = []
    with open(filename, 'r') as f:
        for row in f:
            values = row.split()
            command = values[0]
            if len(values) == 1:
                value = 0
            else:
                value = int(values[1])
            commands.append(Command(command, value))
    return commands

def exampleData():
    user = User()
    user.readCommandFile('inputs/10_example.txt')
    user.runAllCommands()

def partA():
    
    def captureCondition(cycle):
        cycles = [20, 60, 100, 140, 180, 220]
        if cycle in cycles:
            return True
        return False
    
    answer = AnswerCapturer()
    cpu = CPU(captureCondition=captureCondition, answerCapturer=answer)
    user = User(cpu=cpu)
    user.readCommandFile('inputs/10_input.txt')
    user.runAllCommands()
    print(answer.values(), "->", answer.total())

def partB():
    cpu = CPU()
    display = CRT(40, 6)
    display.show()
    #commands = readCommandFile('inputs/10_input.txt')
    commands = readCommandFile('inputs/10_example.txt')
    for command in commands:
        display.update(cpu.cycle, cpu.x)
        cpu.runCommand(command.command, command.value)
        
        display.show()
        

def main():
    #exampleData()
    #partA()
    partB()

    

if __name__ == "__main__":
    main()