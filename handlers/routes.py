from email.mime import message
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
import aiosqlite
from aiogram import Bot
import asyncio

router = Router()


subscribers = set()

async def notifier(bot: Bot):
    while True:
        if subscribers:
            for user_id in list(subscribers):
                try:
                    await bot.send_message(user_id, "Ваше стандартне повідомлення.")
                except Exception:
                    pass

        await asyncio.sleep(10)

@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Привіт\n"
        "Я можу допомогти з розсилкою!\n\n"
        "Команди:\n"
        "/subscribe - підписатися на повідомлення\n"
        "/unsubscribe - відписатися\n"
        "/subscribers_cmd - список підписників"
    )

@router.message(Command("subscribe"))
async def subscribe(message: Message):
    user_id = message.from_user.id

    subscribers.add(user_id)

    await message.answer("Ви підписалися!")


@router.message(Command("unsubscribe"))
async def unsubscribe(message: Message):
    user_id = message.from_user.id

    subscribers.discard(user_id)

    await message.answer("Ви відписалися від підписки.")


@router.message(Command("subscribers_cmd"))
async def subscribers_cmd(message: Message):
    if not subscribers:
        await message.answer("Поки нічого немає")
        return

    text = "Підписники:\n"
    for uid in subscribers:
        text += f"{uid}\n"
    await message.answer(text)