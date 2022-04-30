from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from create_bot import bot
from keyboards import kb_admin, kb_admin_downloading, start_kb, kb_admin_time
from SQLScripts import BusinessRepository, WorkerRepository, OwnerRepository, RecordsRepository
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import re
from datetime import datetime


class FSMAdmin1(StatesGroup):
    name = State()
    photo = State()
    description = State()
    time_of_session = State()


# @dp.message_handler(commands=['download'], state=None)
async def cm_start(message: types.Message):
    if await OwnerRepository.IsOwner(message.from_user.id):
        await FSMAdmin1.name.set()
        await message.reply('Введіть назву вашого закладу', reply_markup=kb_admin_downloading)
    else:
        await message.reply('Вийди отсюда, розбійник!!!🤬😡')


# @dp.message_handler(state="*", commands='cancel')
# @dp.message_handler(Text(equals='відмінити', ignore_case=Trure), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    if await OwnerRepository.IsOwner(message.from_user.id):
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('Ok', reply_markup=kb_admin)
    else:
        await message.reply('Вийди отсюда, розбійник!!!🤬😡')


async def load_name(message: types.Message, state: FSMContext):
    if await OwnerRepository.IsOwner(message.from_user.id):
        async with state.proxy() as data:
            data[0] = message.from_user.id
            data[1] = message.text
        await FSMAdmin1.next()
        await message.reply('Тепер вставте фото')
    else:
        await message.reply('Вийди отсюда, розбійник!!!🤬😡')


# @dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    if await OwnerRepository.IsOwner(message.from_user.id):
        async with state.proxy() as data:
            data[2] = message.photo[0].file_id
        await FSMAdmin1.next()
        await message.reply('Тепер введіть опис')
    else:
        await message.reply('Вийди отсюда, розбійник!!!🤬😡')


# @dp.message_handler(state=FSMAdmin.description)
async def load_description(message: types.Message, state: FSMContext):
    if await OwnerRepository.IsOwner(message.from_user.id):
        async with state.proxy() as data:
            data[3] = message.text
        await FSMAdmin1.next()
        await message.reply('Введіть години роботи у форматі HH:MM - HH:MM')
    else:
        await message.reply('Вийди отсюда, розбійник!!!🤬😡')


# @dp.message_handler(state=FSMAdmin.time_of_session)
async def load_duration(message: types.Message, state: FSMContext):
    if await OwnerRepository.IsOwner(message.from_user.id):
        async with state.proxy() as data:
            try:
                work_time = re.split(' - ', message.text)
                open_time = datetime.strptime(work_time[0], "%H:%M")
                close_time = datetime.strptime(work_time[1], "%H:%M")
                data[4] = message.text
            except Exception as _ex:
                print('[INFO] wrong time format')
                await bot.send_message(message.from_user.id, 'Ви ввели неправильний формат часу')

        if (await BusinessRepository.AddBusiness(state)):
            await bot.send_message(message.from_user.id, 'Заклад успішно додано', reply_markup=kb_admin)
        else:
            await bot.send_message(message.from_user.id, 'Cталась помилка. Спробуйте, будь ласка, ще раз пізніше',
                                   reply_markup=kb_admin)
        await state.finish()

    else:
        await message.reply('Вийди отсюда, розбійник!!!🤬😡')


# WORKER
class FSMAdmin2(StatesGroup):
    id = State()
    name = State()
    lastname = State()
    photo = State()
    phone_number = State()
    time_of_session = State()
    description = State()


async def cm_start1(callback: types.CallbackQuery):
    if await OwnerRepository.IsOwner(callback.from_user.id):
        await FSMAdmin2.id.set()
        await callback.message.answer('Введіть введіть id(повинно відповідати id в telegram) працівника', reply_markup=kb_admin_downloading)
    else:
        await callback.answer('Вийди отсюда, розбійник!!!🤬😡')


async def load_worker_id(message: types.Message, state: FSMContext):
    if await OwnerRepository.IsOwner(message.from_user.id):
        async with state.proxy() as data:
            data[0] = message.text
        await FSMAdmin2.next()
        await message.reply('Тепер введіть ім\'я працівника')
    else:
        await message.reply('Вийди отсюда, розбійник!!!🤬😡')


async def load_worker_name(message: types.Message, state: FSMContext):
    if await OwnerRepository.IsOwner(message.from_user.id):
        async with state.proxy() as data:
            id = await BusinessRepository.GetBusinessById(message.from_user.id)
            data[1] = id[0][0]
            data[2] = message.text
        await FSMAdmin2.next()
        await message.reply('Тепер введіть прізвище')
    else:
        await message.reply('Вийди отсюда, розбійник!!!🤬😡')


async def load_worker_lastname(message: types.Message, state: FSMContext):
    if await OwnerRepository.IsOwner(message.from_user.id):
        async with state.proxy() as data:
            data[3] = message.text
        await FSMAdmin2.next()
        await message.reply('Тепер вставте фото')
    else:
        await message.reply('Вийди отсюда, розбійник!!!🤬😡')


async def load_worker_photo(message: types.Message, state: FSMContext):
    if await OwnerRepository.IsOwner(message.from_user.id):
        async with state.proxy() as data:
            data[4] = message.photo[0].file_id
        await FSMAdmin2.next()
        await message.reply('Тепер введіть номер працівника')
    else:
        await message.reply('Вийди отсюда, розбійник!!!🤬😡')


async def load_worker_phone_number(message: types.Message, state: FSMContext):
    if await OwnerRepository.IsOwner(message.from_user.id):
        async with state.proxy() as data:
            data[5] = message.text
        await FSMAdmin2.next()
        await message.reply('Тепер введіть час одного сеансу', reply_markup=kb_admin_time)
    else:
        await message.reply('Вийди отсюда, розбійник!!!🤬😡')


async def load_worker_session_time(message: types.Message, state: FSMContext):
    if await OwnerRepository.IsOwner(message.from_user.id):
        async with state.proxy() as data:
            new_data = message.text.split(' ')
            data[6] = new_data[0]
        await FSMAdmin2.next()
        await message.reply('Тепер введіть опис послуг')
    else:
        await message.reply('Вийди отсюда, розбійник!!!🤬😡')


async def load_worker_description(message: types.Message, state: FSMContext):
    if await OwnerRepository.IsOwner(message.from_user.id):
        async with state.proxy() as data:
            data[7] = message.text

        if (await WorkerRepository.AddWorker(state)):
            await bot.send_message(message.from_user.id, 'Працівника успішно додано', reply_markup=kb_admin)
        else:
            await bot.send_message(message.from_user.id, 'Cталась помилка. Спробуйте, будь ласка, ще раз пізніше',
                                   reply_markup=kb_admin)
        await state.finish()
    else:
        await message.reply('Вийди отсюда, розбійник!!!🤬😡')


async def command_admin(message: types.Message):
    if await OwnerRepository.IsOwner(message.from_user.id):
        await bot.send_message(message.from_user.id, '\tДоброго дня\n Чим можу вам допомогти?', reply_markup=kb_admin)
    else:
        await message.reply('Вийди отсюда, розбійник!!!🤬😡')


async def command_get_businesses(message: types.Message):
    if await OwnerRepository.IsOwner(message.from_user.id):
        data = await BusinessRepository.GetBusinessById(message.from_user.id)
        for ret in data:
            await bot.send_photo(message.from_user.id, ret[3], f'{ret[2]}\nОПИС: {ret[4]}\nРЕЖИМ РОБОТИ: {ret[5]}',
                                 reply_markup=InlineKeyboardMarkup(row_width=2).add(
                                     InlineKeyboardButton(text=f'Додати працівника', callback_data=f'add {ret[0]}')).insert(
                                     InlineKeyboardButton(text=f'Видалити працівника', callback_data=f'del {ret[0]}')).insert(
                                     InlineKeyboardButton(text=f'Видалити заклда', callback_data=f'b_del {ret[0]}')))
            await message.reply(str(ret[0]))
    else:
        await message.reply('Вийди отсюда, розбійник!!!🤬😡')


async def command_delete(callback: types.CallbackQuery):
    if await OwnerRepository.IsOwner(callback.from_user.id):
        id = callback.data.replace('del ', ' ')
        data = await WorkerRepository.GetWorkers(id)

        for ret in data:
            await callback.message.answer_photo(ret[4],
                    f'{ret[2]} {ret[3]}\nОПИС: {ret[7]}\nТривалість процедур: {ret[6]}\nНомер телефону: {ret[5]}',
                    reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text=f'Видалити', callback_data=f'w_del {ret[0]}')))

        await callback.answer()
    else:
        await callback.answer('Вийди отсюда, розбійник!!!🤬😡')


async def command_delete_worker(callback: types.CallbackQuery):
    if await OwnerRepository.IsOwner(callback.from_user.id):
        id = callback.data.replace('w_del ', ' ')
        if await WorkerRepository.DeleteWorker(id):
            await callback.answer('Працівника видалено')
        else:
            await callback.answer('Працівника не видалено\nСпробуйте ще раз пізніше')
    else:
        await callback.answer('Вийди отсюда, розбійник!!!🤬😡')


async def command_delete_business(callback: types.CallbackQuery):
    if await OwnerRepository.IsOwner(callback.from_user.id):
        id = callback.data.replace('b_del ', ' ')
        if await BusinessRepository.DeleteBusiness(id):
            await callback.answer('Заклад видалено')
        else:
            await callback.answer('Заклад не видалено. Спробуйте ще раз пізніше')

        await callback.answer()
    else:
        await callback.answer('Вийди отсюда, розбійник!!!🤬😡')


async def command_back(message: types.Message):
    await message.reply('Так, мій госопдарю', reply_markup=start_kb.kb_start)


def reg_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, Text(equals='Завантажити заклад', ignore_case=True), state=None)
    dp.register_message_handler(cancel_handler, Text(equals='відмінити', ignore_case=True), state="*")
    dp.register_message_handler(cancel_handler, state="*", commands='cancel')
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin1.photo)
    dp.register_message_handler(load_name, state=FSMAdmin1.name)
    dp.register_message_handler(load_description, state=FSMAdmin1.description)
    dp.register_message_handler(load_duration, state=FSMAdmin1.time_of_session)

    dp.register_callback_query_handler(cm_start1, lambda x: x.data and x.data.startswith('add '), state=None)
    dp.register_message_handler(load_worker_id, state=FSMAdmin2.id)
    dp.register_message_handler(load_worker_name, state=FSMAdmin2.name)
    dp.register_message_handler(load_worker_lastname, state=FSMAdmin2.lastname)
    dp.register_message_handler(load_worker_photo, content_types=['photo'], state=FSMAdmin2.photo)
    dp.register_message_handler(load_worker_phone_number, state=FSMAdmin2.phone_number)
    dp.register_message_handler(load_worker_session_time, state=FSMAdmin2.time_of_session)
    dp.register_message_handler(load_worker_description, state=FSMAdmin2.description)

    dp.register_message_handler(command_admin, lambda message: 'Адміністратор' in message.text)
    dp.register_message_handler(command_back, lambda message: 'Назад' in message.text)

    dp.register_message_handler(command_get_businesses, lambda message: 'Показати заклади' in message.text)
    dp.register_callback_query_handler(command_delete, lambda x: x.data and x.data.startswith('del '))
    dp.register_callback_query_handler(command_delete_worker, lambda x: x.data and x.data.startswith('w_del '))
    dp.register_callback_query_handler(command_delete_business, lambda x: x.data and x.data.startswith('b_del '))