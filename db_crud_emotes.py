import logging
from config import db_path
import sqlite3
from datetime import datetime

logger = logging.getLogger(__name__)

connection = sqlite3.connect(db_path())
cursor = connection.cursor()


def db_create_emote(user_id, emote, mood=0):
    """
        emote_structure = {
            'id': i[0], autogenerated
            'user_id': i[1], // internal fw id
            'emote': text
            'date': now()
            'mood': -1/0/1

    1. update date as of now()
    2. insert data in the tb Emotes"""

    emote_date = datetime.today().isoformat()

    with connection:
        cursor.execute('''INSERT INTO Emotes (user_id, emote_date, emote, mood) VALUES (?, ? , ? , ?)
            ''', (user_id, emote_date, emote, mood))


def db_get_last_emote(user_id):

    with connection:
        cursor_obj = cursor.execute('''SELECT emote FROM Emotes WHERE id = (select max(id) from Emotes where user_id = ?)
            ''', (user_id,))

    return cursor_obj.fetchone()

def db_get_all_user_emotes(user_id, period=0):

    '''return dictionary where key: value -> emote: number '''
    user_emotes = {}
    with connection:
        cursor_obj = cursor.execute('''SELECT emote, count(emote) from Emotes where user_id = ? group by emote
        ''', (user_id,))
        emotes_data = cursor_obj.fetchall()

        for i in range(len(emotes_data)):
            user_emotes.update({emotes_data[i][0]: emotes_data[i][1]})

    return user_emotes
