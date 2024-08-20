import aiohttp
import asyncio
from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from googletrans import Translator
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from random import choices

router = Router()
translator = Translator()


class RecipeStates(StatesGroup):
    waiting_for_category = State()
    waiting_for_recipes = State()


@router.message(F.text == "/start")
async def cmd_start(message: Message):
    await message.answer("Добро пожаловать! Используйте команду /category_search_random для поиска рецептов.")


@router.message(F.text.startswith("/category_search_random"))
async def category_search_random(message: Message, state: FSMContext):
    try:
        count = int(message.text.split()[1])
    except (IndexError, ValueError):
        await message.answer("Укажите количество рецептов после команды. Пример: /category_search_random 3")
        return

    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.themealdb.com/api/json/v1/1/categories.php") as response:
            data = await response.json()

    categories = [category["strCategory"] for category in data["categories"]]
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=category, callback_data=category)] for category in categories
    ])

    await message.answer("Выберите категорию:", reply_markup=markup)
    await state.update_data(count=count)
    await state.set_state(RecipeStates.waiting_for_category)


@router.callback_query(RecipeStates.waiting_for_category)
async def category_selected(callback_query, state: FSMContext):
    category = callback_query.data
    data = await state.get_data()
    count = data["count"]

    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://www.themealdb.com/api/json/v1/1/filter.php?c={category}") as response:
            data = await response.json()

    meals = data["meals"]
    selected_meals = choices(meals, k=count)
    meal_ids = [meal["idMeal"] for meal in selected_meals]

    translated_meals = [
        translator.translate(meal["strMeal"], dest='ru').text for meal in selected_meals
    ]

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Показать рецепты", callback_data="show_recipes")]
    ])

    await state.update_data(meal_ids=meal_ids)
    await callback_query.message.answer("Выбранные рецепты:\n" + "\n".join(translated_meals), reply_markup=markup)
    await state.set_state(RecipeStates.waiting_for_recipes)


@router.callback_query(RecipeStates.waiting_for_recipes, F.data == "show_recipes")
async def show_recipes(callback_query, state: FSMContext):
    data = await state.get_data()
    meal_ids = data["meal_ids"]

    async with aiohttp.ClientSession() as session:
        tasks = [
            session.get(f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}")
            for meal_id in meal_ids
        ]
        responses = await asyncio.gather(*tasks)
        meals = [await response.json() for response in responses]

    for meal_data in meals:
        meal = meal_data["meals"][0]
        meal_name = translator.translate(meal["strMeal"], dest='ru').text
        instructions = translator.translate(meal["strInstructions"], dest='ru').text
        ingredients = [
            translator.translate(meal[f"strIngredient{i}"], dest='ru').text for i in range(1, 21) if
            meal[f"strIngredient{i}"]
        ]

        ingredients_str = ", ".join(ingredients)
        message_text = f"{meal_name}\n\nРецепт:\n{instructions}\n\nИнгредиенты: {ingredients_str}"

        await callback_query.message.answer(message_text)

    await state.clear()
