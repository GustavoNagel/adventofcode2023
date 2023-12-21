# y, x (linha / coluna)
from collections import OrderedDict

direction_ref = {
    'N': (-1, 0),
    'S': (1, 0),
    'W': (0, -1),
    'E': (0, 1),
}

s_groups = {
    'N': (('W',),('E',)),
    'S': (('E',),('W',)),
    'W': (('N',),('S',)),
    'E': (('S',),('W',)),
}

opposite_dict = {
    'N': 'S',
    'S': 'N',
    'W': 'E',
    'E': 'W',
}

def convert_direction_to_delta(direction: str):
    return direction_ref[direction]

# PIPE_TYPE : FROM & TO , GROUP LEFT, GROUP RIGHT
pipe_ref = {
    'F': (('S', 'E'), ('N', 'W'), ()),
    'J': (('N', 'W'), ('S', 'E'), ()),
    'L': (('N', 'E'), (), ('S', 'W')),
    '7': (('S', 'W'), (), ('N', 'E')),
    '|': (('N', 'S'), ('E',), ('W',)),
    '-': (('W', 'E'), ('N',), ('S',)),
}
def get_pipe_out(pipe_type: str, input_direction: str) -> tuple[str, tuple, tuple]:
    if directions := pipe_ref.get(pipe_type):
        try:
            index_in = directions[0].index(input_direction)
        except ValueError:
            pass
        else:
            index_out = (index_in + 1) % 2
            pipe_out = directions[0][index_out]
            return pipe_out, directions[index_in + 1], directions[index_out + 1]
    
    return None, None, None

class PipeMap:

    def __init__(self, ref: list[list[str]]):
        self._ref = ref
        self.start_position = self._get_start_position()

    def _get_start_position(self) -> tuple[int, int]:
        for i, line in enumerate(self._ref):
            for j, elem in enumerate(line):
                if elem == 'S':
                    return i, j

    def get_elem(self, position: tuple[int, int]) -> str | None:
        try:
            return self._ref[position[0]][position[1]]
        except KeyError:
            return

    def get_next_position(self, position: tuple[int, int], direction: str) -> tuple[int, int]:
        delta = convert_direction_to_delta(direction)
        return (position[0] + delta[0], position[1] + delta[1])

    def set_path_faces(self, group_1, group_2):
        for i in range(len(self._ref)):
            for position, faces in group_1.items():
                if i == position[0]:
                    self.external = group_1 if 'N' in faces else group_2
                    self.internal = group_2 if 'N' in faces else group_1
                    return

    def count_internal_parts(self):
        count = 0
        for i, line in enumerate(self._ref[1:-2]):
            for j, elem in enumerate(line[1:-2]):
                if (i + 1, j + 1) not in self.internal:
                    # check going in North direction
                    for k in range(i + 1, 0, -1):
                        try:
                            internal_faces = self.internal[(k - 1, j + 1)]
                        except KeyError:
                            pass
                        else:
                            if 'S' in internal_faces:
                                count += 1
                            break

        return count

    def find_path_size(self):
        count = 0
        for main_direction in direction_ref.keys():
            direction = main_direction
            group_left: OrderedDict[tuple[int, int], tuple] = {self.start_position: s_groups[direction][0]}
            group_right: OrderedDict[tuple[int, int], tuple] = {self.start_position: s_groups[direction][1]}
            position = self.get_next_position(self.start_position, direction)
            elem = self.get_elem(position)
            while elem and elem != 'S':
                direction, _left, _right = get_pipe_out(elem, input_direction=opposite_dict[direction])
                if not direction:
                    break
                group_left[position] = _left
                group_right[position] = _right
                position = self.get_next_position(position, direction)
                elem = self.get_elem(position)
                count += 1
            if elem == 'S':
                self.set_path_faces(group_left, group_right)
                return int((count + 1) / 2)
            count = 0


def run(filename: str):
    with open(filename, 'r') as file:
        ref = [list(line) for line in file]
        my_pipe_map = PipeMap(ref)
        path_size = my_pipe_map.find_path_size()
        return path_size, my_pipe_map.count_internal_parts()

if __name__ == "__main__":
    print(run("input_file.txt"))
