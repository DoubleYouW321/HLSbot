from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import random

import app.keyboard as kb
from app.database.requests import save_daily_metrics, get_today_metrics, get_user_category

physics_router = Router()

ADVICES = {
    1: 'Вода и мозг. Обезвоживание всего на 2% уже снижает концентрацию и кратковременную память. Стакан воды утром — лучший "будильник" для мозга.',
    2: 'Сон и иммунитет. Во время глубокого сна организм вырабатывает цитокины — белки, которые борются с инфекциями. Хронический недосып = открытые ворота для болезней.',
    3: 'Спорт vs. Стресс. 30 минут быстрой ходьбы не только сжигают калории, но и снижают уровень гормона стресса (кортизола) и повышают уровень эндорфинов.',
    4: 'Осанка и настроение. Сутулость усиливает чувство тревоги и бессилия. Расправьте плечи и поднимите голову на 1 минуту — это сигнализирует мозгу, что вы в безопасности и уверены в себе.',
    5: 'Сила жевания. Тщательное пережевывание пищи (20-30 раз) улучшает пищеварение, помогает контролировать вес и даже снижает стресс, действуя как медитация.',
    6: 'Холодный душ. Краткий холодный душ (30-60 сек) с утра повышает бодрость, ускоряет метаболизм и укрепляет устойчивость к стрессу.',
    7: 'Солнечный витамин D. 15-20 минут на дневном свету (даже в пасмурную погоду) значительно улучшают настроение и регулируют сон благодаря выработке витамина D и серотонина.',
    8: 'Сахарные качели. Быстрые углеводы (сладости, выпечка) вызывают резкий скачок, а затем спад энергии и настроения. Белок и клетчатка дают ровную энергию на часы.',
    9: 'Микро-разминка. 5-минутная разминка каждый час сидячей работы ускоряет обмен веществ на 20% и снижает риски для сердечно-сосудистой системы.', 
    10: 'Мозг на прогулке. Прогулка на свежем воздухе, особенно в зеленых зонах, увеличивает приток крови к префронтальной коре мозга, отвечающей за креативность и решение задач.',
}

class MetricsStates(StatesGroup):
    waiting_for_water = State()
    waiting_for_sleep = State()
    waiting_for_steps = State()

@physics_router.callback_query(F.data == 'physics')
async def cmd_physics(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('В разделе ФИЗИЧЕСКОЕ БЛАГОПОЛУЧИЕ ты можешь получить совет из Базы Знаний, а также записать и редактировать свои физические показатели(кол-во выпитых стаканов воды, часы сна и кол-во пройденных шагов), сравнивая их с норомой.', reply_markup=kb.physics)

@physics_router.callback_query(F.data == 'advice')
async def generate_advice(callback: CallbackQuery):
    await callback.answer('')
    random_adv = random.randint(1, 10)
    advice = ADVICES[random_adv]
    await callback.message.edit_text(advice, reply_markup=kb.back_to_physics)

@physics_router.callback_query(F.data == 'datas')
async def handle_datas_button(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    category = await get_user_category(callback.from_user.id)
    today_metrics = await get_today_metrics(callback.from_user.id)
    if today_metrics and (today_metrics['water_glasses'] > 0 or today_metrics['sleep_hours'] > 0 or today_metrics['steps'] > 0):
        text = f"У тебя уже есть данные за сегодня:\n💧 Вода: {today_metrics['water_glasses']}/{category['water']} стаканов\n😴 Сон: {today_metrics['sleep_hours']}/{category['hours']} часов\n👣 Шаги: {today_metrics['steps']}/{category['steps']}\n\nХочешь обновить данные?"
        await callback.message.edit_text(text, reply_markup=kb.update_metrics)
    else:
        text = f"Твои целевые показатели:\n💧 Вода: {category['water']} стаканов\n😴 Сон: {category['hours']} часов\n👣 Шаги: {category['steps']}\n\nВведи количество выпитых стаканов воды:"
        await callback.message.edit_text(text, reply_markup=kb.cancel_keyboard)
        await state.set_state(MetricsStates.waiting_for_water)

@physics_router.message(MetricsStates.waiting_for_water)
async def process_water_input(message: Message, state: FSMContext):
    try:
        water_glasses = int(message.text)
        if water_glasses < 0:
            raise ValueError
        await state.update_data(water=water_glasses)
        category = await get_user_category(message.from_user.id)
        await message.answer(f"Цель по сну: {category['hours']} часов\nВведи количество часов сна:", reply_markup=kb.cancel_keyboard)
        await state.set_state(MetricsStates.waiting_for_sleep)
    except ValueError:
        await message.answer("Пожалуйста, введи целое число (например: 8):")

@physics_router.message(MetricsStates.waiting_for_sleep)
async def process_sleep_input(message: Message, state: FSMContext):
    try:
        sleep_hours = float(message.text)
        if sleep_hours < 0:
            raise ValueError
        await state.update_data(sleep=sleep_hours)
        category = await get_user_category(message.from_user.id)
        await message.answer(f"Цель по шагам: {category['steps']}\nВведи количество шагов за день:", reply_markup=kb.cancel_keyboard)
        await state.set_state(MetricsStates.waiting_for_steps)
    except ValueError:
        await message.answer("Пожалуйста, введи число (например: 7.5):")

@physics_router.message(MetricsStates.waiting_for_steps)
async def process_steps_input(message: Message, state: FSMContext):
    try:
        steps = int(message.text)
        if steps < 0:
            raise ValueError
        data = await state.get_data()
        metrics = await save_daily_metrics(message.from_user.id, data['water'], data['sleep'], steps)
        category = await get_user_category(message.from_user.id)
        water_status = "✅" if metrics['water_glasses'] >= category['water'] else "❌"
        sleep_status = "✅" if metrics['sleep_hours'] >= category['hours'] else "❌"
        steps_status = "✅" if metrics['steps'] >= category['steps'] else "❌"
        await message.answer(f"✅ Данные сохранены!\n\n{water_status} Вода: {metrics['water_glasses']}/{category['water']} стаканов\n{sleep_status} Сон: {metrics['sleep_hours']}/{category['hours']} часов\n{steps_status} Шаги: {metrics['steps']}/{category['steps']}\n\nДата: {metrics['date']}", reply_markup=kb.back_to_physics)
        await state.clear()
    except ValueError:
        await message.answer("Пожалуйста, введи целое число (например: 10000):")

@physics_router.callback_query(F.data == 'my_metrics')
async def show_my_metrics(callback: CallbackQuery):
    await callback.answer('')
    category = await get_user_category(callback.from_user.id)
    metrics = await get_today_metrics(callback.from_user.id)
    if metrics:
        water_status = "✅" if metrics['water_glasses'] >= category['water'] else "❌"
        sleep_status = "✅" if metrics['sleep_hours'] >= category['hours'] else "❌"
        steps_status = "✅" if metrics['steps'] >= category['steps'] else "❌"
        text = f"📊 Твои показатели за сегодня:\n\n{water_status} Вода: {metrics['water_glasses']}/{category['water']} стаканов\n{sleep_status} Сон: {metrics['sleep_hours']}/{category['hours']} часов\n{steps_status} Шаги: {metrics['steps']}/{category['steps']}\n\nДата: {metrics['date']}"
    else:
        text = f"У тебя еще нет данных за сегодня.\n\nТвои цели:\n💧 Вода: {category['water']} стаканов\n😴 Сон: {category['hours']} часов\n👣 Шаги: {category['steps']}"
    await callback.message.edit_text(text, reply_markup=kb.metrics_actions)

@physics_router.callback_query(F.data == 'cancel_input')
async def cancel_input(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Ввод данных отменен.", reply_markup=kb.physics)
    await callback.answer()

@physics_router.callback_query(F.data == 'update_metrics_confirm')
async def update_metrics_confirm(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    category = await get_user_category(callback.from_user.id)
    await callback.message.edit_text(f"Введи новые данные:\n\nЦелевые показатели:\n💧 Вода: {category['water']} стаканов\n😴 Сон: {category['hours']} часов\n👣 Шаги: {category['steps']}\n\nВведи количество выпитых стаканов воды:", reply_markup=kb.cancel_keyboard)
    await state.set_state(MetricsStates.waiting_for_water)

@physics_router.callback_query(F.data == 'back_to_main_menu')
async def back_to_main_menu(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Выбери категорию:', reply_markup=kb.health)
