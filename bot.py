import asyncio

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN

from database import create

from handlers import (
    start,
    tools,
    profile,
    admin
)


async def main():

    create()

    bot = Bot(
        BOT_TOKEN
    )

    dp = Dispatcher()


    dp.include_router(
        start.router
    )

    dp.include_router(
        tools.router
    )

    dp.include_router(
        profile.router
    )

    dp.include_router(
        admin.router
    )


    print(
        "✅ ixxy Tools запущен"
    )


    await dp.start_polling(bot)



if __name__ == "__main__":

    asyncio.run(main())