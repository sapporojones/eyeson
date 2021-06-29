import pytest
from eve_sysstats.__main__ import *

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


def test_name2id(get_name):
    assert name2id(get_name) == sys_id


def test_id2name(get_id):
    assert id2name(get_id) == "1DQ1-A"


def test_getkillsdict():
    test_dict = getkillsdict(sys_id, 1)
    assert len(test_dict) > 0


# def test_fill_lists():
#     test_dict = getkillsdict(sys_id, 1)
#     out_list = fill_lists(test_dict)
#     assert len(out_list) == 1


def test_getjumps():
    assert getjumps(sys_id) >= 0


def test_num_stargates():
    assert num_stargates(sys_id) == 4


def test_getrecentkills():
    assert len(getrecentkills(sys_id)) > 0


def test_timestamper(get_timestamp):
    ts = timestamper(get_timestamp)
    assert "ago" in ts
