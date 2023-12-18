import itertools

class MySequence:

    def __init__(self, list_elem: list[int]):
        self.list_elem = list_elem

    def get_diff(self) -> list[int]:
        return [j - i for i, j in itertools.pairwise(self.list_elem)]

    def get_next(self):
        if all(self.list_elem[0] == elem for elem in self.list_elem[1:]):
            return self.list_elem[0]
        return self.__class__(self.get_diff()).get_next() + self.list_elem[-1]

    def get_previous(self):
        if all(self.list_elem[0] == elem for elem in self.list_elem[1:]):
            return self.list_elem[0]
        return self.list_elem[0] - self.__class__(self.get_diff()).get_previous()

def run(filename: str, is_next: bool = True):
    my_sequences: list[MySequence] = []
    with open(filename, 'r') as file:
        for line in file:
            my_sequences.append(MySequence(list(map(int, line.split()))))

    return sum(sequence.get_next() if is_next is True else sequence.get_previous() for sequence in my_sequences)

if __name__ == "__main__":
    print(run("input_file.txt"))
    print(run("input_file.txt", is_next=False))