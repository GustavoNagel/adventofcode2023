

from dataclasses import dataclass


@dataclass
class Card:
    winning_numbers: set[int]
    your_numbers: set[int]
    num_of_copies: int = 1

    def count_matching_numbers(self):
        return len(self.winning_numbers.intersection(self.your_numbers))

    def get_value(self):
        points = self.count_matching_numbers()
        return 2 ** (points - 1) if points else 0

    @classmethod
    def from_line(cls, line: str):
        winning_numbers_str, your_numbers_str = line.split(":")[1].split("|")
        return cls(winning_numbers=set(winning_numbers_str.split()), your_numbers=set(your_numbers_str.split()))

    def add_copies(self, num: int):
        self.num_of_copies += num

def run_and_sum(filename: str) -> int:
    with open(filename, 'r') as file:
        total = sum(Card.from_line(line).get_value() for line in file)
    return total

def run_and_count_scratchcards(filename: str) -> int:
    with open(filename, 'r') as file:
        cards = {i+1: Card.from_line(line) for i, line in enumerate(file)}

    total = 0
    for i, card in cards.items():
        for j in range(1, 1 + card.count_matching_numbers()):
            cards[i+j].add_copies(card.num_of_copies)
        total += card.num_of_copies
    return total

if __name__ == "__main__":
    print(run_and_sum("input_file.txt"))
    print(run_and_count_scratchcards("input_file.txt"))