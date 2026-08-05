from aiogram import Router
from aiogram.types import Message

from database import connect


router = Router()



@router.message(
    lambda m: m.text == "👤 Профиль"
)
async def profile(
    message: Message
):

    db = connect()
    cur = db.cursor()


    cur.execute(
        "SELECT * FROM users WHERE id=?",
        (
            message.from_user.id,
        )
    )


    user = cur.fetchone()

    db.close()



    await message.answer(

        f"""
👤 Профиль

🆔 ID:
{user[0]}

👤 Username:
@{user[1]}

⭐ Тариф:
FREE
        """

    )