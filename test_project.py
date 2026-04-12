
import project
#pytest test_project.py


def test_call_api():
    assert project.call_api("AAPL") != None


