from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu():

    return ReplyKeyboardMarkup(

        keyboard=[

            [
                KeyboardButton(text="🔐 Пароль"),
                KeyboardButton(text="🔳 QR")
            ],

            [
                KeyboardButton(text="🔤 Текст"),
                KeyboardButton(text="🧠 Пересказ")
            ],

            [
                KeyboardButton(text="🎲 Идея"),
                KeyboardButton(text="👤 Никнейм")
            ],

            [
                KeyboardButton(text="👤 Профиль")
            ]

        ],

        resize_keyboard=True
    )