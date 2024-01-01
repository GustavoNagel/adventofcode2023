from .main import run

def test_run():
    assert run(filename="day14/testing_file.txt") == 136

def test_run_with_cycles():
    assert run(filename="day14/testing_file.txt", cycles=1_000_000_000) == 64
