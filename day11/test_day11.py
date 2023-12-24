from .main import run

def test_run():
    assert run(filename="day11/testing_file.txt") == 374

def test_run():
    assert run(filename="day11/testing_file.txt", size=100) == 8410
