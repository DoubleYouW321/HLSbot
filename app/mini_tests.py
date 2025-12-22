from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
import app.keyboard as kb
import asyncio
from aiogram.types import FSInputFile

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

mini_tests_router = Router()

class MiniTest1States(StatesGroup):
    waiting_for_answer_1 = State()
    waiting_for_answer_2 = State()
    waiting_for_answer_3 = State()
    waiting_for_answer_4 = State()

class MiniTest2States(StatesGroup):
    waiting_for_answer_1 = State()
    waiting_for_answer_2 = State()
    waiting_for_answer_3 = State()
    waiting_for_answer_4 = State()
    waiting_for_answer_5 = State()

TEST_1_QUESTIONS = [
    "В компании малознакомых людей ты скорее:",
    "После тяжёлого дня тебе больше поможет:",
    "Когда друг рассказывает тебе о своей проблеме, ты:",
    "Для тебя идеальный диалог — это:"
]

TEST_1_OPTIONS = [
    ["а) Включишься в активный разговор, чтобы разрядить обстановку и познакомиться.",
     "б) Будешь наблюдать со стороны, вступая в беседу, только если спросят или тема будет очень близка."],
    ["а) Выговориться другу, проговаривая события и эмоции.",
     "б) Побыть в тишине или послушать, как говорит кто-то другой (подкаст, музыка), чтобы отвлечься."],
    ["а) Часто ловишь себя на мысли, что уже знаешь, что ему посоветовать, и хочешь это озвучить.",
     "б) В основном задаёшь уточняющие вопросы и киваешь, давая ему выговориться."],
    ["а) Энергичный обмен идеями, где мысли летят, как мячик в пинг-понге.",
     "б) Глубокое, неспешное обсуждение одной важной темы, где есть паузы для размышления."]
]

TEST_2_QUESTIONS = [
    "Источник энергии. Откуда у тебя появляется энергия после тяжёлого дня или недели?",
    "Внимание: внутрь или наружу? Где обычно фокус твоего внимания?",
    "Социализация: ширина или глубина?",
    "Процесс мышления: думаю — говорю или говорю — думаю?",
    "Реакция на новую социальную ситуацию (вечеринка, корпоратив)."
]

TEST_2_OPTIONS = [
    ["а) От уединения. Мне нужен тихий вечер наедине с собой (книга, сериал, хобби), чтобы прийти в себя.",
     "б) От общения. Лучший отдых — встретиться с друзьями, сходить на вечеринку или в оживлённое место. Одиночество утомляет."],
    ["а) Внутренний мир. Я много размышляю о своих мыслях, чувствах, идеях, впечатлениях. Мне комфортно в своих размышлениях.",
     "б) Внешний мир. Мне интересны события, люди, действия вокруг. Я легко вовлекаюсь во внешнюю активность, меньше склонен к долгим рефлексиям."],
    ["а) Глубина. У меня немного близких друзей, но с ними очень глубокие и доверительные отношения. Новые знакомства даются с усилием.",
     "б) Ширина. У меня широкий круг общения, много знакомых. Я легко завожу новые контакты, получаю от этого заряд."],
    ["а) Думаю, потом говорю. Я предпочитаю обдумать идею в голове, прежде чем ей поделиться. Часто кажусь «тихим» в группе.",
     "б) Говорю, чтобы думать. Я мыслю вслух, обсуждая и развивая идеи в разговоре. В диалоге мне проще понять, что я на самом деле думаю."],
    ["а) Наблюдаю и адаптируюсь. Я сначала постою в стороне, изучу обстановку, людей. Вхожу в общение постепенно.",
     "б) Включаюсь сразу. Я легко подхожу к людям, начинаю разговор, становлюсь частью активности почти моментально."]
]

@mini_tests_router.callback_query(F.data == 'tests')
async def cmd_tests(callback: CallbackQuery):
    await callback.answer('')
    photo = FSInputFile('images/Tests.jpeg')
    await callback.message.answer_photo(photo=photo)
    await callback.message.answer('''Выбери мини-тест, который тебя интересует: 🧐

1. Ты слушатель или тот, кто говорит? 🗣️👂
2. Ты интроверт или экстраверт? 🌙✨''', reply_markup=kb.tests_menu)

@mini_tests_router.callback_query(F.data == 'test_1')
async def start_test_1(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.set_state(MiniTest1States.waiting_for_answer_1)
    await state.update_data(answers=[], current_question=0, test_type='test_1')
    await ask_test_1_question(callback.message, state)

async def ask_test_1_question(message: Message, state: FSMContext):
    data = await state.get_data()
    current = data.get('current_question', 0)
    
    if current < len(TEST_1_QUESTIONS):
        question = TEST_1_QUESTIONS[current]
        options = TEST_1_OPTIONS[current]
        
        text = f"❓ Вопрос {current + 1}/{len(TEST_1_QUESTIONS)}\n\n{question}\n\n{options[0]}\n{options[1]}"
        
        await message.answer(text, reply_markup=kb.test_answers)
    else:
        await finish_test_1(message, state)

@mini_tests_router.callback_query(MiniTest1States.waiting_for_answer_1, F.data.startswith('answer_'))
@mini_tests_router.callback_query(MiniTest1States.waiting_for_answer_2, F.data.startswith('answer_'))
@mini_tests_router.callback_query(MiniTest1States.waiting_for_answer_3, F.data.startswith('answer_'))
@mini_tests_router.callback_query(MiniTest1States.waiting_for_answer_4, F.data.startswith('answer_'))
async def process_test_1_answer(callback: CallbackQuery, state: FSMContext):
    answer = callback.data.split('_')[1]
    await callback.answer('')
    
    data = await state.get_data()
    answers = data.get('answers', [])
    answers.append(answer)
    current = data.get('current_question', 0) + 1
    
    await state.update_data(answers=answers, current_question=current)
    
    if current == 1:
        await state.set_state(MiniTest1States.waiting_for_answer_2)
    elif current == 2:
        await state.set_state(MiniTest1States.waiting_for_answer_3)
    elif current == 3:
        await state.set_state(MiniTest1States.waiting_for_answer_4)
    
    await ask_test_1_question(callback.message, state)

async def finish_test_1(message: Message, state: FSMContext):
    data = await state.get_data()
    answers = data.get('answers', [])
    
    count_a = answers.count('a')
    count_b = answers.count('b')
    
    if count_a > count_b:
        result = f'''🎯 Твои результаты:

📊 Ответов А: {count_a}
📊 Ответов Б: {count_b}

Преимущественно "ГОВОРИТЬ" 🗣️

Ты — тот, кто готов говорить. Ты оживляешь беседы, не даёшь им заглохнуть, легко делишься идеями.

💡 Твоя зона роста — давать больше пространства другим, практиковать активное слушание (переспрашивать, резюмировать), следить, не перебиваешь ли ты.'''
    
    elif count_b > count_a:
        result = f'''🎯 Твои результаты:

📊 Ответов А: {count_a}
📊 Ответов Б: {count_b}

Преимущественно «СЛУШАТЬ» 👂

Ты — Наблюдатель, Аналитик, Эмпат. Ты улавливаешь нюансы, тонкие эмоции, создаёшь безопасное пространство для других, чтобы они раскрывались.

💡 Твоя зона роста — чаще делиться своим мнением, даже если оно не до конца сформировано, учиться вступать в разговор в шумной компании, ценить свой внутренний мир как не менее важный, чем мир других.'''
    
    else:
        result = f'''🎯 Твои результаты:

📊 Ответов А: {count_a}
📊 Ответов Б: {count_b}

Примерно поровну (Сбалансированный тип) ⚖️

Ты — "Гибкий" собеседник, Адаптер. Ты интуитивно чувствуешь, что сейчас нужнее — говорить или слушать, и подстраиваешься под ситуацию и собеседника.

🎉 Это очень ценный и сильный социальный навык!'''
    
    await message.answer(result, reply_markup=kb.after_test)
    await state.clear()

@mini_tests_router.callback_query(F.data == 'test_2')
async def start_test_2(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.set_state(MiniTest2States.waiting_for_answer_1)
    await state.update_data(answers=[], current_question=0, test_type='test_2')
    await ask_test_2_question(callback.message, state)

async def ask_test_2_question(message: Message, state: FSMContext):
    data = await state.get_data()
    current = data.get('current_question', 0)
    
    if current < len(TEST_2_QUESTIONS):
        question = TEST_2_QUESTIONS[current]
        options = TEST_2_OPTIONS[current]
        
        text = f"❓ Вопрос {current + 1}/{len(TEST_2_QUESTIONS)}\n\n{question}\n\n{options[0]}\n{options[1]}"
        
        await message.answer(text, reply_markup=kb.test_answers)
    else:
        await finish_test_2(message, state)

@mini_tests_router.callback_query(MiniTest2States.waiting_for_answer_1, F.data.startswith('answer_'))
@mini_tests_router.callback_query(MiniTest2States.waiting_for_answer_2, F.data.startswith('answer_'))
@mini_tests_router.callback_query(MiniTest2States.waiting_for_answer_3, F.data.startswith('answer_'))
@mini_tests_router.callback_query(MiniTest2States.waiting_for_answer_4, F.data.startswith('answer_'))
@mini_tests_router.callback_query(MiniTest2States.waiting_for_answer_5, F.data.startswith('answer_'))
async def process_test_2_answer(callback: CallbackQuery, state: FSMContext):
    answer = callback.data.split('_')[1]
    await callback.answer('')
    
    data = await state.get_data()
    answers = data.get('answers', [])
    answers.append(answer)
    current = data.get('current_question', 0) + 1
    
    await state.update_data(answers=answers, current_question=current)
    
    if current == 1:
        await state.set_state(MiniTest2States.waiting_for_answer_2)
    elif current == 2:
        await state.set_state(MiniTest2States.waiting_for_answer_3)
    elif current == 3:
        await state.set_state(MiniTest2States.waiting_for_answer_4)
    elif current == 4:
        await state.set_state(MiniTest2States.waiting_for_answer_5)
    
    await ask_test_2_question(callback.message, state)

async def finish_test_2(message: Message, state: FSMContext):
    data = await state.get_data()
    answers = data.get('answers', [])
    
    count_a = answers.count('a')
    count_b = answers.count('b')
    
    if count_a > count_b:
        result = f'''🎯 Твои результаты:

📊 Ответов А: {count_a}
📊 Ответов Б: {count_b}

Ты интроверт! 🌙

🌟 Твоя «социальная батарея» заряжается в тишине. Активное общение, шумные мероприятия и новые знакомства требуют от тебя значительных энергозатрат.

💖 Чтобы восстановить силы, тебе необходимо время наедине с собой или в спокойной обстановке с близким человеком.

🤝 Тебе комфортнее и ценнее иметь несколько по-настоящему близких и доверительных отношений, чем широкий круг поверхностных знакомств.'''
    
    elif count_b > count_a:
        result = f'''🎯 Твои результаты:

📊 Ответов А: {count_a}
📊 Ответов Б: {count_b}

Ты экстраверт! ✨

⚡ Ты черпаешь энергию из внешнего мира: новых знакомств, групповой активности. Длительное одиночество может тебя утомлять.

💬 Ты часто мыслишь вслух, легко включаешься в новые социальные ситуации и оживляешь атмосферу вокруг себя.

🚀 Твоя суперсила — в коммуникабельности, инициативности и умении быстро адаптироваться!'''
    
    else:
        result = f'''🎯 Твои результаты:

📊 Ответов А: {count_a}
📊 Ответов Б: {count_b}

Ты амбиверт! 🔄

🔄 Тебе может нравиться быть в центре внимания на вечеринке, а на следующий день с таким же удовольствием ты проведёшь время в полном уединении.

🎭 Ты гибко адаптируешься к ситуации: в комфортной среде можешь проявлять черты экстраверта, а в незнакомой — наблюдать и анализировать, как интроверт.

🌈 Твоя суперсила — в универсальности и умении находить общий язык с разными людьми!'''
    
    await message.answer(result, reply_markup=kb.after_test)
    await state.clear()

@mini_tests_router.callback_query(F.data == 'back_to_tests')
async def back_to_tests_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer('')
    await callback.message.answer('Выбери мини-тест:', reply_markup=kb.tests_menu)