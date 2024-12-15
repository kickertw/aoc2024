from src.utils import find_number_in_string


def test_find_number_in_string():
    sut = find_number_in_string("1cannonsToTheLeft")
    assert sut == ("1", 0)
