import re
import itertools
import math

pattern_map = re.compile(r"(\w{3}) = \((\w{3}), (\w{3})\)")

def read_file(filename: str):
    with open(filename, 'r') as file:
        instructions = next(file).strip()
        next(file)
        desert_map = {}
        for line in file:
            desert_map_match = pattern_map.search(line)
            desert_map[desert_map_match.group(1)] = {
                'L': desert_map_match.group(2),
                'R': desert_map_match.group(3),
            }
        return instructions, desert_map

def run(filename: str):
    instructions, desert_map = read_file(filename=filename)
    position = 'AAA'
    for count, direction in enumerate(itertools.cycle(instructions)):
        position = desert_map[position][direction]
        if position == 'ZZZ':
            break

    return count + 1

def mount_iter(start: int, end: int, solutions: list[int]):
    print(start, end, solutions)
    for i in itertools.count():
        base = start + (end - start) * i
        for j in solutions:
            yield base + (j - start)

def get_repetitions(position: str, desert_map: dict[str, dict], instructions: str):
    position_temp = position
    my_list = []
    my_dict =  {}
    size = len(instructions)
    for count in itertools.count():
        for i, direction in enumerate(instructions):
            position_temp = desert_map[position_temp][direction]
            if position_temp.endswith('Z'):
                print(position_temp, size, count, i, size * count + i + 1)
                my_list.append(size * count + i + 1)

        if position_temp in my_dict.keys():
            break
        my_dict[position_temp] = size * count + i + 1

    return mount_iter(my_dict[position_temp], size * count + i + 1, my_list)


def get_repetitions_new(position: str, desert_map: dict[str, dict], instructions: str):
    position_temp = position
    my_list = []
    my_dict =  {}
    size = len(instructions)
    for count in itertools.count():
        for i, direction in enumerate(instructions):
            position_temp = desert_map[position_temp][direction]
            if position_temp.endswith('Z'):
                print(position_temp, size, count, i, size * count + i + 1)
                my_list.append(size * count + i + 1)

        if position_temp in my_dict.keys():
            break
        my_dict[position_temp] = size * count + i + 1

    start = my_dict[position_temp]
    end = size * count + i + 1
    my_filtered_list = list(filter(lambda x: start < x <= end, my_list))
    return int((end - start) / len(my_filtered_list))

def run_for_ghosts_new(filename: str):
    instructions, desert_map = read_file(filename=filename)
    positions_list = [position for position in filter(lambda x: x.endswith('A'), desert_map.keys())]
    result = [get_repetitions_new(position, desert_map, instructions) for position in positions_list]
    return math.lcm(*result)

def run_for_ghosts(filename: str):
    instructions, desert_map = read_file(filename=filename)
    positions_list = [position for position in filter(lambda x: x.endswith('A'), desert_map.keys())]
    my_iterators = [get_repetitions(position, desert_map, instructions) for position in positions_list]
    ending_positions = [next(i) for i in my_iterators]
    limit_print = 1_000_000_000
    while True:
        max_position = max(ending_positions)
        for i, position in enumerate(ending_positions):
            if position < max_position:
                ending_positions[i] = next(my_iterators[i])
        if all(max_position == i for i in ending_positions):
            break
        if max_position > limit_print:
            print(max_position, ending_positions)
            limit_print += 1_000_000_000
    return max_position

if __name__ == "__main__":
    print(run("input_file.txt"))
    # print(run_for_ghosts("input_file.txt"))  # Too slow!
    print(run_for_ghosts_new("input_file.txt"))