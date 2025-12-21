from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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

# back_to_main = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='⬅️ Назад в меню', callback_data='back_to_main_menu')]
# ])

metrics_actions = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='➕ Обновить данные', callback_data='datas')],
    [InlineKeyboardButton(text='📈 Статистика', callback_data='stats')],
    [InlineKeyboardButton(text='⬅️ Назад', callback_data='physics')]
])