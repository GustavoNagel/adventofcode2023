from .main import run

def test_run():
    assert run(filename="day18/testing_file.txt") == 62

def test_run_using_color():
    assert run(filename="day18/testing_file.txt", fix_instructions_opt=True) == 952408144115
