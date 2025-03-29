from project import Portfolio
import project
#pytest test_project.py

p = Portfolio()

def test_init():
    assert p._holdings == []



def test_balance_check():
    assert project.balance_check() != None


def test_call_api():
    assert project.call_api("AAPL") != None


def test_update():
    #backbone of the project
    assert project.update(100) == True

def test_difference():
    assert project.difference(100, 100) == 200
    assert project.difference(-10, 100) ==  90
    assert project.difference(0, 100) == 100
