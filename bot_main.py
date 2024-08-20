import asyncio
from aiogram import Bot, Dispatcher
from recipes_handler import router
from token_data import BOT_TOKEN


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Регистрация роутера
    dp.include_router(router)

    # Запуск polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
