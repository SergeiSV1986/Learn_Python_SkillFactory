from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import CommandStart, Command
from quiz_handler import quiz_router, start_quiz
from adoption_info import adoption_info_router
from animal_data import API_TOKEN

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Регистрация роутеров
dp.include_router(quiz_router)
dp.include_router(adoption_info_router)

@dp.message(Command('start'))
async def start_command(message: Message, state: FSMContext):
    await message.answer("Привет! Давай узнаем, какое у тебя тотемное животное? Начнем викторину!")
    await start_quiz(message,  state)

router = Router()
router.message.register(start_command, CommandStart())
dp.include_router(router)

if __name__ == '__main__':
    dp.run_polling(bot)



