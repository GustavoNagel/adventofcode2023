import pytest
from .main import run

test_inputs = (
    ("1abc2", 12),
    ("pqr3stu8vwx", 38),
    ("a1b2c3d4e5f", 15),
    ("treb7uchet", 77),
    ("sixrrmlkptmc18zhvninek", 69),
    ("jcb82eightwond", 82),
    ("twofourthree778nineeight", 28),
)

@pytest.mark.parametrize("line,expected_output", test_inputs)
def test_initial(line: str, expected_output: int):
    assert run(line) == expected_output
