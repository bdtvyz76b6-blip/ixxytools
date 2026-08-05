from aiogram import Router
from aiogram.types import Message

import random
import string
import qrcode


router = Router()

qr_wait = set()


@router.message(lambda m: m.text == "🔐 Пароль")
async def password(message: Message):

    chars = string.ascii_letters + string.digits + "!@#$%"

    pwd = "".join(
        random.choice(chars)
        for _ in range(16)
    )

    await message.answer(
        f"🔐 Пароль:\n\n`{pwd}`",
        parse_mode="Markdown"
    )


@router.message(lambda m: m.text == "🔳 QR")
async def qr_start(message: Message):

    qr_wait.add(message.from_user.id)

    await message.answer(
        "🔳 Отправь текст или ссылку для QR"
    )


@router.message()
async def qr_create(message: Message):

    if message.from_user.id not in qr_wait:
        return

    img = qrcode.make(
        message.text
    )

    img.save("qr.png")

    qr_wait.remove(
        message.from_user.id
    )

    await message.answer_photo(
        photo=open("qr.png", "rb"),
        caption="✅ QR готов"
    )


@router.message(lambda m: m.text == "🔤 Текст")
async def text_tool(message: Message):

    await message.answer(
        "🔤 Напиши текст"
    )


@router.message(lambda m: m.text == "🔗 Ссылка")
async def link_tool(message: Message):

    await message.answer(
        "🔗 Отправь ссылку"
    )