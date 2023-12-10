import pytest
from .main import Race

test_inputs = (
    (7, 9, 4),
    (15, 40, 8),
    (30, 200, 9),
    (71530, 940200, 71503)
)
@pytest.mark.parametrize("time_input,record_input,expected_count", test_inputs)
def test_almanac_map(time_input: int, record_input: int, expected_count: int):
    race = Race(time_input, record_input)
    assert race.count_winning_possibilities() == expected_count
