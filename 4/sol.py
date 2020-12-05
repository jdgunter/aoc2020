"""Solution to Advent of Code Day 4."""

import re


def read_input():
    with open('input') as f:
        return f.read().split('\n\n')


def validate_hgt(value):
    """Validate the hgt field."""
    if value[-2:] == 'cm':
        return 150 <= int(value[:-2]) <= 193
    elif value[-2:] == 'in':
        return 59 <= int(value[:-2]) <= 76
    return False


hcl_regex = re.compile(r'(\#[a-f0-9]{6})$')

ecl_regex = re.compile(r'(amb|blu|brn|gry|grn|hzl|oth)$')

pid_regex = re.compile(r'[0-9]{9}$')

"""Map from passport fields to validation functions for the corresponding values."""
validation_funcs = {
    'byr': lambda value: 1920 <= int(value) <= 2002,
    'iyr': lambda value: 2010 <= int(value) <= 2020,
    'eyr': lambda value: 2020 <= int(value) <= 2030,
    'hgt': lambda value: validate_hgt(value),
    'hcl': lambda value: hcl_regex.match(value),
    'ecl': lambda value: ecl_regex.match(value),
    'pid': lambda value: pid_regex.match(value),
    'cid': lambda value: True,
}


def contains_required_fields(fields):
    """Check if a passport contains all required fields."""
    for field in ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']:
        if field not in fields:
            return False
    return True


def validate_passport(fields):
    """Validate a single passport."""
    try:
        if contains_required_fields(fields.keys()):
            return all([validation_funcs[key](value) for key, value in fields.items()])
        return False
    except:
        return False


def count_valid_passports(input):
    """Count the valid passports in the sequence of lines."""
    num_valid = 0
    for passport_string in input:
        passport_fields = {word.split(':')[0]: word.split(':')[1] for word in passport_string.split()}
        num_valid += validate_passport(passport_fields)
    return num_valid


print(count_valid_passports(read_input()))