from db_crud_users import *

def test_db_read_user():
    temp = db_read_user(333333333) # existing tg_id
    temp_n = db_read_user(0) # non-existing tg_id
    # (3, '333333333', '2025-03-22T21:28:45.220111', 'test user', 0)

    assert temp is not None
    assert temp_n == 'User not found'
    assert len(temp) == 5
    assert type(temp) is tuple
    assert temp[2] > '2025-01-01'


def test_db_get_fw_id():
    temp = db_get_fw_id(333333333) # existing tg_id

    assert temp > 0
    assert type(temp) is int


def test_db_if_keep_data():
    temp = db_if_keep_data(333333333)

    assert temp


def test_db_if_user_exists():
    temp = db_if_user_exists(333333333)
    temp_n = db_if_user_exists(0)

    assert temp
    assert not temp_n

def test_db_read_all_users():
    temp = db_read_all_users()
    assert len(temp) > 1
    assert type(temp) is list