"""Solution to Advent of Code day 10."""

def read_input_lines():
    with open('input') as f:
        return f.readlines()

input = list(map(int, read_input_lines()))
input.sort()


# Part 1.
one_differences = 0
three_differences = 1
for current, next in zip([0] + input, input):
    if next == current + 1:
        one_differences += 1
    elif next == current + 3:
        three_differences += 1

print('Part 1:', one_differences * three_differences)


# Part 2.
class ArrangementCounter:

    def __init__(self, adapters):
        self.adapters = sorted([0] + adapters) 
        self.num_adapters = len(self.adapters)
        self.lookup_table = [None] * self.num_adapters

    def count(self):
        return self._count_arrangements(0)

    def _count_arrangements(self, index):
        if index == self.num_adapters - 1:
            return 1
        if self.lookup_table[index] is None:
            joltage = self.adapters[index]
            num_arrangements = 0
            for other_joltage, other_index in zip(
                    self.adapters[index+1:index+4], range(index+1, index+4)):
                for delta in [1,2,3]:
                    if joltage + delta == other_joltage:
                        num_arrangements += self._count_arrangements(other_index)
            self.lookup_table[index] = num_arrangements
        return self.lookup_table[index]


print('Part 2:', ArrangementCounter(input).count())