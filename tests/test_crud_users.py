from db_crud_users import *

def test_db_read_user(tg_id_exists, tg_id_not_exists):
    temp = db_read_user(tg_id_exists) # existing tg_id
    temp_n = db_read_user(tg_id_not_exists) # non-existing tg_id
    # (3, '999', '2025-03-22T21:28:45.220111', 'test user', 0)

    assert temp is not None
    assert temp_n == 'User not found'
    assert len(temp) == 5
    assert type(temp) is tuple
    assert temp[2] > '2025-01-01'


def test_db_get_fw_id(tg_id_exists, tg_id_not_exists):
    temp = db_get_fw_id(tg_id_exists) # existing tg_id

    assert temp > 0
    assert type(temp) is int


def test_db_if_keep_data(tg_id_exists, tg_id_not_exists):
    temp = db_if_keep_data(tg_id_exists)

    assert temp


def test_db_if_user_exists(tg_id_exists, tg_id_not_exists):
    temp = db_if_user_exists(tg_id_exists)
    temp_n = db_if_user_exists(tg_id_not_exists)

    assert temp
    assert not temp_n

def test_db_read_all_users():
    temp = db_read_all_users()
    assert len(temp) > 1
    assert type(temp) is list