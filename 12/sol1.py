"""Solution to Advent of Code day 12."""

from collections import namedtuple
from enum import IntEnum


def read_input_lines():
    with open('input') as f:
        return f.readlines()


class Direction(IntEnum):
    E = 0
    S = 1
    W = 2
    N = 3

    def rotate_left(self):
        return Direction((self.value - 1) % 4)

    def rotate_right(self):
        return Direction((self.value + 1) % 4)


class Ship:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction = Direction.E

    def process_move(self, move):
        action = move[0]
        value = int(move[1:])
        if action == 'N':
            self.y += value
        elif action == 'S':
            self.y -= value
        elif action == 'E':
            self.x += value
        elif action == 'W':
            self.x -= value
        elif action == 'L':
            while value != 0:
                self.direction = self.direction.rotate_left()
                value -= 90
        elif action == 'R':
            while value != 0:
                self.direction = self.direction.rotate_right()
                value -= 90
        elif action == 'F':
            self.process_move(self.direction.name + str(value))


Point = namedtuple('Point', 'x y')

def manhattan_distance(p, q):
    return abs(p.x - q.x) + abs(p.y - q.y)


ship = Ship()
for line in read_input_lines():
    ship.process_move(line)
print('Part 1:', manhattan_distance(ship, Point(x=0, y=0)))
