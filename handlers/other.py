from aiogram import types, Dispatcher
from keyboards import kb_start
from create_bot import bot

async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Слава Україні🇺🇦 \n' \
                           + '\nЯ - AppointmentBot🤖' \
                           + ' Допоможу тобі потрапити на будь-якій процедури 🦾' \
                           + '\nНапиши у чаті "Допомога" або ж натисніть кнопку з відповідною назвою' \
                           + ' для того, щоб отримати інструкцію з користування ботом' \
                           + '\n\nГарного дня тобі, сонечко 🥰', reply_markup=kb_start)


async def command_help(message: types.Message):
    await bot.send_message(message.from_user.id, 'Інструкція з користування ботом📖\n'\
                                                + '\n\n'\
                                                + 'КОРИСТУВАЧ:\n'\
                                                + 'Нажавши на кнопу "Записатися", ви зможете обрати заклад і людина, до якої ви б хотіли записатися на процедуру\n'\
                                                + 'Вибираєте заклад, людину, вільну годину, при необхідності залишаєте коментар'\
                                                + '\n\n\n'\
                                                + 'АДМІНІСТРАТОР:\n'
                                                + 'Для того, щоб дадати заклад натисніть на кнопку "Завантажити заклад". Щоб показати заклади у яких ви є'
                                                  'адміністратором натисніть "Показати всі заклади"\n')

async def command_back(message: types.Message):
    await message.reply('Так, мій госопдарю', reply_markup=kb_start)

def reg_handlers_other(dp: Dispatcher):
    dp.register_message_handler(command_start, lambda message: 'start' in message.text)
    dp.register_message_handler(command_help, lambda message: 'Допомога' in message.text)
    dp.register_message_handler(command_back, lambda message: 'Назад' in message.text)