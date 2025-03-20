import json
import platform
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import (KeyboardButton, Message)
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from dotenv import dotenv_values
from src.fw_logging import logging_config
from src.fw_database_crud import db_read_user
from src.fw_database_crud import db_create_user


logging_config()
logger = logging.getLogger(__name__)
config = dotenv_values(".env")

API_URL = 'https://api.telegram.org/bot'
# development env vs prod
if platform.system() == 'Windows':
    BOT_FW_TOKEN = config['BOT_DEV_TOKEN']
else:
    BOT_FW_TOKEN = config['BOT_FW_TOKEN']

with open('base_emote.json', 'r', encoding='utf-8') as emote_file:
    emote_dict = json.loads(emote_file.read())

'''
        users[message.from_user.id] = {
            id = tg_id
            'previous_emote': None,
            'current_emote': None
            'save_data': 0 | 1
        }
'''
users = {}

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
    if message.from_user.id not in users:
        users[message.from_user.id] = {
            'previous_emote': None,
            'current_emote': None,
            'save_data': 0
        }

@dp.message(Command(commands='emote'))
async def process_command_emote(message: Message):
    await message.answer(text='Базовая эмоция',
                         reply_markup=kb_builder.as_markup(resize_keyboard=True))

@dp.message(F.text.lower().in_([k for k, v in emote_dict.items()]))
async def process_response(message: Message):
    # print(message)
    if db_read_user(message.from_user.id) is None:
        new_user = {
            'tg_id': message.from_user.id,
            'tg_name': message.from_user.first_name,
            'keep_data_flag': 0
        }
        db_create_user(new_user)

    if message.from_user.id not in users:
        users[message.from_user.id] = {
            'previous_emote': None,
            'current_emote': None
        }

    temp = users[message.from_user.id]['current_emote']
    users[message.from_user.id] = {
            'previous_emote': temp,
            'current_emote': message.text
        }

    deep_emote = emote_dict.get(message.text)
    print(deep_emote)

    await message.answer(text=f'''Вы выбрали базовую эмоцию {message.text}.
                \nОттенки этой эмоции: {" ".join(deep_emote.keys())}
                \nПредыдущая эмоция была {temp}. 
                        '''
                         )

@dp.message()
async def process_other_answers(message: Message):
    await message.answer('Это я не понимаю\nЧтобы найти эмоцию наберите /emote')


if __name__ == '__main__':
    dp.run_polling(bot)