from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext

import random
import string
import qrcode

from states import ToolsState


router = Router()


# =========================
# 🔐 Генератор пароля
# =========================

@router.message(lambda m: m.text == "🔐 Пароль")
async def password(message: Message):

    chars = (
        string.ascii_letters
        + string.digits
        + "!@#$%^&*"
    )

    pwd = "".join(
        random.choice(chars)
        for _ in range(16)
    )

    await message.answer(
        f"""
🔐 Новый пароль:

`{pwd}`

Длина: 16 символов
""",
        parse_mode="Markdown"
    )


# =========================
# 🔳 QR код
# =========================

@router.message(lambda m: m.text == "🔳 QR")
async def qr_start(
    message: Message,
    state: FSMContext
):

    await state.set_state(
        ToolsState.qr
    )

    await message.answer(
        """
🔳 QR генератор

Отправь:
• ссылку
• текст
• сообщение

Я сделаю QR-код 👇
"""
    )



@router.message(ToolsState.qr)
async def qr_create(
    message: Message,
    state: FSMContext
):

    try:

        img = qrcode.make(
            message.text
        )


        file = (
            f"qr_{message.from_user.id}.png"
        )


        img.save(file)


        await message.answer_photo(
            photo=FSInputFile(file),
            caption="✅ QR-код готов"
        )


        await state.clear()


    except Exception as e:

        await message.answer(
            f"❌ Ошибка QR:\n{e}"
        )



# =========================
# 🔤 Красивый текст
# =========================

@router.message(lambda m: m.text == "🔤 Текст")
async def text_start(
    message: Message,
    state: FSMContext
):

    await state.set_state(
        ToolsState.text
    )


    await message.answer(
        "🔤 Отправь текст для оформления"
    )



@router.message(ToolsState.text)
async def text_create(
    message: Message,
    state: FSMContext
):

    await message.answer(
        f"""
✨ Красивый текст:

╭──────────╮
 {message.text}
╰──────────╯

🔥 {message.text.upper()}
"""
    )


    await state.clear()



# =========================
# 🔗 Ссылка
# =========================

@router.message(lambda m: m.text == "🔗 Ссылка")
async def link_start(
    message: Message,
    state: FSMContext
):

    await state.set_state(
        ToolsState.link
    )


    await message.answer(
        "🔗 Отправь ссылку"
    )



@router.message(ToolsState.link)
async def link_create(
    message: Message,
    state: FSMContext
):

    await message.answer(
        f"""
🔗 Ссылка получена:

{message.text}

Сокращение добавим следующим обновлением 🚀
"""
    )


    await state.clear()



# =========================
# 🎲 Случайное число
# =========================

@router.message(lambda m: m.text == "🎲 Число")
async def number(
    message: Message
):

    await message.answer(
        f"🎲 Случайное число: {random.randint(1,100)}"
    )