import pytest
from .main import sum_part_numbers, sum_gear_ratio


def test_sum_part_numbers():
    assert sum_part_numbers(filename="day03/testing_file.txt") == 4361


def test_sum_gear_ratios():
    assert sum_gear_ratio(filename="day03/testing_file.txt") == 467835
