import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import os
import random
import json

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return []

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("🎁 Участвовать в розыгрыше", callback_data="join"))
    keyboard.add(InlineKeyboardButton("📜 Условия розыгрыша", callback_data="rules"))
    await message.answer("Добро пожаловать! Выбери действие 👇", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data == "rules")
async def rules(callback: types.CallbackQuery):
    await callback.message.answer("📌 Условия: подпишись на канал и нажми «Участвовать». Победитель будет выбран случайно каждую среду!")

@dp.callback_query_handler(lambda c: c.data == "join")
async def join(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
    if member.status in ["member", "creator", "administrator"]:
        users = load_users()
        if user_id in users:
            await callback.answer("Вы уже участвуете ✅", show_alert=True)
        else:
            users.append(user_id)
            save_users(users)
            await callback.answer("Вы успешно зарегистрированы 🎉", show_alert=True)
    else:
        await callback.answer("Сначала подпишитесь на канал!", show_alert=True)

@dp.message_handler(commands=["розыгрыш"])
async def draw(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    users = load_users()
    if not users:
        await message.reply("❗ Участников нет.")
        return
    winner_id = random.choice(users)
    await message.answer(f"🏆 Победитель: <a href='tg://user?id={winner_id}'>участник</a>")
    save_users([])

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)