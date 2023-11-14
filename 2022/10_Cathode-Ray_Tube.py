from dataclasses import dataclass

class AnswerCapturer:
    def __init__(self):
        self.values = []

    def addValue(self, value):
        self.values.append(value)
    
    def total(self):
        return sum(self.values)

class Buffer:
    def __init__(self, slots=2):
        self.slots = slots
        self.buffer = [0 for i in range(slots)]
        
    def advance(self, a=0):
        self.buffer.append(a)
        return self.buffer.pop(0)

    def __str__(self):
        return f"[{'', ''.join(self.buffer)}]"
    
    def __repr__(self):
        return f"[{'', ''.join(self.buffer)}]"

class Device:
    def __init__(self, x=1, cycle=0, verbose=True, captureCondition=lambda cycle: True, answerCapturer = AnswerCapturer()):
        self.x = x
        self.cycle = cycle
        self.buffer = Buffer()
        self.verbose = verbose
        self.lastCommand = 'noop'
        self.captureCondition = captureCondition
        self.answerCapturer = answerCapturer
        self.printState()

    def printState(self):
        if self.verbose:
            print(f"{self.lastCommand:8}    x: {self.x:3}    cycle: {self.cycle:3}    signal strength: {self.signalStrength():4}")
        if self.captureCondition(self.cycle):
            self.answerCapturer.addValue(self.signalStrength())
    
    def noop(self):
        self.cycle += 1
        self.x += self.buffer.advance(0)
        self.lastCommand = 'noop'
        self.printState()
        

    def addx(self, a):
        self.cycle += 1
        self.x += self.buffer.advance(a)
        self.lastCommand = f'addx {a}'
        self.printState()
        

    def signalStrength(self):
        return self.x * self.cycle
    
    

@dataclass
class Command:
    command: str = 'noop'
    value: int = 0


class User:
    def __init__(self, device = Device()):
        self.device = device
        self.commands = []

    def runCommand(self, command, a):
        if command == 'noop':
            self.device.noop()
        elif command == 'addx':
            self.device.addx(a)
            

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
    device = Device(captureCondition=captureCondition, answerCapturer=answer)
    user = User(device=device)
    user.readCommandFile('inputs/10_input.txt')
    user.runAllCommands()
    print(answer.values, "->", answer.total())

def main():
    exampleData()
    #partA()

    

if __name__ == "__main__":
    main()