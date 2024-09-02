# results_handler.py
from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("learn_more"))
async def learn_more(message: Message):
    info_text = ("Программа опеки позволяет вам стать частью жизни вашего любимого животного! "
                 "Вы можете помочь нам ухаживать за ним и получать специальные новости и фотографии.")
    await message.answer(info_text)
