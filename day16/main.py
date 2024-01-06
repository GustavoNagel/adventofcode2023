import sys
from contextlib import suppress
from dataclasses import dataclass
from enum import Enum

class Direction(Enum):
    NORTH = (-1, 0)
    SOUTH = (1, 0)
    WEST = (0, -1)
    EAST = (0, 1)

def invert_direction(direction: Direction) -> Direction:
    return {
        Direction.WEST: Direction.EAST,
        Direction.EAST: Direction.WEST,
        Direction.NORTH: Direction.SOUTH,
        Direction.SOUTH: Direction.NORTH,
    }[direction]


_ref: dict[str, tuple[tuple, tuple]] = {
    '\\': (
        (Direction.EAST, Direction.SOUTH),
        (Direction.WEST, Direction.NORTH),
    ),
    '/': (
        (Direction.EAST, Direction.NORTH),
        (Direction.WEST, Direction.SOUTH),
    ),
}

def get_direction_out(type: str, input_direction: Direction) -> Direction:
    index = 0
    try:
        index_in = _ref[type][index].index(input_direction)
    except ValueError:
        index = 1
        index_in = _ref[type][index].index(input_direction)

    index_out = (index_in + 1) % 2
    return _ref[type][index][index_out]


@dataclass
class Visited:
    row: int
    column: int
    direction: Direction

    def get_next(self):
        return self.__class__(
            self.row + self.direction.value[0],
            self.column + self.direction.value[1],
            self.direction,
        )

    def get_inverted(self) -> "Visited":
        return self.__class__(self.row, self.column, invert_direction(self.direction))

    def as_tuple(self) -> tuple[int, int, Direction]:
        return (self.row, self.column, self.direction)

@dataclass
class Contraption:
    layout: list[list[int]]

    def get_type(self, visited: Visited):
        if visited.row < 0 or visited.column < 0:
            raise IndexError("Negative indexes are not accepted here")
        return self.layout[visited.row][visited.column]

    def get_next_directions(self, visited: Visited) -> list[Visited]:
        next_visited = visited.get_next()
        try:
            next_type = self.get_type(next_visited)
        except IndexError:
            self.visited_edge.append(next_visited.get_inverted())
            return []
        if (
            next_type == '.'
            or (next_type == '-' and next_visited.direction in [Direction.WEST, Direction.EAST])
            or (next_type == '|' and next_visited.direction in [Direction.NORTH, Direction.SOUTH])
        ):
            return [next_visited]
        elif next_type in ('/', '\\'):
            next_visited.direction = get_direction_out(next_type, next_visited.direction)
            return [next_visited]
        elif next_type == '-':
            next_visited.direction = Direction.WEST
            return [next_visited.get_inverted(), next_visited]
        elif next_type == '|':
            next_visited.direction = Direction.NORTH
            return [next_visited.get_inverted(), next_visited]

    def run_over_layout(self, visited: Visited):
        for next_visited in self.get_next_directions(visited):
            if next_visited in self.visited_hist:
                continue
            self.visited_hist.append(next_visited)
            self.run_over_layout(next_visited)

    def energize_it(self, visited: Visited = Visited(0, -1, Direction.EAST)):
        recursion_limit = sys.getrecursionlimit()
        print(recursion_limit)
        sys.setrecursionlimit(10000)
        self.visited_hist = []
        self.visited_edge = []
        self.run_over_layout(visited)
        sys.setrecursionlimit(recursion_limit)
        total = self.count_energized_tiles()
        if hasattr(self, 'edges'):
            for visited in self.visited_edge:
                self.edges[visited.as_tuple()] = total
        return total

    def count_energized_tiles(self):
        points = set((visited.row, visited.column) for visited in self.visited_hist)
        return len(points)

    def get_edges(self) -> list[tuple[int, int, Direction]]:
        left_edge = [(x, -1, Direction.EAST) for x in range(len(self.layout))]
        right_edge = [(x, len(self.layout), Direction.WEST) for x in range(len(self.layout))]
        top_edge = [(-1, x, Direction.SOUTH) for x in range(len(self.layout[0]))]
        bottom_edge = [(len(self.layout[0]), x, Direction.NORTH) for x in range(len(self.layout[0]))]
        return left_edge + right_edge + bottom_edge + top_edge

    def get_max_energized_tiles(self):
        edges_list = self.get_edges()
        self.edges = dict.fromkeys(edges_list, None)
        for edge in edges_list:
            if self.edges[edge] is None:
                self.edges[edge] = self.energize_it(Visited(*edge))
        return max(self.edges.values())

def run(filename: str, maximum: bool = False):
    with open(filename, 'r') as file:
        contraption = Contraption([list(line.strip()) for line in file])
        return contraption.energize_it() if not maximum else contraption.get_max_energized_tiles()
