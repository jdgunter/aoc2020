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
def count_arrangements(adapters):
    adapters = sorted([0] + adapters) 
    num_adapters = len(adapters)
    lookup_table = [0] * num_adapters

    def _count_arrangements(index):
        if index == num_adapters - 1:
            return 1
        if lookup_table[index] == 0:
            joltage = adapters[index]
            for other_joltage, other_index in zip(
                    adapters[index+1:index+4], range(index+1, index+4)):
                for delta in [1,2,3]:
                    if joltage + delta == other_joltage:
                        lookup_table[index] += _count_arrangements(other_index)
        return lookup_table[index]

    return _count_arrangements(0)


print('Part 2:', count_arrangements(input))