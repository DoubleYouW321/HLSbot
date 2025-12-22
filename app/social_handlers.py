from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
import app.keyboard as kb
import asyncio
from aiogram.types import FSInputFile

social_router = Router()

pomodoro_timers = {}  

GIDES = {
    1: '''Не бойся, готовься!
Шаг 1. Знай своего «врага»: Волнение — это просто энергия. Перенаправь ее в голос (пусть он будет громче) и в жесты.

Шаг 2. Правило 10 секунд: Первые 10 секунд самые важные. Выучи наизусть ПЕРВУЮ фразу: «Здравствуйте, сегодня я расскажу о...». Сказал ее — дальше пойдет легче.

Шаг 3. Друг, а не враг: Не читай со слайда. Слайд — это картинка для аудитории. ТЫ — главный. Объясняй своими словами.

Шаг 4. Спасательный круг: Если забыл текст — сделай паузу, сделай глоток воды, посмотри в свои заметки. Молчание в 5 секунд кажется вечностью только тебе.

Шаг 5. Фишка от биоэтики: Представь, что ты не просто делишься фактами, а рассказываешь историю, которая может изменить чье-то мнение. Это придает смысл.''',
    2: '''Начни с малого.
Шаг 1: Откройся. Простой улыбки и кивка часто достаточно.

Шаг 2: Найди общее. Это называется «контекст». Говори о том, что вокруг: «Как тебе эта контрольная?», «Классный свитер, где взял?», «Ты тоже ходишь на секцию по...?».

Шаг 3: Используй формулу «Комментарий + Вопрос».
Плохо: «Привет. Чем занимаешься?» (слишком общий).
Отлично: «Привет, я видел, ты здорово нарисовал(а) на ИЗО. Ты давно рисуешь?» (Конкретный комментарий + открытый вопрос).

Шаг 4: Слушай по-настоящему. Не думай, что сказать дальше. Просто слушай ответ. Задай уточняющий вопрос по его словам.

Помни: Большинство людей так же боятся показаться неинтересными. Твое внимание — лучший подарок.''',
    3: '''Отказывать — это навык.

1. Четко и без apologies: «Нет, я не могу» звучит увереннее, чем «Ой, я не знаю, наверное, нет, извини...».

2. Короткое объяснение (если хочешь): «Нет, я не могу, у меня другие планы» (не обязательно вдаваться в детали).

3. Предложи альтернативу (если это друг): «Я не могу пойти сегодня гулять, но давай завтра после школы?»

4. Фраза-щит от давления: Если продолжают уговаривать, повтори спокойно и твердо: «Я уже сказал(а) «нет».»

5. Философская основа (от партнеров): Уважение к своим границам — первый шаг к уважению себя. Тот, кто злится на твое «нет», скорее всего, хотел воспользоваться твоим «да»''',
}

@social_router.callback_query(F.data == 'social')
async def cmd_social(callback: CallbackQuery):
    await callback.answer('')
    photo = FSInputFile('images\social.jpeg')
    await callback.message.answer_photo(photo=photo)
    await callback.message.answer(
        '''В разделе Социальное Благополучие ты можешь включить таймер Pomodoro для лучшей фокусировки и работоспособности, пройти мини-тесты которые помогут тебе узнать многое о социальной стороне твоей личность. И почитать гайды из библиотеки soft skills.
                                     
Выбери интересующий тебя раздел''',
        reply_markup=kb.social
    )
    
@social_router.callback_query(F.data == 'timer')
async def cmd_pomodoro_menu(callback: CallbackQuery):
    await callback.answer('')
    photo = FSInputFile('images\Timer.jpeg')
    await callback.message.answer_photo(photo=photo)
    await callback.message.answer(
        '''Таймер Помодоро — это инструмент в рамках техники тайм-менеджмента «Pomodoro», который помогает сфокусироваться на задаче, разделяя работу на короткие интервалы по 25 минут (это «помидор»), за которыми следуют 5-минутные перерывы. После четырех таких «помидоров» делается более длительный перерыв (15 минут).''',
        reply_markup=kb.pomodoro
    )
    
@social_router.callback_query(F.data == 'timer_start')
async def cmd_pomodoro_start(callback: CallbackQuery, bot: Bot):
    await callback.answer('Таймер запущен...')
    
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    
    if user_id in pomodoro_timers and pomodoro_timers[user_id]['is_running']:
        await callback.message.answer(
            '⚠️ У вас уже есть запущенный таймер Pomodoro! Сначала остановите текущий таймер.',
            reply_markup=kb.stop_timer
        )
        return
    
    pomodoro_timers[user_id] = {
        'is_running': True,
        'cycles': 0,
        'task': None,
        'chat_id': chat_id
    }
    
    await callback.message.answer(
        '🍅 **Таймер Pomodoro запущен!**\n\n25 минут работы начались...\nСледите за уведомлениями о перерывах! ✅',
        reply_markup=kb.stop_timer
    )
    
    task = asyncio.create_task(pomodoro_worker(user_id, chat_id, bot))
    pomodoro_timers[user_id]['task'] = task

async def pomodoro_worker(user_id: int, chat_id: int, bot: Bot):
    try:
        while user_id in pomodoro_timers and pomodoro_timers[user_id]['is_running']:
            work_time = 25 * 60
            
            await bot.send_message(
                chat_id=chat_id,
                text=f"🍅 **25 минут работы начались...**\n\nЦикл {pomodoro_timers[user_id]['cycles'] + 1}\nСосредоточься на задаче! ⏱️",
                reply_markup=kb.stop_timer
            )
            
            await asyncio.sleep(work_time)
            
            if not (user_id in pomodoro_timers and pomodoro_timers[user_id]['is_running']):
                break
                
            cycles = pomodoro_timers[user_id]['cycles']
            
            if cycles % 4 == 0 and cycles > 0:
                await bot.send_message(
                    chat_id=chat_id,
                    text=f"✅ **Прошло 4 цикла!**\n\n🍅🍅🍅🍅 Отличная работа!\nВремя для длинного перерыва - 15 минут...\nМожно прогуляться или сделать разминку 🏃‍♂️",
                    reply_markup=kb.stop_timer
                )
                break_time = 15 * 60
            else:
                await bot.send_message(
                    chat_id=chat_id,
                    text=f"✅ **Цикл {cycles + 1} завершен!**\n\nВремя для перерыва - 5 минут...\nОтдохни, разомнись, посмотри в окно 👀",
                    reply_markup=kb.stop_timer
                )
                break_time = 5 * 60
            
            await asyncio.sleep(break_time)
            
            if not (user_id in pomodoro_timers and pomodoro_timers[user_id]['is_running']):
                break

            pomodoro_timers[user_id]['cycles'] += 1
    
    except asyncio.CancelledError:
        pass
    except Exception as e:
        print(f"Ошибка в таймере: {e}")
        try:
            await bot.send_message(
                chat_id=chat_id,
                text="⚠️ Произошла ошибка в работе таймера. Попробуйте запустить заново.",
                reply_markup=kb.pomodoro
            )
        except:
            pass

@social_router.callback_query(F.data == 'timer_stop')
async def cmd_pomodoro_stop(callback: CallbackQuery):
    await callback.answer('Таймер остановлен.')
    
    user_id = callback.from_user.id
    
    if user_id in pomodoro_timers:
        pomodoro_timers[user_id]['is_running'] = False
        
        if pomodoro_timers[user_id]['task']:
            pomodoro_timers[user_id]['task'].cancel()
        
        cycles = pomodoro_timers[user_id]['cycles']
        
        await callback.message.answer(
            f'🛑 **Таймер Pomodoro остановлен.**\n\n✅ Выполнено циклов: {cycles}\n⏱️ Общее время работы: {cycles * 25} минут\n\nОтличная работа! Можете запустить новый таймер когда будете готовы! 🎯',
            reply_markup=kb.pomodoro
        )

        del pomodoro_timers[user_id]
    else:
        await callback.message.answer(
            'ℹ️ У вас нет запущенного таймера Pomodoro.',
            reply_markup=kb.pomodoro
        )

@social_router.callback_query(F.data == 'timer_status')
async def cmd_pomodoro_status(callback: CallbackQuery):
    user_id = callback.from_user.id
    
    if user_id in pomodoro_timers and pomodoro_timers[user_id]['is_running']:
        cycles = pomodoro_timers[user_id]['cycles']
        await callback.message.answer(
            f'📊 **Статус Pomodoro**\n\n✅ Выполнено циклов: {cycles}\n🔄 Текущий цикл: {cycles + 1}\n⏱️ Время работы: {cycles * 25} минут\n\nТаймер активен и работает... 🟢',
            reply_markup=kb.stop_timer
        )
    else:
        await callback.message.answer(
            '📝 У вас нет активного таймера Pomodoro.\n\nНажмите "Запустить таймер" чтобы начать работу по технике Pomodoro.',
            reply_markup=kb.pomodoro
        )

@social_router.callback_query(F.data == 'library')
async def cmd_lib(callback: CallbackQuery):
    await callback.answer('')
    photo = FSInputFile('images\gides.jpeg')
    await callback.message.answer_photo(photo=photo)
    await callback.message.answer('''В библиотеке soft skills ты можешь посмотреть интерсные гайды по ситуация в обществе, которые зачастую вызывают вопросы.
                                     
Выбери интересующий тебя гайд:
1. «Как уверенно выступить с докладом»
2. «Как завести разговор (даже если страшно)»
3. «Как сказать «НЕТ» и не испортить отношения»''', reply_markup=kb.gides)
    
@social_router.callback_query(F.data.startswith('gide'))
async def cmd_lib_answ(callback: CallbackQuery):
    await callback.answer('')
    num = int(callback.data.split('_')[1])
    await callback.message.answer(GIDES[num], reply_markup=kb.back_to_gides)

