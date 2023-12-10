import pytest
from .main import AlmanacMap, run, get_min_destination

@pytest.fixture
def almanac_seed_soil():
    almanac = AlmanacMap("seed", "soil")
    almanac.add_ref_from_line("50 98 2")
    almanac.add_ref_from_line("52 50 48")
    return almanac

test_inputs = (
    (50, 52),
    (99, 51),
    (100, 100),
    (53, 55),
    (48, 48),
)
@pytest.mark.parametrize("origin,destination", test_inputs)
def test_almanac_map(almanac_seed_soil: AlmanacMap, origin: int, destination: int):
    assert almanac_seed_soil.get_destination_number(origin) == destination
    assert almanac_seed_soil.get_origin_number(destination) == origin

def test_almanac_read():
    assert run(filename="day05/testing_file.txt") == 35

def test_almanac_is_range():
    assert run(filename="day05/testing_file.txt", is_range=True) == 46

def test_get_min_destination():
    assert get_min_destination(filename="day05/testing_file.txt") == 46