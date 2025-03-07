from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from dotenv import dotenv_values
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] #%(levelname)-8s %(filename)s:'
           '%(lineno)d - %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)
logger.debug('Лог уровня DEBUG')

config = dotenv_values(".env")

API_URL = 'https://api.telegram.org/bot'
BOT_FW_TOKEN = config['BOT_FW_TOKEN']
'''
Data based on 
https://www.odbtomsk.ru/useful-information/articles-from-the-health-center/795-koleso-emotsij-roberta-plutchika
'''
#\U0001F600 \U0001F622
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

# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands='start'))
async def process_command_start(message: Message):
    await message.answer('Это бот колесо эмоций.\nЧтобы найти эмоцию набери /emote')


@dp.message(Command(commands='emote'))
async def process_command_emote(message: Message):
    await message.answer(text='Базовая эмоция>',
                         reply_markup=kb_builder.as_markup(resize_keyboard=True))

@dp.message(F.text.lower().in_(['грусть', 'грустно']))
async def process_sadness(message: Message):
    await message.answer(text='горе, печаль, задумчивость, сожаление'
        )

@dp.message()
async def process_other_answers(message: Message):
    await message.answer('Это я не понимаю\nЧтобы найти эмоцию набери /emote')


if __name__ == '__main__':
    dp.run_polling(bot)