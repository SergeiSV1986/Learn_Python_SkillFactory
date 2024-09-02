from aiogram import Router
from aiogram.types import Message, CallbackQuery, InputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData

quiz_router = Router()


class QuizStates(StatesGroup):
    question_1 = State()
    question_2 = State()
    question_3 = State()
    result = State()


class QuizCallbackData(CallbackData, prefix="quiz"):
    answer: str


class RestartQuizCallbackData(CallbackData, prefix="restart"):
    action: str


# Пустой словарь для хранения баллов
user_points = {}

animal_details = {
    'Обезьяна': {
        'image': 'https://animalsglobe.ru/wp-content/uploads/2017/08/makaka-3.jpg',
        'description': 'Обезьяны известны своей игривостью и умом. Они живут в тропических лесах и часто имеют сложные социальные структуры.'
    },
    'Тигр': {
        'image': 'https://www.mos.ru/upload/newsfeed/newsfeed/IMG_6502(1).JPG',
        'description': 'Тигры — это мощные хищники, обитающие в лесах Азии. Они символизируют силу и мужество.'
    },
    'Выдра': {
        'image': 'https://rg.ru/uploads/images/187/94/47/iStock-644032024.jpg',
        'description': 'Выдры — это милые и игривые существа, которые живут в водоемах и любят проводить время в воде.'
    },
    'Ленивец': {
        'image': 'https://cs13.pikabu.ru/post_img/2023/11/07/10/1699379675147451966.jpg',
        'description': 'Ленивцы — это медлительные, но очаровательные существа, которые проводят большую часть времени на деревьях.'
    },
    'Сурикат': {
        'image': 'https://botanika35.ru/uploads/cache/e6/ea/e6eace7dc9d6b0353319d96edb2b95ad.jpg',
        'description': 'Сурикаты — это маленькие и любопытные млекопитающие, живущие в сухих регионах Африки. Они известны своей социальной организацией.'
    },
    'Сивуч': {
        'image': 'https://example.com/sea_lion.jpg',
        'description': 'Сивучи — это морские львы, которые обитают на побережьях северных океанов. Они отличают своей грациозностью и умением плавать.'
    },
}

adoption_program_info = (
    "Присоединяйтесь к нашей программе опеки за животными! Вы можете принять участие в заботе о наших животных и помочь им найти новые дома. "
    "Чтобы узнать больше о программе, посетите наш сайт или свяжитесь с нами напрямую."
)

# Вопросы и их влияние на каждое животное (баллы)
question_1_points = {
    'Обезьяна': 3,
    'Тигр': 1,
    'Сурикат': 2,
}

question_2_points = {
    'Выдра': 3,
    'Тигр': 2,
    'Обезьяна': 1,
}

question_3_points = {
    'Сивуч': 3,
    'Ленивец': 2,
    'Сурикат': 1,
}


@quiz_router.message(Command('quiz'))
async def start_quiz(message: Message, state: FSMContext):
    # Инициализируем баллы для каждого животного
    user_points[message.from_user.id] = {animal: 0 for animal in animal_details.keys()}
    await state.set_state(QuizStates.question_1)
    await message.answer("Где бы вы хотели жить?",
                         reply_markup=get_question_1_keyboard())


@quiz_router.callback_query(QuizCallbackData.filter())
async def handle_quiz_answer(callback: CallbackQuery, callback_data: QuizCallbackData, state: FSMContext):
    current_state = await state.get_state()
    user_id = callback.from_user.id

    if current_state == QuizStates.question_1.state:
        animal = callback_data.answer
        update_points(user_id, {animal: question_1_points[animal]})
        await state.set_state(QuizStates.question_2)
        await callback.message.answer("Какая ваша любимая еда?",
                                      reply_markup=get_question_2_keyboard())

    elif current_state == QuizStates.question_2.state:
        animal = callback_data.answer
        update_points(user_id, {animal: question_2_points[animal]})
        await state.set_state(QuizStates.question_3)
        await callback.message.answer("Как вы предпочитаете отдыхать?",
                                      reply_markup=get_question_3_keyboard())

    elif current_state == QuizStates.question_3.state:
        animal = callback_data.answer
        update_points(user_id, {animal: question_3_points[animal]})
        await state.set_state(QuizStates.result)
        result = get_quiz_result(user_id)
        await callback.message.answer(f"Ваше тотемное животное — {result}!")
        await send_animal_image(callback, result)
        await callback.message.answer("Спасибо за участие!", reply_markup=get_restart_keyboard())
        await callback.message.answer("Если у вас остались вопросы, вы можете связаться с нашим сотрудником.",
                                      reply_markup=get_contact_staff_keyboard())
        await state.clear()


@quiz_router.callback_query(RestartQuizCallbackData.filter())
async def handle_restart(callback: CallbackQuery, callback_data: RestartQuizCallbackData, state: FSMContext):
    if callback_data.action == 'restart':
        await start_quiz(callback.message, state)


async def send_animal_image(callback: CallbackQuery, animal: str):
    details = animal_details.get(animal)
    if details:
        await callback.message.answer_photo(photo=details['image'], caption=details['description'])
        await callback.message.answer(adoption_program_info)


def update_points(user_id: int, points_distribution: dict):
    if user_id not in user_points:
        user_points[user_id] = {animal: 0 for animal in animal_details.keys()}
    for animal, points in points_distribution.items():
        if animal in user_points[user_id]:
            user_points[user_id][animal] += points


def get_quiz_result(user_id: int):
    if user_id not in user_points:
        return None
    return max(user_points[user_id], key=user_points[user_id].get)


def get_question_1_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="В тени деревьев", callback_data=QuizCallbackData(answer='Обезьяна').pack())
    keyboard.button(text="В горах", callback_data=QuizCallbackData(answer='Тигр').pack())
    keyboard.button(text="На открытой местности", callback_data=QuizCallbackData(answer='Сурикат').pack())
    return keyboard.as_markup()


def get_question_2_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Рыба", callback_data=QuizCallbackData(answer='Выдра').pack())
    keyboard.button(text="Мясо", callback_data=QuizCallbackData(answer='Тигр').pack())
    keyboard.button(text="Фрукты", callback_data=QuizCallbackData(answer='Обезьяна').pack())
    return keyboard.as_markup()


def get_question_3_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="В воде, пуская пузыри", callback_data=QuizCallbackData(answer='Сивуч').pack())
    keyboard.button(text="На дереве", callback_data=QuizCallbackData(answer='Ленивец').pack())
    keyboard.button(text="В уютном месте с семьей", callback_data=QuizCallbackData(answer='Сурикат').pack())
    return keyboard.as_markup()


def get_restart_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Попробовать ещё раз?", callback_data=RestartQuizCallbackData(action='restart').pack())
    return keyboard.as_markup()


def get_contact_staff_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Связаться с сотрудником", callback_data="contact_staff")
    return keyboard.as_markup()


@quiz_router.callback_query(lambda c: c.data == "contact_staff")
async def contact_staff(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    result = get_quiz_result(user_id)

    contact_info = (
        "Сотрудник зоопарка: Иван Иванов\n"
        "Электронная почта: ivan.ivanov@example.com\n"
        "Телефон: +7 (999) 123-45-67"
    )

    message_to_staff = (
        f"Пользователь {callback.from_user.full_name} прошел викторину.\n"
        f"Результат: {result}\n"
        f"Телеграм ID: {user_id}"
    )

    # Логика отправки данных сотруднику (например, через API, Email или другой канал)
    # Например, это может быть функция отправки email:
    # send_email_to_staff(subject="Результат викторины", body=message_to_staff)

    await callback.message.answer(
        f"Ваши результаты викторины были отправлены сотруднику. Он свяжется с вами в ближайшее время.\n\n{contact_info}"
    )


def send_email_to_staff(subject, body):
    # Используйте библиотеку smtplib или любой другой способ отправки email.
    pass


from aiogram import Router
from aiogram.types import Message, CallbackQuery, InputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData

quiz_router = Router()


class QuizStates(StatesGroup):
    question_1 = State()
    question_2 = State()
    question_3 = State()
    result = State()


class QuizCallbackData(CallbackData, prefix="quiz"):
    answer: str


class RestartQuizCallbackData(CallbackData, prefix="restart"):
    action: str


# Пустой словарь для хранения баллов
user_points = {}

animal_details = {
    'Обезьяна': {
        'image': 'https://animalsglobe.ru/wp-content/uploads/2017/08/makaka-3.jpg',
        'description': 'Обезьяны известны своей игривостью и умом. Они живут в тропических лесах и часто имеют сложные социальные структуры.'
    },
    'Тигр': {
        'image': 'https://www.mos.ru/upload/newsfeed/newsfeed/IMG_6502(1).JPG',
        'description': 'Тигры — это мощные хищники, обитающие в лесах Азии. Они символизируют силу и мужество.'
    },
    'Выдра': {
        'image': 'https://rg.ru/uploads/images/187/94/47/iStock-644032024.jpg',
        'description': 'Выдры — это милые и игривые существа, которые живут в водоемах и любят проводить время в воде.'
    },
    'Ленивец': {
        'image': 'https://cs13.pikabu.ru/post_img/2023/11/07/10/1699379675147451966.jpg',
        'description': 'Ленивцы — это медлительные, но очаровательные существа, которые проводят большую часть времени на деревьях.'
    },
    'Сурикат': {
        'image': 'https://botanika35.ru/uploads/cache/e6/ea/e6eace7dc9d6b0353319d96edb2b95ad.jpg',
        'description': 'Сурикаты — это маленькие и любопытные млекопитающие, живущие в сухих регионах Африки. Они известны своей социальной организацией.'
    },
    'Сивуч': {
        'image': 'https://example.com/sea_lion.jpg',
        'description': 'Сивучи — это морские львы, которые обитают на побережьях северных океанов. Они отличают своей грациозностью и умением плавать.'
    },
}

adoption_program_info = (
    "Присоединяйтесь к нашей программе опеки за животными! Вы можете принять участие в заботе о наших животных и помочь им найти новые дома. "
    "Чтобы узнать больше о программе, посетите наш сайт или свяжитесь с нами напрямую."
)

# Вопросы и их влияние на каждое животное (баллы)
question_1_points = {
    'Обезьяна': 3,
    'Тигр': 1,
    'Сурикат': 2,
}

question_2_points = {
    'Выдра': 3,
    'Тигр': 2,
    'Обезьяна': 1,
}

question_3_points = {
    'Сивуч': 3,
    'Ленивец': 2,
    'Сурикат': 1,
}


@quiz_router.message(Command('quiz'))
async def start_quiz(message: Message, state: FSMContext):
    # Инициализируем баллы для каждого животного
    user_points[message.from_user.id] = {animal: 0 for animal in animal_details.keys()}
    await state.set_state(QuizStates.question_1)
    await message.answer("Где бы вы хотели жить?",
                         reply_markup=get_question_1_keyboard())


@quiz_router.callback_query(QuizCallbackData.filter())
async def handle_quiz_answer(callback: CallbackQuery, callback_data: QuizCallbackData, state: FSMContext):
    current_state = await state.get_state()
    user_id = callback.from_user.id

    if current_state == QuizStates.question_1.state:
        animal = callback_data.answer
        update_points(user_id, {animal: question_1_points[animal]})
        await state.set_state(QuizStates.question_2)
        await callback.message.answer("Какая ваша любимая еда?",
                                      reply_markup=get_question_2_keyboard())

    elif current_state == QuizStates.question_2.state:
        animal = callback_data.answer
        update_points(user_id, {animal: question_2_points[animal]})
        await state.set_state(QuizStates.question_3)
        await callback.message.answer("Как вы предпочитаете отдыхать?",
                                      reply_markup=get_question_3_keyboard())

    elif current_state == QuizStates.question_3.state:
        animal = callback_data.answer
        update_points(user_id, {animal: question_3_points[animal]})
        await state.set_state(QuizStates.result)
        result = get_quiz_result(user_id)
        await callback.message.answer(f"Ваше тотемное животное — {result}!")
        await send_animal_image(callback, result)
        await callback.message.answer("Спасибо за участие!", reply_markup=get_restart_keyboard())
        await callback.message.answer("Если у вас остались вопросы, вы можете связаться с нашим сотрудником.",
                                      reply_markup=get_contact_staff_keyboard())
        await state.clear()


@quiz_router.callback_query(RestartQuizCallbackData.filter())
async def handle_restart(callback: CallbackQuery, callback_data: RestartQuizCallbackData, state: FSMContext):
    if callback_data.action == 'restart':
        await start_quiz(callback.message, state)


async def send_animal_image(callback: CallbackQuery, animal: str):
    details = animal_details.get(animal)
    if details:
        await callback.message.answer_photo(photo=details['image'], caption=details['description'])
        await callback.message.answer(adoption_program_info)


def update_points(user_id: int, points_distribution: dict):
    if user_id not in user_points:
        user_points[user_id] = {animal: 0 for animal in animal_details.keys()}
    for animal, points in points_distribution.items():
        if animal in user_points[user_id]:
            user_points[user_id][animal] += points


def get_quiz_result(user_id: int):
    if user_id not in user_points:
        return None
    return max(user_points[user_id], key=user_points[user_id].get)


def get_question_1_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="В тени деревьев", callback_data=QuizCallbackData(answer='Обезьяна').pack())
    keyboard.button(text="В горах", callback_data=QuizCallbackData(answer='Тигр').pack())
    keyboard.button(text="На открытой местности", callback_data=QuizCallbackData(answer='Сурикат').pack())
    return keyboard.as_markup()


def get_question_2_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Рыба", callback_data=QuizCallbackData(answer='Выдра').pack())
    keyboard.button(text="Мясо", callback_data=QuizCallbackData(answer='Тигр').pack())
    keyboard.button(text="Фрукты", callback_data=QuizCallbackData(answer='Обезьяна').pack())
    return keyboard.as_markup()


def get_question_3_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="В воде, пуская пузыри", callback_data=QuizCallbackData(answer='Сивуч').pack())
    keyboard.button(text="На дереве", callback_data=QuizCallbackData(answer='Ленивец').pack())
    keyboard.button(text="В уютном месте с семьей", callback_data=QuizCallbackData(answer='Сурикат').pack())
    return keyboard.as_markup()


def get_restart_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Попробовать ещё раз?", callback_data=RestartQuizCallbackData(action='restart').pack())
    return keyboard.as_markup()


def get_contact_staff_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Связаться с сотрудником", callback_data="contact_staff")
    return keyboard.as_markup()


@quiz_router.callback_query(lambda c: c.data == "contact_staff")
async def contact_staff(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    result = get_quiz_result(user_id)

    contact_info = (
        "Сотрудник зоопарка: Иван Иванов\n"
        "Электронная почта: ivan.ivanov@example.com\n"
        "Телефон: +7 (999) 123-45-67"
    )

    message_to_staff = (
        f"Пользователь {callback.from_user.full_name} прошел викторину.\n"
        f"Результат: {result}\n"
        f"Телеграм ID: {user_id}"
    )

    # Логика отправки данных сотруднику (например, через API, Email или другой канал)
    # Например, это может быть функция отправки email:
    # send_email_to_staff(subject="Результат викторины", body=message_to_staff)

    await callback.message.answer(
        f"Ваши результаты викторины были отправлены сотруднику. Он свяжется с вами в ближайшее время.\n\n{contact_info}"
    )


def send_email_to_staff(subject, body):
    # Используйте библиотеку smtplib или любой другой способ отправки email.
    pass
#