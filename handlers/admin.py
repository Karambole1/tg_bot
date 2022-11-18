from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import bot
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from data_base import sql_name_list, sql_callback_list, sql_add_command, sql_delete_button
from keyboards import button_case_admin, to_delete_currency


ID = None


class FSMAdmin(StatesGroup):
    name = State()
    url = State()
    class_to_scrap = State()
    callback = State()


async def if_admin(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, "Модерируйте)", reply_markup=button_case_admin)
    await message.delete()


async def start_states(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.name.set()
        await message.answer('Введите название валюты:')
    else:
        await message.answer('Вы не администратор или не прошли подтверждение')
        await message.delete()


async def set_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        if message.text.title() not in sql_name_list():
            async with state.proxy() as data:
                data['name'] = message.text.title()
            await FSMAdmin.next()
            await message.answer('Теперь введите ссылку на страницу с информацией:')
        else:
            await message.answer('Такое название уже есть\nПопробуйте другое')


async def set_url(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        if message.text.startswith('https://'):
            async with state.proxy() as data:
                data['url'] = message.text
            await FSMAdmin.next()
            await message.answer('Укажите искомый класс:')
        else:
            await message.answer('Обычно ссылка начинается с https://\nПопробуйте снова')


async def set_class(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['class_to_scrap'] = message.text
        await FSMAdmin.next()
        await message.answer('Последнее - укажите соответствующий callback:')


async def set_callback(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        if message.text.title() not in sql_callback_list():
            async with state.proxy() as data:
                data['callback'] = message.text.title()

            await sql_add_command(state)
            await message.answer('Запитсь добавлена')
            await state.finish()
        else:
            await message.answer('Такой callback уже есть\nПопробуйте другой')


async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return None
        await state.finish()
        await message.answer('Успешно отменено')


async def del_note(callback: types.CallbackQuery):
    if callback.data.replace('del ', '') in sql_name_list():
        await sql_delete_button(callback.data.replace('del ', ''))
        await callback.answer(text=f'{callback.data.replace("del ", "")} удален.', show_alert=True)
    else:
        await callback.answer(text=f'{callback.data.replace("del ", "")} уже удален.', show_alert=True)


async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        await message.answer('Выберите, что удалить:', reply_markup=to_delete_currency())
    else:
        await message.answer('Вы не администратор или не прошли подтверждение')
        await message.delete()


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cancel_handler, state="*", commands='cancel')
    dp.register_message_handler(cancel_handler, Text(equals='cancel', ignore_case=True), state="*")
    dp.register_message_handler(start_states, commands=['add'], state=None)
    dp.register_message_handler(delete_item, commands=['delete'], state=None)
    dp.register_callback_query_handler(del_note, lambda x: x.data and x.data.startswith('del '))
    dp.register_message_handler(set_name, state=FSMAdmin.name)
    dp.register_message_handler(set_url, state=FSMAdmin.url)
    dp.register_message_handler(set_class, state=FSMAdmin.class_to_scrap)
    dp.register_message_handler(set_callback, state=FSMAdmin.callback)
    dp.register_message_handler(if_admin, commands=['admin'], is_chat_admin=True)
