"""Solution to Advent of Code day 12.

Includes plot of ship movement."""

import matplotlib.pyplot as plt


def read_input_lines():
    with open('input') as f:
        return f.readlines()


class Ship:

    def __init__(self, initial_waypoint, *, translated_member):
        self.position = 0 + 0j
        self.waypoint = initial_waypoint
        assert translated_member in self.__dict__
        self.translated_member = translated_member

    def process_move(self, move):
        action = move[0]
        value = int(move[1:])
        if   action == 'N': self.__dict__[self.translated_member] += value * 1j
        elif action == 'S': self.__dict__[self.translated_member] -= value * 1j
        elif action == 'E': self.__dict__[self.translated_member] += value
        elif action == 'W': self.__dict__[self.translated_member] -= value
        elif action == 'L': self.waypoint *= 1j ** int(value/90)
        elif action == 'R': self.waypoint *= 1j ** (3 * int(value/90))
        elif action == 'F': self.position += value * self.waypoint


def manhattan_distance(z0, z1):
    return int(abs(z0.real - z1.real) + abs(z0.imag - z1.imag))


ship1 = Ship(1, translated_member='position')
ship2 = Ship(10+1j, translated_member='waypoint')
ship1_positions = []
ship2_positions = []
for line in read_input_lines():
    ship1.process_move(line)
    ship2.process_move(line)
    ship1_positions.append(ship1.position)
    ship2_positions.append(ship2.position)
print('Part 1:', manhattan_distance(ship1.position, 0 + 0j))
print('Part 2:', manhattan_distance(ship2.position, 0 + 0j))


line1, = plt.plot([z.real for z in ship1_positions], [z.imag for z in ship1_positions], 'r-+', label='Ship 1')
line2, = plt.plot([z.real for z in ship2_positions], [z.imag for z in ship2_positions], 'b-+', label='Ship 2')
plt.legend(handles=[line1, line2])
plt.show()