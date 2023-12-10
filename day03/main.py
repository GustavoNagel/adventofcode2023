import re
import itertools
import typing as t

symbol_pattern = re.compile(r"([^\.\d\s]{1})")
digits_pattern = re.compile(r"([\d]+)")
gear_pattern = re.compile(r"\*")

def get_symbols_indexes_by_line(line: str, pattern: re.Pattern) -> set[int]:
    indexes = set()
    for _match in pattern.finditer(line):
        start_index = _match.start() - 1 if _match.start() > 0 else _match.start()
        end_index = _match.end() + 1 if _match.end() + 1 < len(line) else _match.end()
        indexes.update(range(start_index, end_index))
    return indexes

def get_symbols_indexes(lines: tuple[str]):
    indexes = set()
    for line in lines:
        indexes.update(get_symbols_indexes_by_line(line, symbol_pattern))
    return indexes

def triplewise(file):
    full_iter = itertools.chain([''], file, [''])
    previous_line_iter, current_line_iter, next_line_iter = itertools.tee(full_iter, 3)
    next(previous_line_iter, None), next(previous_line_iter, None), next(current_line_iter, None)
    return zip(previous_line_iter, current_line_iter, next_line_iter)

def sum_part_numbers(filename: str) -> int:
    total = 0
    with open(filename, 'r') as file:
        for previous_line, current_line, next_line in triplewise(file):
            indexes = get_symbols_indexes((previous_line, current_line, next_line))
            for digits_match in digits_pattern.finditer(current_line):
                if digits_match.start() in indexes or (digits_match.end() - 1) in indexes:
                    total += int(digits_match.group(1))
    return total

def get_digits_and_indexes(line: str) -> t.Iterator[tuple[int, range]]:
    for _match in digits_pattern.finditer(line):
        start_index = _match.start() - 1 if _match.start() > 0 else _match.start()
        end_index = _match.end() + 1 if _match.end() + 1 < len(line) else _match.end()
        yield int(_match.group(1)), range(start_index, end_index)

def find_gear_symbols(line):
    for possible_gear_match in gear_pattern.finditer(line):
        yield possible_gear_match.start()

def get_gear_ratio(lines: tuple[str], gear_index: int):
    gear_neighborhood = []
    for line in lines:
        for digit_and_range in get_digits_and_indexes(line):
            if gear_index in digit_and_range[1]:
                gear_neighborhood.append(digit_and_range)
    if len(gear_neighborhood) != 2:
        return 0
    return gear_neighborhood[0][0] * gear_neighborhood[1][0]
            

def sum_gear_ratio(filename: str) -> int:
    total = 0
    with open(filename, 'r') as file:
        for previous_line, current_line, next_line in triplewise(file):
            for gear_index in find_gear_symbols(current_line):
                total += get_gear_ratio((previous_line, current_line, next_line), gear_index)
            
    return total

if __name__ == "__main__":
    print(sum_part_numbers("input_file.txt"))
    print(sum_gear_ratio("input_file.txt"))
