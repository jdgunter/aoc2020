"""Solution to Advent of Code Day 5."""

def read_input_lines():
    with open('input') as f:
        return f.readlines()

def decode_binary_number(code, one):
    val = 0
    exponents = reversed(range(len(code)))
    for exponent, char in zip(exponents, code):
        if char == one:
            val += 2 ** exponent
    return val

def decode_row_and_col(code):
    row = decode_binary_number(code[:7], one='B')
    col = decode_binary_number(code[7:10], one='R')
    return row, col

def compute_seat_id(row, col):
    return row * 8 + col

def missing_seat_id(seat_ids):
    min_seat = min(seat_ids)
    max_seat = max(seat_ids)
    return min(set(range(min_seat, max_seat+1)).difference(set(seat_ids)))

def main():
    rows_and_cols = [decode_row_and_col(code) for code in read_input_lines()]
    seat_ids = [compute_seat_id(row, col) for row, col in rows_and_cols]
    print('Max:', max(seat_ids))
    print('Seat:', missing_seat_id(seat_ids))

def test():
    code = 'FBFBBFFRLR'
    row, col = decode_row_and_col(code)
    seat_id = compute_seat_id(row, col)
    print(row, col)
    print(seat_id)

if __name__=='__main__':
    main()
