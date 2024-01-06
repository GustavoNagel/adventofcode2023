from collections import namedtuple
# from turtle import Turtle
from itertools import pairwise

# turtle = Turtle()
Instruction = namedtuple('Instruction', ['direction', 'module', 'color'])
Point = namedtuple('Point', ['x', 'y', 'is_clockwise'])

ref = {
    'U': (0, 1),
    'R': (1, 0),
    'D': (0, -1),
    'L': (-1, 0),
}
clockwise = {
    'U': 'R',
    'R': 'D',
    'D': 'L',
    'L': 'U',
}


def get_next_point(point: Point, instruction: Instruction, next_direction: str):
    delta = ref[instruction.direction]
    return Point(
        x=point.x + delta[0] * int(instruction.module),
        y=point.y + delta[1] * int(instruction.module),
        is_clockwise=is_clockwise(instruction.direction, next_direction),
    )

def get_coordinates(point: Point) -> list[tuple[int, int]]:
    """
    1 . . 2
    .     .
    .     .
    0 . . 3
    """
    return [
        (point.x, point.y),
        (point.x, point.y + 1),
        (point.x + 1, point.y + 1),
        (point.x + 1, point.y),
    ]

def get_coordinates_corner(direction, point: Point):
    index = list(clockwise.keys()).index(direction)
    coords = get_coordinates(point)
    add_index = int(point.is_clockwise)
    return coords[(index + add_index) % 4], coords[(index + 2 + add_index) % 4]

def is_clockwise(direction: str, new_direction) -> bool:
    return bool(clockwise[direction] == new_direction)


def calculate_area(list_of_points: list[Point]) -> int:
    sum1 = sum2 = 0
    for coord1, coord2 in pairwise([list_of_points[-1]] + list_of_points):
        sum1 += coord1[0] * coord2[1]
        sum2 += coord2[0] * coord1[1]
    return abs(int((sum1 - sum2) / 2))

def fix_instructions(list_of_instructions: list[Instruction]) -> list[Instruction]:
    new_list_of_instructions = []
    translator = list(clockwise.values())
    for instruction in list_of_instructions:
        new_list_of_instructions.append(
            Instruction(
                translator[int(instruction.color[7])],
                int(instruction.color[2:7], 16),
                '',
            )
        )
    return new_list_of_instructions

def run(filename: str, fix_instructions_opt: bool = False):
    with open(filename, 'r') as file:

        list_of_instructions = [Instruction(*line.split()) for line in file]
        if fix_instructions_opt:
            list_of_instructions = fix_instructions(list_of_instructions)
        point = Point(0, 0, False)
        side_a, side_b = [], []
        for instruction, next_instruction in pairwise(
            list_of_instructions + [list_of_instructions[0]]
        ):
            point = get_next_point(point, instruction, next_instruction.direction)
            corner_a, corner_b = get_coordinates_corner(instruction.direction, point)
            side_a.append(corner_a)
            side_b.append(corner_b)
            # turtle.setpos(*point)
        # turtle.screen.mainloop()
        return max(calculate_area(side_a), calculate_area(side_b))

if __name__ == "__main__":
    print(run("input_file.txt"))
    print(run("input_file.txt", fix_instructions_opt=True))
