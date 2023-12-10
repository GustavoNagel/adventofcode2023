import re
from itertools import islice, chain, count

almanac_map_pattern = re.compile(r"(\w+)\-to\-(\w+) map\:")

def batched(iterable, n):
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch

class AlmanacMap:

    def __init__(self, origin_name: str, destination_name: str) -> None:
        self.origin_name = origin_name
        self.destination_name = destination_name
        self._ref: list[(tuple[int, int, int])] = []

    def get_destination_number(self, origin: int) -> int:
        for i, j, n in self._ref:
            if j <= origin < j + n:
                return i + (origin - j)
        return origin

    def get_origin_number(self, destination: int) -> int:
        for i, j, n in self._ref:
            if i <= destination < i + n:
                return j + (destination - i)
        return destination

    def add_ref_from_line(self, line: str):
        self._ref.append(tuple(map(int, line.split())))

def set_ranges(seeds_input: map):
    return [range(i, i + j) for i, j in batched(seeds_input, n=2)]

def get_seeds_from_ranges(seeds_input: map):
    for n in chain.from_iterable(set_ranges(seeds_input)):
        yield n

def read_file(filename) -> tuple[list[AlmanacMap], map]:
    almanac = []
    almanac_map: AlmanacMap = None
    with open(filename, 'r') as file:
        seeds_input = map(int, next(file)[7:].split())
        for line in file:
            line = line.strip()
            if not line:
                continue
            map_match = almanac_map_pattern.match(line)
            if map_match:
                if almanac_map:
                    almanac.append(almanac_map)
                almanac_map = AlmanacMap(origin_name=map_match.group(1), destination_name=map_match.group(2))
            else:
                almanac_map.add_ref_from_line(line)
        almanac.append(almanac_map)
    return almanac, seeds_input

def run(filename: str, is_range=False) -> int:
    almanac, seeds_input = read_file(filename)
    if is_range:
        seeds_input = get_seeds_from_ranges(seeds_input)
    locations = []
    for seed in seeds_input:
        destination = seed
        for almanac_map in almanac:
            destination = almanac_map.get_destination_number(destination)
        locations.append(destination)
    return min(locations)

def get_min_destination(filename: str):
    almanac, seeds_input = read_file(filename)
    seeds_ranges = set_ranges(seeds_input)
    for i in count():
        origin = i
        for almanac_map in almanac[::-1]:
            origin = almanac_map.get_origin_number(origin)
        if any(origin in _range for _range in seeds_ranges):
            return i
        if i % 1_000_000 == 0:
            print(i)

if __name__ == "__main__":
    print(run("input_file.txt"))
    # print(run("input_file.txt", is_range=True))  # memory overflow problem
    print(get_min_destination("input_file.txt"))