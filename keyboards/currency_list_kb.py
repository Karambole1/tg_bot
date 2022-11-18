from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data_base import sqlite_db


def currency_list():
    inline_currency_list = InlineKeyboardMarkup(row_width=1)
    tuple_list = sqlite_db.sql_read_to_buttons()
    for tpl in tuple_list:
        inline_currency_list.add(InlineKeyboardButton(text=tpl[0], callback_data=tpl[1]))
    return inline_currency_list


def to_delete_currency():
    inline_currency_list_delete = InlineKeyboardMarkup(row_width=1)
    tuple_list = sqlite_db.sql_read_to_buttons()
    for tpl in tuple_list:
        inline_currency_list_delete.add(InlineKeyboardButton(text=f'Удалить {tpl[0]}', callback_data=f'del {tpl[0]}'))
    return inline_currency_list_delete
