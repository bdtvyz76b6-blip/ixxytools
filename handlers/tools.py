from aiogram import Router
from aiogram.types import Message

import random
import string
import qrcode
import aiohttp


router = Router()


# =========================
# 🔐 Генератор паролей
# =========================

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
        "!@#$%^&*"
    )

    pwd = "".join(
        random.choice(chars)
        for _ in range(16)
    )


    await message.answer(
        f"""
🔐 Ваш новый пароль:

`{pwd}`

Длина: 16 символов
""",
        parse_mode="Markdown"
    )



# =========================
# 🔳 QR генератор
# =========================

@router.message(
    lambda m: m.text == "🔳 QR"
)
async def qr_start(
    message: Message
):

    await message.answer(
        """
🔳 QR генератор

Отправь мне любой текст или ссылку,
и я сделаю QR-код.
"""
    )



@router.message(
    lambda m:
    m.text
    and
    (
        m.text.startswith("http")
        or
        len(m.text) > 3
    )
)
async def create_qr(
    message: Message
):

    try:

        img = qrcode.make(
            message.text
        )


        file = "qr.png"

        img.save(
            file
        )


        await message.answer_photo(
            photo=open(
                file,
                "rb"
            ),
            caption="✅ QR-код готов"
        )


    except Exception:

        await message.answer(
            "❌ Ошибка создания QR"
        )



# =========================
# 🔤 Красивый текст
# =========================

@router.message(
    lambda m: m.text == "🔤 Текст"
)
async def text_start(
    message: Message
):

    await message.answer(
        """
🔤 Отправь текст,
и я сделаю красивое оформление.
"""
    )



@router.message(
    lambda m:
    m.text
    and
    len(m.text) < 100
)
async def style_text(
    message: Message
):

    if message.text in [
        "🔐 Пароль",
        "🔳 QR",
        "🔗 Ссылка",
        "🔤 Текст",
        "👤 Профиль"
    ]:
        return


    text = message.text


    await message.answer(
        f"""
✨ Красивый текст:

╭───────╮
  {text}
╰───────╯

🔥 {text.upper()}
"""
    )



# =========================
# 🔗 Сокращение ссылок
# =========================

@router.message(
    lambda m: m.text == "🔗 Ссылка"
)
async def link_start(
    message: Message
):

    await message.answer(
        """
🔗 Отправь ссылку,
я сделаю её короче.
"""
    )



@router.message(
    lambda m:
    m.text
    and
    m.text.startswith(
        "http"
    )
)
async def short_link(
    message: Message
):

    try:

        api = (
            "https://tinyurl.com/api-create.php"
            f"?url={message.text}"
        )


        async with aiohttp.ClientSession() as session:

            async with session.get(api) as response:

                result = await response.text()



        await message.answer(
            f"""
✅ Готово!

🔗 Новая ссылка:

{result}
"""
        )


    except Exception:

        await message.answer(
            "❌ Не получилось сократить ссылку"
        )