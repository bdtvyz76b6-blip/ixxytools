from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext

import random
import string
import qrcode
import requests

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
# 🔤 Красивый шрифт
# =========================


def bold_text(text):

    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

    fancy = "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳"

    return text.translate(
        str.maketrans(
            normal,
            fancy
        )
    )



def italic_text(text):

    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

    fancy = "𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻"

    return text.translate(
        str.maketrans(
            normal,
            fancy
        )
    )



def circle_text(text):

    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

    fancy = "ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ"

    return text.translate(
        str.maketrans(
            normal,
            fancy
        )
    )



@router.message(lambda m: m.text == "🔤 Текст")
async def text_start(
    message: Message,
    state: FSMContext
):

    await state.set_state(
        ToolsState.text
    )

    await message.answer(
        """
🔤 Генератор шрифтов

Отправь любой текст,
я сделаю красивые варианты ✨
"""
    )



@router.message(ToolsState.text)
async def text_create(
    message: Message,
    state: FSMContext
):

    text = message.text


    await message.answer(
        f"""
✨ Готово:

1️⃣ Жирный

{bold_text(text)}


2️⃣ Курсив

{italic_text(text)}


3️⃣ Кружочки

{circle_text(text)}


4️⃣ Стиль

『 {text} 』


5️⃣ Дизайн

꧁༺ {text} ༻꧂
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
        "🔗 Отправь длинную ссылку, я её сокращу ⚡"
    )



@router.message(ToolsState.link)
async def link_create(
    message: Message,
    state: FSMContext
):

    import requests


    url = message.text


    if not url.startswith("http"):

        await message.answer(
            "❌ Это не похоже на ссылку"
        )

        return


    try:

        result = requests.get(
            "https://is.gd/create.php",
            params={
                "format": "simple",
                "url": url
            },
            timeout=10
        )


        short_url = result.text


        await message.answer(
            f"""
✅ Ссылка сокращена!

🔗 Новая ссылка:

{short_url}
"""
        )


    except Exception as e:

        await message.answer(
            "❌ Ошибка сокращения ссылки"
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
    
    

# =========================
# 🧠 Краткий пересказ
# =========================

@router.message(lambda m: m.text == "🧠 Пересказ")
async def summary_start(
    message: Message,
    state: FSMContext
):

    await state.set_state(
        ToolsState.summary
    )

    await message.answer(
        """
🧠 Краткий пересказ

Отправь длинный текст,
а я выделю главную мысль.
"""
    )


@router.message(ToolsState.summary)
async def summary_make(
    message: Message,
    state: FSMContext
):

    text = message.text


    # разбиваем на предложения
    sentences = text.split(".")


    sentences = [
        s.strip()
        for s in sentences
        if len(s.strip()) > 20
    ]


    if len(sentences) == 0:

        await message.answer(
            "❌ Текст слишком короткий"
        )

        await state.clear()
        return


    # берём первые важные предложения
    result = ". ".join(
        sentences[:3]
    )


    await message.answer(
        f"""
🧠 Главная мысль:

{result}

📌 Кратко: выделено {len(sentences)} предложений.
"""
    )


    await state.clear()