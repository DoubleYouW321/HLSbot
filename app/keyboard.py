from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

health = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Физическое', callback_data='physics')],
    [InlineKeyboardButton(text='Психологическое', callback_data='psychology')],
    [InlineKeyboardButton(text='Социальное', callback_data='social')],
])

physics = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Совет', callback_data='advice')],
    [InlineKeyboardButton(text='Показатели', callback_data='datas')],
    [InlineKeyboardButton(text='⬅️ Назад в меню', callback_data='back_to_main_menu')],
])

cancel_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='❌ Отмена', callback_data='cancel_input')]
])

update_metrics = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅ Да, обновить', callback_data='update_metrics_confirm')],
    [InlineKeyboardButton(text='❌ Нет, оставить как есть', callback_data='physics')]
])

back_to_physics = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⬅️ Назад', callback_data='physics')]
])

metrics_actions = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='➕ Обновить данные', callback_data='datas')],
    [InlineKeyboardButton(text='📈 Статистика', callback_data='stats')],
    [InlineKeyboardButton(text='⬅️ Назад', callback_data='physics')]
])

psychology = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='SOS(антистресс)', callback_data='sos')],
    [InlineKeyboardButton(text='Дневник настроения', callback_data='happy_diary')],
    [InlineKeyboardButton(text='Навигатор помощи', callback_data='help_navig')],
    [InlineKeyboardButton(text='⬅️ Назад в меню', callback_data='back_to_main_menu')],
])

sos = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='1', callback_data='soss_1')],
    [InlineKeyboardButton(text='2', callback_data='soss_2')],
    [InlineKeyboardButton(text='3', callback_data='soss_3')],
    [InlineKeyboardButton(text='4', callback_data='soss_4')],
    [InlineKeyboardButton(text='⬅️ Назад', callback_data='psychology')],
])

back_to_sos = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⬅️ Назад', callback_data='sos')],
])

mood_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='😊 Отлично', callback_data='mood_happy')],
    [InlineKeyboardButton(text='🙂 Хорошо', callback_data='mood_good')],
    [InlineKeyboardButton(text='😐 Нормально', callback_data='mood_neutral')],
    [InlineKeyboardButton(text='😔 Плохо', callback_data='mood_sad')],
    [InlineKeyboardButton(text='😤 Ужасно', callback_data='mood_angry')],
    [InlineKeyboardButton(text='📊 Моя статистика', callback_data='mood_stats')],
    [InlineKeyboardButton(text='⬅️ Назад', callback_data='psychology')],
])

mood_stats_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='➕ Добавить настроение', callback_data='happy_diary')],
    [InlineKeyboardButton(text='⬅️ Назад к выбору', callback_data='happy_diary')],
])
 
problems = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='1', callback_data='problem_1')],
    [InlineKeyboardButton(text='2', callback_data='problem_2')],
    [InlineKeyboardButton(text='3', callback_data='problem_3')],
    [InlineKeyboardButton(text='4', callback_data='problem_4')],
    [InlineKeyboardButton(text='5', callback_data='problem_5')],
    [InlineKeyboardButton(text='⬅️ Назад', callback_data='psychology')],
])

back_to_navigator = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⬅️ Назад', callback_data='help_navig')],
])