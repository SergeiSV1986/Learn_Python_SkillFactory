from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

adoption_info_router = Router()

@adoption_info_router.message(Command('adoption'))
async def show_adoption_info(message: Message):
    await message.answer(
        "Программа опеки в нашем зоопарке — это уникальная возможность поддержать наших животных. "
        "Вы можете стать опекуном и заботиться о выбранном вами животном. "
        "Узнайте больше, нажав на кнопку ниже."
    )
    # Здесь можно добавить кнопку для перехода на сайт с программой опеки.

