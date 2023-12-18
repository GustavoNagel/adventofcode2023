import pytest
from .main import MySequence

test_inputs = (
    ('0 3 6 9 12 15', 18),
    ('1 3 6 10 15 21', 28),
    ('10 13 16 21 30 45', 68),
)
@pytest.mark.parametrize("my_list,expected_next", test_inputs)
def test_my_sequence(my_list: str, expected_next: int):
    my_sequence = MySequence(list(map(int, my_list.split())))
    assert my_sequence.get_next() == expected_next
