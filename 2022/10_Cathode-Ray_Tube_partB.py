from dataclasses import dataclass
#import matplotlib.pyplot as plt

@dataclass
class Command:
    command: str = 'noop'
    value: int = 0


class CPU:
    def __init__(self, x=1, cycle=0):
        self.x : int = x
        self.cycle : int = cycle
        self.buffered : bool = False
        self.buffer : Command = None 
        self.xhistory = []

    def __repr__(self):
        return f"CPU | x: {self.x} | cycle: {self.cycle} | buffered: {self.buffered} | buffer: {self.buffer}"
    

    def next(self, command: Command):
        if self.buffered:
            self.buffered = False
            if self.buffer.command == 'addx':
                self._addx(self.buffer.value)
            self.buffer = None
            self.cycle += 1
        elif command.command == 'noop':
            self._noop()
            self.cycle += 1
        elif command.command == 'addx':
            self.buffer = Command('addx', command.value)
            self.buffered = True
            self.cycle += 1
        else:
            print(f"Unknown command: ({command.command}, {command.value})")
        self.xhistory.append(self.x)


    def _noop(self):
        return 

    def  _addx(self, v: int):
        self.x += v


class Display:
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
        if ((cycle) % self.width) in [x-1, x, x+1]:
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


def main():
    cpu = CPU()
    display = Display(40, 6)
    commands = readCommandFile('inputs/10_input.txt')
    for command in commands:
        while cpu.buffered:
            cpu.next(Command('none'))
            display.update(cpu.cycle, cpu.x)
            print(cpu)
            print(f"{cpu.x} is within +-1 from {cpu.cycle}? -> {display.pixelBrightness(cpu.cycle, cpu.x)}")
            display.show()
        
        print(command)
        cpu.next(command)
        display.update(cpu.cycle, cpu.x)
        print(cpu)
        print(f"{cpu.x} is within +-1 from {cpu.cycle}? -> {display.pixelBrightness(cpu.cycle, cpu.x)}")
        display.show()

    print("Final state:")
    display.show()

    #plt.plot(cpu.xhistory)
    #plt.show()



if __name__ == '__main__':
    main()