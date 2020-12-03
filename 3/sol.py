"""Solution to Advent of Code day 3."""

from functools import reduce
from operator import mul

def read_input_lines():
    with open('input') as f:
        return f.readlines()

class Slope:

    def __init__(self, lines):
        self.width = len(lines[0]) - 1  # -1 to account for ending newline
        self.length = len(lines)
        self.tree_positions = lines

    def tree_at(self, row, col):
        """Check if a tree exists at the given position."""
        return self.tree_positions[row][col % self.width] == '#'
    
    def count_trees_on_slope(self, delta_x, delta_y, origin_x=0, origin_y=0):
        """Count number of trees following a set path down the slope.

        The path starts at the given origin, and travels delta_x places right and
        delta_y places down at every step.
        """
        pos_x, pos_y = origin_x, origin_y
        trees_hit = 0
        while pos_y < self.length:
            if self.tree_at(pos_y, pos_x):
                trees_hit += 1
            pos_x += delta_x
            pos_y += delta_y
        return trees_hit

def main():
    cases = [(1,1), (3,1), (5,1), (7,1), (1,2)]
    slope = Slope(read_input_lines())
    tree_counts = [slope.count_trees_on_slope(right, down) for right, down in cases]
    print(reduce(mul, tree_counts, 1))

if __name__=='__main__':
    main()