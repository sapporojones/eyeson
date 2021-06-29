import pytest

from src.eyeson import translators
from src.eyeson import core

sys_id = 30004759


@pytest.fixture
def get_id():
    sys_id = 30004759
    return sys_id


@pytest.fixture
def get_name():
    sys_name = "1DQ1-A"
    return sys_name


@pytest.fixture
def get_timestamp():
    timestamp = "2021-06-04T01:25:26Z"
    return timestamp


# def test_fill_lists():
#     test_dict = getkillsdict(sys_id, 1)
#     out_list = fill_lists(test_dict)
#     assert len(out_list) == 1
