import pytest
import time
from db_crud_users import db_create_user


@pytest.fixture(scope='session')
def tg_id_exists():

    test_user = {
        'id': 25,
        'tg_id': 999,
        'tg_name': 'test user',
        'date': '2025-01-01',
        'keep_data_flag': 0
    }

    db_create_user(test_user)
    return test_user['tg_id']


@pytest.fixture(scope='session')
def tg_id_not_exists():
    user_id = 0
    return user_id

@pytest.fixture(autouse=True)
def calculate_test_duration():
    """Report test durations after each function."""
    start = time.time()
    yield
    stop = time.time()
    delta = stop - start
    print('\ntest duration : {:0.3} seconds'.format(delta))
