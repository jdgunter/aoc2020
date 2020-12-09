"""Solution for Advent of Code Day 9."""

def read_input_lines():
    with open('input') as f:
        return f.readlines()

def unique_pair_sums(numbers):
    sums = set()
    for i, x in enumerate(numbers):
        for y in numbers[i+1:]:
            sums.add(x+y)
    return sums

def find_invalid_number(numbers):
    start = 0
    size = 25
    for number in numbers[25:]:
        window = numbers[start:start+size]
        sums = unique_pair_sums(window)
        if number not in sums:
            return number
        start += 1

def sublist_sum(numbers, goal):
    start = 0
    end = 2
    sublist = numbers[start:end]
    summ = sum(sublist)
    while summ != goal:
        if summ < goal:
            end += 1
        if summ > goal:
            start += 1
        while end - start < 2:
            end += 1
        sublist = numbers[start:end]
        summ = sum(sublist)
    return sublist

def find_weakness(numbers):
    sublist = sublist_sum(numbers, find_invalid_number(numbers))
    return min(sublist) + max(sublist)

print('Part 1:', find_invalid_number(list(map(int, read_input_lines()))))
print('Part 2:', find_weakness(list(map(int, read_input_lines()))))