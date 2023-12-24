from dataclasses import dataclass
from itertools import combinations

@dataclass
class Galaxy:
    x: int
    y: int


def get_distance(galaxy: Galaxy, other_galaxy: Galaxy):
    return abs(other_galaxy.x - galaxy.x) + abs(other_galaxy.y - galaxy.y)

def get_compressed_columns(galaxies: list[Galaxy], line_len: int) -> list:
    compressed_columns = set(range(line_len))
    contains_galaxies = set(galaxy.x for galaxy in galaxies)
    return list(compressed_columns - contains_galaxies)

def update_galaxies(galaxies, compressed_columns, compressed_rows, size: int):
    for galaxy in galaxies:
        galaxy.x += len(list(filter(lambda i: i < galaxy.x, compressed_columns))) * (size - 1)
        galaxy.y += len(list(filter(lambda j: j < galaxy.y, compressed_rows))) * (size - 1)

def run(filename: str, size: int = 2):
    with open(filename, 'r') as file:
        compressed_rows = []
        galaxies: list[Galaxy] = []
        for row, line in enumerate(file):
            marked = False
            for column, char in enumerate(line):
                if char == '#':
                    galaxies.append(Galaxy(x=column, y=row))
                    marked = True
            if not marked:
                compressed_rows.append(row)

    compressed_columns = get_compressed_columns(galaxies, column)
    update_galaxies(galaxies, compressed_columns, compressed_rows, size)
    return sum(get_distance(g1, g2)for g1, g2 in combinations(galaxies, 2))

if __name__ == "__main__":
    print(run("input_file.txt"))
    print(run("input_file.txt", size=1000000))
