from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.types import FSInputFile

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('''Привет, ты попал в мир здорового оброза жизни и я твой бот-помщник.
                            
Я уверен что благополучие это баланс трех главных элементов:
1. Физическое(Здоровье, тело)
2. Психологическое(Эмоции, ментальное здоровье)
3. Социалное(Обучение, отношение, самореализация)
                         
Выбирите раздел, который интересует вас в данный момент''')