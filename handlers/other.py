from aiogram import types, Dispatcher
import json
import string


async def check_message(message : types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation + '№' + string.digits))\
            for i in message.text.split()}.intersection(set(json.load(open('cenz.json')))) != set():
        await message.reply('материться запрещено!')
        await message.delete()
    else:
        await message.answer(f'Ответ "{message.text}" не предусмотрен(')
        await message.delete()


def register_handlers_other(dp : Dispatcher):
    dp.register_message_handler(check_message)
