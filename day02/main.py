import re
from dataclasses import dataclass

pattern_game_id = re.compile(r"Game (\d+)")
pattern_game_set = re.compile(r"(\d+) (red|green|blue)")

@dataclass
class GameSet:
    red: int = 0
    green: int = 0
    blue: int = 0

    @classmethod
    def from_record(cls, line: str):
        game_set = cls()
        for match in pattern_game_set.finditer(line):
            setattr(game_set, match.group(2), int(match.group(1)))
        return game_set

    def __contains__(self, another_game_set: 'GameSet') -> bool:
        return (
            another_game_set.blue <= self.blue
            and another_game_set.green <= self.green
            and another_game_set.red <= self.red
        )

    def power(self) -> int:
        return self.red * self.green * self.blue

    def add_minimum(self, another_game_set: 'GameSet'):
        self.red = max(self.red, another_game_set.red)
        self.green = max(self.green, another_game_set.green)
        self.blue = max(self.blue, another_game_set.blue)


@dataclass
class Game:
    id_number: int
    game_sets: list[GameSet]

    @classmethod
    def from_record(cls, line: str):
        part1, part2 = line.split(":")
        id_number = int(pattern_game_id.match(part1).group(1))
        game_sets = [GameSet.from_record(game_set_line) for game_set_line in part2.split(";")]
        return cls(id_number, game_sets)

    def check_if_possible(self, game_set_total: GameSet) -> bool:
        return all(game_set in game_set_total for game_set in self.game_sets)

    def get_minimum(self):
        min_game_set = GameSet()
        for game_set in self.game_sets:
            min_game_set.add_minimum(game_set)
        return min_game_set

def run_and_sum_power() -> int:
    with open("input_file.txt", 'r') as file:
        games: list[Game] = [Game.from_record(line) for line in file]
    return sum(game.get_minimum().power() for game in games)

def run_and_sum() -> int:
    total = GameSet(red=12, green=13, blue=14)
    with open("input_file.txt", 'r') as file:
        games: list[Game] = [Game.from_record(line) for line in file]
    return sum(game.id_number for game in games if game.check_if_possible(total))

if __name__ == "__main__":
    print(run_and_sum())
    print(run_and_sum_power())
