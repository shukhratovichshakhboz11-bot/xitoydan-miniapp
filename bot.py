
import os
import secrets
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Header, HTTPException
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo,
    Update
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("APP_URL")
RENDER_URL = os.getenv("RENDER_EXTERNAL_URL")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN topilmadi!")

if not APP_URL:
    raise ValueError("APP_URL topilmadi!")

if not RENDER_URL:
    raise ValueError("RENDER_EXTERNAL_URL topilmadi!")

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET") or secrets.token_urlsafe(32)

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


@asynccontextmanager
async def lifespan(app: FastAPI):
    await bot.set_webhook(
        url=f"{RENDER_URL.rstrip('/')}/webhook",
        secret_token=WEBHOOK_SECRET,
        allowed_updates=dp.resolve_used_update_types()
    )
    print("XITOYDAN webhook ishga tushdi!")
    yield
    await bot.session.close()


app = FastAPI(lifespan=lifespan)


@app.get("/healthz")
async def health():
    return {"status": "ok", "bot": "XITOYDAN"}


@app.post("/webhook")
async def webhook(
    request: Request,
    x_telegram_bot_api_secret_token: str = Header(default=None)
):
    if x_telegram_bot_api_secret_token != WEBHOOK_SECRET:
        raise HTTPException(status_code=403, detail="Forbidden")

    data = await request.json()
    update = Update.model_validate(data, context={"bot": bot})
    await dp.feed_update(bot, update)

    return {"ok": True}