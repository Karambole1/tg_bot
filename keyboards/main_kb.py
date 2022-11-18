from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inline_commands = InlineKeyboardMarkup(row_width=1)

course_button = InlineKeyboardButton(text='Курсы валют', callback_data='get_courses')
convert_button = InlineKeyboardButton(text='Конвертировать валюту', callback_data='convert_value')
help_button = InlineKeyboardButton(text='Помощь', callback_data='help')

inline_commands.add(course_button, convert_button, help_button)

to_main_menu = InlineKeyboardMarkup(row_width=1)

menu_button = InlineKeyboardButton(text='Тык', callback_data='menu')
to_main_menu.add(menu_button)
