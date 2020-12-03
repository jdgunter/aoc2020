"""Solution for Day 1 of Advent of Code."""

def read_input():
    with open('input') as f:
        input = [int(line) for line in f.readlines()]
        return input

def values_adding_to(goal, lst):
    for i, p in enumerate(lst):
        for j, q in enumerate(lst[i+1:]):
            for r in lst[j+1:]:
                if p+q+r == goal:
                    return (p,q,r)
    return None

def main():
    input = read_input()
    x, y, z = values_adding_to(2020, input)
    print(x*y*z)

if __name__=='__main__':
    main()