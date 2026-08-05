from aiogram import Router
from aiogram.types import Message

from database import add_user

from keyboards.menu import main_menu


router = Router()



@router.message(
    lambda m: m.text == "/start"
)
async def start(
    message: Message
):

    add_user(
        message.from_user.id,
        message.from_user.username
    )


    await message.answer(

        """
🔥 Добро пожаловать в ixxy Tools!

Твой набор полезных инструментов:

🔐 Генератор паролей
🔳 QR-коды
🔗 Работа со ссылками
🔤 Красивый текст

Выбирай инструмент 👇
        """,

        reply_markup=main_menu()

    )