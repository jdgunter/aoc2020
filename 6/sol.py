"""Solution to Advent of Code day 6."""

from functools import reduce

def read_input():
    with open('input') as f:
        return f.read().split('\n\n')

def count_any_yes(group):
    return len(set(group.replace('\n', '')))

def count_all_yes(group):
    return len(reduce(
        lambda set_a, set_b: set_a.intersection(set_b),
        (set(member) for member in group.split('\n'))))

def yes_count(counting_func):
    count = 0
    for group in read_input():
        count += counting_func(group)
    return count

print('Part 1:', yes_count(count_any_yes))
print('Part 2:', yes_count(count_all_yes))
