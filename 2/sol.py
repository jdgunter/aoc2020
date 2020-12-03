"""Solution to Advent of Code Day 2."""

def read_input_lines():
    with open('input') as f:
        return f.readlines()

def parse_policy_and_password(line):
    words = line.split(' ')
    left_num, right_num = tuple([int(x) for x in words[0].split('-')])
    character = words[1][0]
    password = words[2]
    return password, character, left_num, right_num

def num_valid_passwords(validate):
    lines = read_input_lines()
    lines = [parse_policy_and_password(line) for line in lines]
    num_valid = 0
    for line in lines:
        if validate(*line):
            num_valid += 1
    return num_valid

def validate_part1(password, character, policy_min, policy_max):
    return policy_min <= password.count(character) <= policy_max

def validate_part2(password, character, i, j):
    return (password[i-1] == character) ^ (password[j-1] == character)

def part1():
    print(num_valid_passwords(validate_part1))

def part2():
    print(num_valid_passwords(validate_part2))

def main():
    part1()
    part2()

if __name__=='__main__':
    main()