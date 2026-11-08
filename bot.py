
import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo
)
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("APP_URL")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN .env faylida topilmadi!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: Message):
    username = message.from_user.first_name or "Foydalanuvchi"

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🛍 XITOYDAN do‘koniga kirish",
                    web_app=WebAppInfo(url=APP_URL)
                )
            ]
        ]
    )

    await message.answer(
        f"Assalomu alaykum, {username}! 👋\n\n"
        "💜 XITOYDAN do‘koniga xush kelibsiz!\n\n"
        "🇨🇳 Xitoydan O‘zbekistonga buyurtma berish "
        "endi yanada oson!\n\n"
        "Quyidagi tugma orqali do‘konimizga kiring:",
        reply_markup=keyboard
    )


async def main():
    print("XITOYDAN bot ishga tushdi!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())