
import numpy as np

diff_ref = [2**i for i in range(20)]

def are_values_almost_equals(value_1: int, value_2: int):
    """Check if 2 lines are equals"""
    if value_2 < value_1:
        value_2, value_1 = value_1, value_2
    value_2 = bin(value_2)[2:]
    value_1_list = list(f'{bin(value_1)[2:]:0>{len(value_2)}}')
    found_difference = False
    for elem_2 in value_2:
        elem_1 = value_1_list.pop(0)
        if elem_1 != elem_2:
            if found_difference:
                return False
            found_difference = True

    return found_difference


def are_lists_almost_equals(list_1: list, list_2: list):
    if len(list_1) != len(list_2):
        return False
    found_difference = False
    list_2_copy = list_2.copy()
    for elem_1 in list_1:
        elem_2 = list_2_copy.pop(0)
        if are_values_almost_equals(elem_1, elem_2):
            if found_difference:
                return False
            found_difference = True
        elif elem_1 != elem_2:
            return False
    return found_difference


def identify_mirror(vector_sum: list) -> int:
    already_visited = []
    for i, elem in enumerate(vector_sum):
        if already_visited and elem == already_visited[-1]:
            size = min(len(vector_sum) - i, i)
            if already_visited[i-1:i-1-size if i-1-size >=0 else None:-1] == vector_sum[i:i+size]:
                return i
        already_visited.append(elem)


def identify_almost_mirror(vector_sum: list) -> int:
    already_visited = []
    for i, elem in enumerate(vector_sum):
        if already_visited and (elem == already_visited[-1] or are_values_almost_equals(elem, already_visited[-1])):
            size = min(len(vector_sum) - i, i)
            if are_lists_almost_equals(
                already_visited[i-1:i-1-size if i-1-size >=0 else None:-1],
                vector_sum[i:i+size]
            ):
                return i
        already_visited.append(elem)

class Pattern:

    def __init__(self, matrix_location: np.ndarray, almost_equal: bool = False):
        self.matrix_num = np.where(matrix_location == '#', 1, 0)
        self.func = identify_almost_mirror if almost_equal else identify_mirror

    def get_first_mirror(self):
        a, b = self.matrix_num.shape
        weight_1 = np.array([[2**i] * b for i in range(a)], np.int32)
        columns_sum = (self.matrix_num * weight_1).sum(axis=0)
        index = self.func(list(columns_sum))
        if index:
            return index
        weight_2 = np.array([[2**i] * a for i in range(b)], np.int32).transpose()
        rows_sum = (self.matrix_num * weight_2).sum(axis=1)
        index = self.func(list(rows_sum))
        return index * 100 if index else 0

def run(filename: str, almost_equal: bool = False):
    total = 0
    with open(filename, 'r') as file:
        ref = []
        for line in map(lambda x: x.strip(), file):
            if line:
                ref.append(list(line))
            else:
                total += Pattern(np.array(ref), almost_equal).get_first_mirror()
                ref = []
        total += Pattern(np.array(ref), almost_equal).get_first_mirror()
        return total

if __name__ == "__main__":
    print(run("input_file.txt"))
    print(run("input_file.txt", almost_equal=True))