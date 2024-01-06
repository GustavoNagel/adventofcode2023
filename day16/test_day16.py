from .main import run

def test_run():
    assert run(filename="day16/testing_file.txt") == 46

def test_run_maximum():
    assert run(filename="day16/testing_file.txt", maximum=True) == 51
