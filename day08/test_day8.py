from .main import run, run_for_ghosts, run_for_ghosts_new

def test_run():
    assert run(filename="day08/testing_file.txt") == 6

def test_run_for_ghosts():
    assert run_for_ghosts(filename="day08/testing_file2.txt") == 6
    assert run_for_ghosts_new(filename="day08/testing_file2.txt") == 6
    