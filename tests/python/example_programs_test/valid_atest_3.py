from valid_code_3 import medianas

def test_one():
    a = 1
    b = 2
    c = 3
    res = medianas(a, b, c)
    assert res == 2

def test_two():
    a = 2
    b = 1
    c = 3
    res = medianas(a, b, c)
    assert res == 2

def test_three():
    a = 3
    b = 1
    c = 2
    res = medianas(a, b, c)
    assert res == 2