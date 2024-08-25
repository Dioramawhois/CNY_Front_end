# telegram_bot.py
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from config import TELEGRAM_BOT_TOKEN, WEB_APP_URL
from db_manager import Database
import logging
import asyncio

# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Инициализация базы данных
db = Database()

@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    web_app_url = f"{WEB_APP_URL}?user_id={user_id}"

    # Проверяем, есть ли пользователь в белом списке
    if db.is_user_in_whitelist(user_id):
        # Создаем клавиатуру с кнопкой для открытия web-приложения
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton(
            text="🕐 Open App",
            web_app=types.WebAppInfo(url=web_app_url)
        )
        keyboard.add(button)

        await message.answer(
            "Нажмите кнопку ниже, чтобы открыть приложение:",
            reply_markup=keyboard
        )
    else:
        await message.answer("Вы не авторизованы для доступа к приложению.")

async def on_startup(dp):
    logging.info("Bot started...")

async def on_shutdown(dp):
    logging.info("Bot stopped...")

def start_bot():
    # Создаем новый event loop для этого потока
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Запускаем бота
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, loop=loop)
