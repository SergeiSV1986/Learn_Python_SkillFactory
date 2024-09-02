import logging
from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import CommandStart, Command
from quiz_handler import quiz_router, start_quiz
from animal_data import API_TOKEN

# Инициализация логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Регистрация роутеров
dp.include_router(quiz_router)


@dp.message(Command('start'))
async def start_command(message: Message, state: FSMContext):
    await message.answer("Привет! Давай узнаем, какое у тебя тотемное животное? Начнем викторину!")
    await start_quiz(message,  state)

# Обработка ошибок
@quiz_router.errors()
async def error_handler(update: Message, exception):
    logger.error(f"Update {update} caused error {exception}")
    return True

router = Router()
router.message.register(start_command, CommandStart())
dp.include_router(router)

if __name__ == '__main__':
    dp.run_polling(bot)
