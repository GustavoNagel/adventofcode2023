import pytest
from .main import Game, GameSet

test_inputs = (
    ("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green", True),
    ("Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue", True),
    ("Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red", False),
    ("Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red", False),
    ("Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green", True),
)

@pytest.mark.parametrize("line,expected_output", test_inputs)
def test_initial(line: str, expected_output: bool):
    total = GameSet(red=12, green=13, blue=14)
    assert Game.from_record(line).check_if_possible(total) is expected_output


test_inputs_2 = (
    ("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green", 48),
    ("Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue", 12),
    ("Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red", 1560),
    ("Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red", 630),
    ("Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green", 36),
)

@pytest.mark.parametrize("line,expected_output", test_inputs_2)
def test_minimum_power(line: str, expected_output: bool):
    assert Game.from_record(line).get_minimum().power() == expected_output
