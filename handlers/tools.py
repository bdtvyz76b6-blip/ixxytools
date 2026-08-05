from aiogram import Router
from aiogram.types import Message

import random
import string
import qrcode
import aiohttp


router = Router()


# состояния ожидания
waiting_qr = set()
waiting_link = set()
waiting_text = set()


# =========================
# 🔐 Генератор паролей
# =========================

@router.message(lambda m: m.text == "🔐 Пароль")
async def password(message: Message):

    chars = (
        string.ascii_letters
        +
        string.digits
        +
        "!@#$%^&*"
    )

    pwd = "".join(
        random.choice(chars)
        for _ in range(16)
    )

    await message.answer(
        f"🔐 Твой пароль:\n\n`{pwd}`",
        parse_mode="Markdown"
    )


# =========================
# 🔳 QR
# =========================

@router.message(lambda m: m.text == "🔳 QR")
async def qr_button(message: Message):

    waiting_qr.add(
        message.from_user.id
    )

    await message.answer(
        "🔳 Отправь текст или ссылку для QR-кода"
    )


@router.message()
async def qr_create(message: Message):

    user = message.from_user.id

    if user not in waiting_qr:
        return


    img = qrcode.make(
        message.text
    )


    file = f"qr_{user}.png"

    img.save(file)


    waiting_qr.remove(user)


    await message.answer_photo(
        photo=open(
            file,
            "rb"
        ),
        caption="✅ QR-код готов"
    )



# =========================
# 🔗 Ссылка
# =========================

@router.message(lambda m: m.text == "🔗 Ссылка")
async def link_button(message: Message):

    waiting_link.add(
        message.from_user.id
    )

    await message.answer(
        "🔗 Отправь ссылку"
    )


@router.message()
async def shorten_link(message: Message):

    user = message.from_user.id

    if user not in waiting_link:
        return


    try:

        api = (
            "https://tinyurl.com/api-create.php"
            f"?url={message.text}"
        )


        async with aiohttp.ClientSession() as session:

            async with session.get(api) as r:

                result = await r.text()



        waiting_link.remove(user)


        await message.answer(
            f"""
✅ Готово!

🔗 Короткая ссылка:

{result}
"""
        )


    except:

        await message.answer(
            "❌ Ошибка сокращения"
        )



# =========================
# 🔤 Красивый текст
# =========================

@router.message(lambda m: m.text == "🔤 Текст")
async def text_button(message: Message):

    waiting_text.add(
        message.from_user.id
    )

    await message.answer(
        "🔤 Отправь текст"
    )


@router.message()
async def make_text(message: Message):

    user = message.from_user.id

    if user not in waiting_text:
        return


    waiting_text.remove(user)


    await message.answer(
        f"""
✨ Красивый текст:

╭──────╮
 {message.text}
╰──────╯

🔥 {message.text.upper()}
"""
    )



# =========================
# 🎲 Случайное число
# =========================

@router.message(lambda m: m.text == "🎲 Число")
async def random_number(message: Message):

    await message.answer(
        f"🎲 Твоё число: {random.randint(1,100)}"
    )