"""Solution to Advent of Code Day 4."""

import re


def read_input_lines():
    with open('input') as f:
        return f.readlines()


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


def validate_passport(**kwargs):
    """Validate a single passport."""
    if kwargs == {}:
        return False
    try:
        if contains_required_fields(kwargs.keys()):
            return all([validation_funcs[key](value) for key, value in kwargs.items()])
        return False
    except:
        return False


def count_valid_passports(lines):
    """Count the valid passports in the sequence of lines."""
    current_passport_fields = {}
    num_valid = 0
    for line in lines:
        if line == '\n':
            num_valid += validate_passport(**current_passport_fields)
            current_passport_fields = {}
        else:
            kv_pairs = {word.split(':')[0]: word.split(':')[1] for word in line.split()}
            current_passport_fields.update(kv_pairs)
    # Validate the final password. This does not happen in the loop above 
    # because there is no ending newline.
    num_valid += validate_passport(**current_passport_fields)
    return num_valid


print(count_valid_passports(read_input_lines()))