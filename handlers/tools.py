from aiogram import Router
from aiogram.types import Message

import random
import string

import qrcode


router = Router()



@router.message(
    lambda m: m.text == "🔐 Пароль"
)
async def password(
    message: Message
):

    chars = (
        string.ascii_letters
        +
        string.digits
        +
        "!@#$%"
    )


    pwd = "".join(
        random.choice(chars)
        for _ in range(16)
    )


    await message.answer(
        f"🔐 Твой пароль:\n\n`{pwd}`",
        parse_mode="Markdown"
    )



@router.message(
    lambda m: m.text == "🔳 QR"
)
async def qr(
    message: Message
):

    await message.answer(
        "Отправь текст или ссылку для QR 👇"
    )



@router.message(
    lambda m: m.text.startswith("http")
)
async def make_qr(
    message: Message
):

    img = qrcode.make(
        message.text
    )


    img.save(
        "qr.png"
    )


    await message.answer_photo(
        open(
            "qr.png",
            "rb"
        )
    )



@router.message(
    lambda m: m.text == "🔤 Текст"
)
async def text_style(
    message: Message
):

    await message.answer(
        "✨ Введи текст:"
    )



@router.message(
    lambda m: m.text == "🔗 Ссылка"
)
async def link(
    message: Message
):

    await message.answer(
        "Отправь ссылку, сделаем короткую 👇"
    )