from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.types import FSInputFile

import app.keyboard as kb
import app.database.requests as rq

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    photo = FSInputFile('images/hello.jpg')
    await message.answer_photo(photo=photo)
    await message.answer('''Привет! Ты попал в мир здорового образа жизни, и я твой бот-помощник. 🌿

Я уверен, что благополучие — это баланс трёх главных элементов:
1. Физическое (здоровье, тело) 💪
2. Психологическое (эмоции, ментальное здоровье) 🧠
3. Социальное (обучение, отношения, самореализация) 🤝

Выбери раздел, который интересует тебя в данный момент:''', reply_markup=kb.health)
    
