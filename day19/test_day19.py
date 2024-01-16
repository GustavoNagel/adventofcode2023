from .main import run

def test_run():
    assert run(filename="day19/testing_file.txt") == (19114, 167409079868000)
