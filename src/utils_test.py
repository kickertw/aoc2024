from utils import ternary_up_to_n_places


def test_ternary_up_to_n_places():
    sut = ternary_up_to_n_places(0, 3)
    assert sut == "000"
