from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import logging
from dotenv import dotenv_values
from src.fw_logging import logging_config

logging_config()
logger = logging.getLogger(__name__)
config = dotenv_values(".env")

API_URL = 'https://api.telegram.org/bot'
BOT_FW_TOKEN = config['BOT_FW_TOKEN']

#TODO - move to db/file data
EMOTE_DICT = {'радость':
                {'восторг': 1, 'спокойствие': 1, 'оптимизм': 0, 'любовь': 0},
            'грусть':
                {'горе': 1, 'задумчивость': 1, 'сожаление': 0, 'неодобрение': 0},
            'страх':
                  {},
            'доверие':
                  {},
            'ожидание':
                  {},
            'удивление':
                  {},
            'злость':
                  {},
            'неудовольствие':
                  {}
}

'''
        users[message.from_user.id] = {
            id = /???
            'previous_emote': None,
            'current_emote': None
        }
'''
users = {}


# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_FW_TOKEN)
dp = Dispatcher()

#объект клавиатуры
kb_builder = ReplyKeyboardBuilder()

#генерим кнопки
basic_emote_buttons: list[KeyboardButton] = [
    KeyboardButton(text=f'{k}') for k, v in EMOTE_DICT.items()
    ]

kb_builder.row(*basic_emote_buttons, width=3)

@dp.message(Command(commands=['start', 'help']))
async def process_command_start(message: Message):
    await message.answer('Это бот колесо эмоций.\nЧтобы найти эмоцию наберите /emote')
    if message.from_user.id not in users:
        users[message.from_user.id] = {
            'previous_emote': None,
            'current_emote': None
        }

@dp.message(Command(commands='emote'))
async def process_command_emote(message: Message):
    await message.answer(text='Базовая эмоция>',
                         reply_markup=kb_builder.as_markup(resize_keyboard=True))

@dp.message(F.text.lower().in_([k for k, v in EMOTE_DICT.items()]))
async def process_response(message: Message):
    # print(message)
    if message.from_user.id not in users:
        users[message.from_user.id] = {
            'previous_emote': None,
            'current_emote': None
        }
    print(message.text)
    print(users[message.from_user.id]['current_emote'])
    temp = users[message.from_user.id]['current_emote']

    users[message.from_user.id] = {
            'previous_emote': temp,
        }

    users[message.from_user.id] = {
            'current_emote': message.text
        }

    await message.answer(text=f'Вы выбрали базовую эмоцию {message.text}. Предыдущая эмоция была {temp}'
                         )

@dp.message()
async def process_other_answers(message: Message):
    await message.answer('Это я не понимаю\nЧтобы найти эмоцию наберите /emote')


if __name__ == '__main__':
    dp.run_polling(bot)