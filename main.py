import json
import platform
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import (KeyboardButton, Message)
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from dotenv import dotenv_values
from config import logging_config
from db_crud_users import *
from db_crud_emotes import *


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


@dp.message(Command(commands=['stat', 'стат']))
async def process_command_emote(message: Message):

    total_emotes = db_get_all_user_emotes(db_get_fw_id(message.from_user.id))

    if len(total_emotes) == 0:
        text = ('''У меня нет информации. Возможно вы еще не пользовались выбором эмоций.\n
                Для этого наберите /emote''')
    else:
        text = "Статистика за прошлую неделю:\n" + "\n".join("{}\t{}".format(k, v) for k, v in sorted(total_emotes.items(),
                                                                                    key=lambda t: -t[1]))

    await message.answer(text=text,
                         reply_markup=kb_builder.as_markup(resize_keyboard=True))


@dp.message(F.text.lower().in_([k for k, v in emote_dict.items()]))
async def process_response(message: Message):

    last_emote = 'not found'
    if not db_if_user_exists(message.from_user.id):
        new_user = {
            'tg_id': message.from_user.id,
            'tg_name': message.from_user.first_name,
            'keep_data_flag': 0
        }
        db_create_user(new_user)

    if db_if_keep_data(message.from_user.id):
        user_id = db_get_fw_id(message.from_user.id)
        last_emote = db_get_last_emote(user_id)
        db_create_emote(user_id, message.text)

    deep_emote = emote_dict.get(message.text)

    await message.answer(text=f'''Вы выбрали базовую эмоцию {message.text}.
                \nОттенки этой эмоции: {" ".join(deep_emote.keys())}
                \nПредыдущая эмоция была {" ".join(last_emote)}.'''
                    )

@dp.message(Command(commands=['mood', 'настроение']))
async def process_command_start(message: Message):
    await message.answer(f'''Здесь будет клавиатура со смайликами настроений''')

@dp.message()
async def process_other_answers(message: Message):
    await message.answer('Это я не понимаю\nЧтобы найти эмоцию наберите /emote')


if __name__ == '__main__':
    dp.run_polling(bot)