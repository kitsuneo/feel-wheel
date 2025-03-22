import json
import os
import platform
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import (KeyboardButton, Message)
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from dotenv import dotenv_values
from config import logging_config
from db_crud_users import db_if_user_exists
from db_crud_users import db_create_user
from db_crud_users import db_if_keep_data
from db_crud_users import db_get_fw_id
from db_crud_emotes import db_create_emote

logging_config()
logger = logging.getLogger(__name__)
config = dotenv_values(".env")

API_URL = config['API_URL']
# development env vs prod
if platform.system() == 'Windows':
    BOT_FW_TOKEN = config['BOT_DEV_TOKEN']
else:
    BOT_FW_TOKEN = config['BOT_FW_TOKEN']

with open('base_emote.json', 'r', encoding='utf-8') as emote_file:
    emote_dict = json.loads(emote_file.read())

# keyboard block
bot = Bot(token=BOT_FW_TOKEN)
dp = Dispatcher()

kb_builder = ReplyKeyboardBuilder()

basic_emote_buttons: list[KeyboardButton] = [
    KeyboardButton(text=f'{k}') for k, v in emote_dict.items()
    ]

kb_builder.row(*basic_emote_buttons, width=3)

@dp.message(Command(commands=['start', 'help']))
async def process_command_start(message: Message):
    await message.answer(f'''Это бот колесо эмоций.\nЧтобы найти эмоцию наберите /emote.
            \nСм. https://en.wikipedia.org/wiki/Robert_Plutchik''')

@dp.message(Command(commands='emote'))
async def process_command_emote(message: Message):
    await message.answer(text='Базовая эмоция',
                         reply_markup=kb_builder.as_markup(resize_keyboard=True))

@dp.message(F.text.lower().in_([k for k, v in emote_dict.items()]))
async def process_response(message: Message):
    # print(message)
    if not db_if_user_exists(message.from_user.id):
        new_user = {
            'tg_id': message.from_user.id,
            'tg_name': message.from_user.first_name,
            'keep_data_flag': 0
        }
        db_create_user(new_user)

    if db_if_keep_data(message.from_user.id):
        db_create_emote(db_get_fw_id(message.from_user.id), message.text)

    deep_emote = emote_dict.get(message.text)

    await message.answer(text=f'''Вы выбрали базовую эмоцию {message.text}.
                \nОттенки этой эмоции: {" ".join(deep_emote.keys())}
                \nПредыдущая эмоция была TODO. 
                        '''
                         )

@dp.message()
async def process_other_answers(message: Message):
    await message.answer('Это я не понимаю\nЧтобы найти эмоцию наберите /emote')


if __name__ == '__main__':
    dp.run_polling(bot)