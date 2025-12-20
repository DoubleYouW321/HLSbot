from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

health = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Физическое', callback_data='physics')],
    [InlineKeyboardButton(text='Психологическое', callback_data='psychology')],
    [InlineKeyboardButton(text='Социальное', callback_data='social')],
])

physics = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Совет', callback_data='advice')],
    [InlineKeyboardButton(text='Показатели', callback_data='datas')],
    [InlineKeyboardButton(text='Челлендж', callback_data='challendge')],
])