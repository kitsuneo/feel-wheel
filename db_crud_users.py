import logging
from config import db_path
import sqlite3
from datetime import datetime

logger = logging.getLogger(__name__)

connection = sqlite3.connect(db_path())
cursor = connection.cursor()

def db_read_user(tg_id: int):
    # check if tg id exists
    with connection:

        cursor_obj = cursor.execute('SELECT * FROM Users WHERE tg_id = ?', (tg_id,))
        found_user = cursor_obj.fetchone()
        return found_user

def db_get_fw_id(tg_id):
    return db_read_user(tg_id)[0]

def db_if_keep_data(tg_id: int):
    return True

def db_if_user_exists(tg_id: int):
    with connection:
        cursor_obj = cursor.execute('SELECT * FROM Users WHERE tg_id = ?', (tg_id,))
        found_users = cursor_obj.fetchall()
        return True if len(found_users) > 0 else False


def db_create_user(new_user: dict):
    """
        temp_dict = {
            'id': i[0],
            'tg_id': i[1],
            'date': i[2],
            'tg_name': i[3],
            'keep_data_flag': i[4] 0 by default - do not keep

    1. search by id, if found -> error - already exists
    2. if not found - match fields to fields
    3. update date as of now()
    4. insert data in the tb Users

    """
    # data for update
    tg_id = new_user['tg_id']
    created_date = datetime.today().isoformat()
    tg_name = new_user['tg_name']
    keep_data_flag = new_user['keep_data_flag']

    with connection:
        cursor.execute('''INSERT INTO Users (tg_id, created_date, tg_name, keep_data_flag) VALUES (?, ? , ? , ?)
            ''', (tg_id, created_date, tg_name, keep_data_flag))


def db_read_all_users():

    with connection:
        cursor.execute('SELECT * FROM Users')
        users_data = cursor.fetchall()

        users = []

        for i in users_data:
            temp_dict = {
                'id': i[0],
                'tg_id': i[1],
                'created_date': i[2],
                'tg_name': i[3],
                'keep_data_flag': i[4]

            }
            users.append(temp_dict)

        return users
