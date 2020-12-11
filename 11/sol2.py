"""Solution to Advent of Code Day 11."""

from copy import deepcopy


def read_input_lines():
    with open('input') as f:
        return f.readlines()


def fix(f, x):
    fx = f(x)
    while x != fx:
        x = fx
        fx = f(x)
    return x


def out_of_bounds(seats, i, j):
    if i < 0 or i >= len(seats):
        return True
    elif j < 0 or j >= len(seats[0]):
        return True
    return False


def occupied_on_line(seats, i, j, dx, dy):
    if not out_of_bounds(seats, i + dx, j + dy):
        if seats[i + dx][j + dy] == '#':
            return True
        elif seats[i + dx][j + dy] == 'L':
            return False
        else:
            return occupied_on_line(seats, i + dx, j + dy, dx, dy)


def count_seen_occupied(seats, i, j):
    occupied = 0
    for dx, dy in [(1, 0), (1, 1), (0, 1), (-1, 1),
                   (-1, 0), (-1, -1), (0, -1), (1, -1)]:
        if occupied_on_line(seats, i, j, dx, dy):
            occupied += 1
    return occupied


def next_seating_iteration(seats):
    new_seats = deepcopy(seats)
    for i, row in enumerate(seats):
        for j, seat in enumerate(row):
            if seat == '.':
                continue
            occupied = count_seen_occupied(seats, i, j)
            if seat == 'L' and occupied == 0:
                new_seats[i][j] = '#'
            if seat == '#' and occupied >= 5:
                new_seats[i][j] = 'L'
    return new_seats


def count_occupied(seats):
    count = 0
    for row in seats:
        for seat in row:
            if seat == '#':
                count += 1
    return count


initial_state = list(map(list, read_input_lines()))
print('Part 2: %d' % count_occupied(fix(next_seating_iteration, initial_state)))
