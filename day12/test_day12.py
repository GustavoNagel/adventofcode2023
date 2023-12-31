import pytest
from .main import Record

test_inputs = (
    ("???.### 1,1,3", 1, 1),
    (".??..??...?##. 1,1,3", 4, 1),
    ("?#?#?#?#?#?#?#? 1,3,1,6", 1, 1),
    ("????.#...#... 4,1,1", 1, 1),
    ("????.######..#####. 1,6,5", 4, 1),
    ("?###???????? 3,2,1", 10, 1),
    ("???.### 1,1,3", 1, 5),
    # (".??..??...?##. 1,1,3", 16384, 5),
    ("?#?#?#?#?#?#?#? 1,3,1,6", 1, 5),
    ("????.#...#... 4,1,1", 16, 5),
    # ("????.######..#####. 1,6,5", 2500, 5),
    # ("?###???????? 3,2,1", 506250, 5),
)

@pytest.mark.parametrize("line,expected_count,scale", test_inputs)
def test_record(line: str, expected_count: int, scale: int):
    record = Record(*line.split(), scale=scale)
    assert record.count_possibilities() == expected_count
