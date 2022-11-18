from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from keyboards import inline_commands
from keyboards import currency_list
from keyboards import to_main_menu
from data_base import sql_get_string, sql_get_name, sql_callback_list
from scraping_function import scrap

from create_bot import bot

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMConvert(StatesGroup):
    callback = State()
    value = State()


async def start_command(message: types.Message):
    await message.answer('Привет!\nЯ так понимаю вы хотите узнать у меня курсы валют.',
                         reply_markup=inline_commands)
    await message.delete()


async def show_menu(callback: types.CallbackQuery):
    await callback.message.answer('Главное меню:', reply_markup=inline_commands)
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)


async def help_command(callback: types.CallbackQuery):
    await callback.message.answer('помощи нет - лень писать)')
    await callback.answer()


async def get_courses(callback: types.CallbackQuery):
    await callback.message.answer('Курс какой валюты сказать?', reply_markup=currency_list())
    await callback.answer()
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)


async def get_one_course(callback: types.CallbackQuery):
    data = sql_get_string(callback.data)
    await callback.message.answer(f"Курс валюты '{sql_get_name(callback.data)}':"
                                  f" {scrap(data[0], data[1])} руб.")
    await callback.answer()
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.message.answer('Вернуться в главное меню', reply_markup=to_main_menu)


async def start_states_convert(callback: types.CallbackQuery):
    await FSMConvert.callback.set()
    await callback.message.answer('Какую валюту конвертировать?', reply_markup=currency_list())
    await callback.answer()
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)


async def set_callback(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as dictionary:
        dictionary['callback'] = callback.data
    await callback.message.answer(f"Введите количество валюты '{sql_get_name(callback.data)}':")
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await FSMConvert.next()


async def set_value_and_finish(message: types.Message, state: FSMContext):
    if message.text.replace('.', '', 1).isdigit() or message.text.replace(',', '', 1).isdigit():
        async with state.proxy() as dictionary:
            data = sql_get_string(dictionary['callback'])
            result = round(float(message.text.replace(',', '.')) * float(scrap(data[0], data[1])), 2)
            await message.answer(f"{message.text} единиц валюты '{sql_get_name(dictionary['callback'])}'"
                                 f" экв. {result} руб.")
            await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
            await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id - 1)
            await message.answer('Вернуться в главное меню', reply_markup=to_main_menu)
            await state.finish()

    else:
        await message.answer('Ведите число или число с точкой')
        await message.delete()


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return None
    await state.finish()
    await message.answer('Успешно отменено')


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(cancel_handler, state="*", commands='cancel')
    dp.register_message_handler(cancel_handler, Text(equals='cancel', ignore_case=True), state="*")
    dp.register_message_handler(start_command, commands='start')
    dp.register_callback_query_handler(show_menu, text='menu')
    dp.register_callback_query_handler(help_command, text='help')
    dp.register_callback_query_handler(get_courses, text='get_courses')
    dp.register_callback_query_handler(get_one_course, lambda callback: callback.data
                                                        if callback.data in sql_callback_list() else None)
    dp.register_callback_query_handler(start_states_convert, text='convert_value')
    dp.register_callback_query_handler(set_callback, lambda callback: callback.data
                                                        if callback.data in sql_callback_list() else None,
                                       state=FSMConvert.callback)
    dp.register_message_handler(set_value_and_finish, state=FSMConvert.value)
