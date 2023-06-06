import time
import tkinter as tk
from tkinter import ttk


class RopeBoard:
    def __init__(self, start_position, width=6, height=5):
        self.start_position = start_position
        self.head_position = start_position
        self.tail_position = start_position
        self.width = width
        self.height = height
        self.tail_visited = {start_position}

    def distance(self, pos1, pos2):
        # manhattan distance, I think
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def move_one(self, direction):
        # 1. move head
        # 2. check tail distance (manhattan?)
        # 3. move tail if necessary
        (old_h_x, old_h_y) = self.head_position
        if direction == "R":
            self.head_position = (old_h_x+1, old_h_y)
        elif direction == "L":
            self.head_position = (old_h_x-1, old_h_y)
        elif direction == "U":
            self.head_position = (old_h_x, old_h_y+1)
        elif direction == "D":
            self.head_position = (old_h_x, old_h_y-1)
        else:
            raise InvalidDirectionException(f"Invalid direction \"{direction}\". Valid directions are R, L, U and D.")
        
        self.move_tail()

    
    def move_tail(self):
        # move tail to keep up with the head.
        # if distance is more than 2, always move diagonally.
        (tx, ty) = self.tail_position
        (hx, hy) = self.head_position
        dx = hx - tx
        dy = hy - ty

        dist = self.distance(self.head_position, self.tail_position)
        if dist <= 1:
            pass
        elif dist == 2:
            self.tail_position = (tx + (abs(dx) > abs(dy)) * (-1) ** (hx < tx), ty + 1*(abs(dy)>abs(dx))*(-1)** (hy < ty))
        elif dist == 3:
            self.tail_position = (tx + (abs(dx) > 0) * (-1) ** (hx < tx), ty + (abs(dy) > 0) * (-1) ** (hy < ty))
        else:
            pass
            #raise TooFarAwayException(f"Head is too far away from the tail.")
        self.tail_visited.add(self.tail_position)


    def move_many(self, direction, amount, print_steps=True):
        for _ in range(amount):
            self.move_one(direction)
            if print_steps:
                self.print_state()

        
    def print_state(self):
        print()
        print(f"H=({self.head_position[0]}, {self.head_position[1]}) -- T=({self.tail_position[0]}, {self.tail_position[1]})")

        # (0,0) is now in the bottom left corner just to spice things up a little :D
        for i in range(self.height):
            row = ""
            for j in range(self.width):
                x = j 
                y = self.height - i - 1 # -1 is because indexing starts with 0.

                if (x,y) == self.head_position:
                    row += "H" # add H
                elif (x,y) == self.tail_position:
                    row += "T" # add T
                elif (x,y) == self.start_position:
                    row += "s" # add s
                else: 
                    row += "." # add .
            print(row)

    
    def moves_from_file(self, filename, print_steps=True):
        with open(filename, 'r') as f:
            for row in f:
                direction, steps = row.split()
                self.move_many(direction, int(steps), print_steps)
                    


class LongRopeBoard(RopeBoard):
    def __init__(self, start_position,length=10, width=6, height=5):
        self.start_position = start_position
        self.length = length
        self.locations = [start_position for i in range(length)]
        self.width = width
        self.height = height
        self.tail_visited = {start_position}

    def move_one(self, direction):
        # 1. move head
        # 2. check tail distance (manhattan?)
        # 3. move tail if necessary
        (old_h_x, old_h_y) = self.locations[0]
        if direction == "R":
            self.locations[0] = (old_h_x+1, old_h_y)
        elif direction == "L":
            self.locations[0] = (old_h_x-1, old_h_y)
        elif direction == "U":
            self.locations[0] = (old_h_x, old_h_y+1)
        elif direction == "D":
            self.locations[0] = (old_h_x, old_h_y-1)
        else:
            raise InvalidDirectionException(f"Invalid direction \"{direction}\". Valid directions are R, L, U and D.")
        
        self.move_tail(1)

    def move_tail(self, tail_nro):
        # move tail to keep up with the head.
        # if distance is more than 2, always move diagonally.
        (tx, ty) = self.locations[tail_nro]
        (hx, hy) = self.locations[tail_nro-1]
        dx = hx - tx
        dy = hy - ty

        dist = self.distance(self.locations[tail_nro-1], self.locations[tail_nro])
        if dist <= 1:
            pass
        elif dist == 2:
            self.locations[tail_nro] = (tx + (abs(dx) > abs(dy)) * (-1) ** (hx < tx), ty + 1*(abs(dy)>abs(dx))*(-1)** (hy < ty))
        elif dist >= 3:
            self.locations[tail_nro] = (tx + (abs(dx) > 0) * (-1) ** (hx < tx), ty + (abs(dy) > 0) * (-1) ** (hy < ty))
        else:
            pass
            #raise TooFarAwayException(f"Head is too far away from the tail.")
        if tail_nro == self.length - 1:
            self.tail_visited.add(self.locations[tail_nro])
        else:
            self.move_tail(tail_nro+1)
    
    def print_state(self):
        print()
        print(f"H=({self.locations[0][0]}, {self.locations[0][1]}) -- T=({self.locations[-1][0]}, {self.locations[-1][1]})")

        # (0,0) is now in the bottom left corner just to spice things up a little :D
        for i in range(self.height):
            row = ""
            for j in range(self.width):
                x = j 
                y = self.height - i - 1 # -1 is because indexing starts with 0.

                if (x,y) == self.locations[0]:
                    row += "H" # add H
                elif (x,y) in self.locations:
                    row += str(self.locations.index((x,y))) # add Tail
                elif (x,y) == self.start_position:
                    row += "s" # add s
                else: 
                    row += "." # add .
            print(row)


class InvalidDirectionException(Exception):
    pass


class TooFarAwayException(Exception):
    pass


def main():
    rba = RopeBoard((0, 0))
    rba.moves_from_file("inputs/09_input.txt", False)
    print("Part a result:", len(rba.tail_visited))

    rbb = LongRopeBoard((0, 0), length=10, width=26, height=21)
    rbb.moves_from_file("inputs/09_input.txt", False)
    print("Part b result:",len(rbb.tail_visited))

    rbab = LongRopeBoard((0,0), length=2)
    rbab.moves_from_file("inputs/09_input.txt", False)
    print("Part a result using part b code:", len(rbab.tail_visited))

if __name__ == "__main__":
    main()