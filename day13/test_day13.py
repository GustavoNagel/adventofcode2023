from .main import run

def test_run():
    assert run(filename="day13/testing_file.txt") == 405

def test_almost_equal_run():
    assert run(filename="day13/testing_file.txt", almost_equal=True) == 400