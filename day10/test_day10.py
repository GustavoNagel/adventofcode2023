from .main import run

def test_run():
    assert run(filename="day10/testing_file.txt") == (8, 1)

def test_run_count_dots():
    assert run(filename="day10/testing_file2.txt")[1] == 4