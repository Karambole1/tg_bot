from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_load = KeyboardButton('/add')
button_delete = KeyboardButton('/delete')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(button_load).add(button_delete)
