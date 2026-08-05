from aiogram import Router
from aiogram.types import Message

from config import ADMIN_ID
from database import users_count


router = Router()



@router.message(
    lambda m: m.text == "/admin"
)
async def admin(
    message: Message
):

    if message.from_user.id != ADMIN_ID:
        await message.answer(
            "❌ Нет доступа"
        )
        return


    await message.answer(

        """
👑 Админ-панель ixxy Tools

📊 Пользователей:
{}
        """.format(
            users_count()
        )

    )