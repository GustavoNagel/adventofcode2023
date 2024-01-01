import pytest
from .main import hash_me, get_total_focusing_power

test_inputs = (
    ("rn=1", 30),
    ("cm-", 253),
    ("qp=3", 97),
    ("cm=2", 47),
    ("qp-", 14),
    ("pc=4", 180),
    ("ot=9", 9),
    ("ab=5", 197),
    ("pc-", 48),
    ("pc=6", 214),
    ("ot=7", 231),
)

@pytest.mark.parametrize("code,expected_int", test_inputs)
def test_hash_me(code: str, expected_int: int):
    assert hash_me(code) == expected_int

def test_get_total_focusing_power():
    testing_list = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7".split(',')
    assert get_total_focusing_power(testing_list) == 145
