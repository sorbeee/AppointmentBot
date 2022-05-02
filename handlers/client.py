from aiogram import types, Dispatcher
from create_bot import bot
from keyboards import client_kb
from SQLScripts import BusinessRepository, WorkerRepository, RecordsRepository, ClientRepository, EstimatesRepository
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta
import re


async def command_client(message: types.Message):
    if await ClientRepository.GetClientById(message.from_user.id):
        await bot.send_message(message.from_user.id, '\tДоброго дня\nОберіть один з запропонованих пунктів',
                               reply_markup=client_kb.kb_client)
    else:
        await bot.send_message(message.from_user.id,
                               '\tДоброго дня\nПеред тим, як перейти до користування ботом, будь ласка, зареєструйтесь',
                               reply_markup=client_kb.kb_reg)


async def command_reg(message: types.Message):
    client_id = message.chat.id
    client_name = message.chat.first_name
    phone_number = message.contact.phone_number

    if await ClientRepository.AddUser(str(client_id), client_name, phone_number):
        await bot.send_message(message.from_user.id, f'Дякуємо за реєстрацію, {client_name}', reply_markup=client_kb.kb_client)


async def command_get_all(message: types.Message):
    data = await BusinessRepository.GetAllBusinesses()
    for ret in data:
        estimate = await EstimatesRepository.GetEstimation(ret[0])
        await bot.send_photo(message.from_user.id, ret[3],
                    f'{ret[2]}\nОПИС: {ret[4]}\nРЕЖИМ РОБОТИ: {ret[5]}\nРейтинг: {estimate[0][0]} / 5  ⭐️',
                    reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton(text='Показати список працівників', callback_data=f'workers {ret[0]}')).add(
                    InlineKeyboardButton(text='Залишити оцінку', callback_data=f'estimation {ret[0]}')))


async def command_show_workers(callback: types.CallbackQuery):
    id = callback.data.replace('workers ', ' ')
    data = await WorkerRepository.GetWorkers(id)

    for ret in data:
        await callback.message.answer_photo(ret[4],
                f'{ret[2]} {ret[3]}\nОПИС: {ret[7]}\nТривалість процедур: {ret[6]}хв.\nНомер телефону: {ret[5]}'
                , reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(text='Записатися', callback_data=f'appointment {ret[0]} {ret[1]}')))

    await callback.answer()


async def command_leave_estimate(callback: types.CallbackQuery):
    id = callback.data.replace('estimation ', ' ')
    kb_client_estimating = InlineKeyboardMarkup(row_width=3)

    b1 = InlineKeyboardButton(text='⭐️', callback_data=f'estimate 1 {str(id)}')
    b2 = InlineKeyboardButton(text='⭐️⭐️', callback_data=f'estimate 2 {str(id)}')
    b3 = InlineKeyboardButton(text='⭐️⭐️⭐️', callback_data=f'estimate 3 {str(id)}')
    b4 = InlineKeyboardButton(text='⭐️⭐️⭐️⭐️', callback_data=f'estimate 4 {str(id)}')
    b5 = InlineKeyboardButton(text='⭐️⭐️⭐️⭐️⭐️', callback_data=f'estimate 5 {str(id)}')
    kb_client_estimating.insert(b1).insert(b2).insert(b3).insert(b4).insert(b5)

    await callback.message.edit_reply_markup(reply_markup=kb_client_estimating)
    await callback.answer()

async def command_estimate_insert(callback: types.CallbackQuery):
    ids = callback.data.replace('estimate ', ' ')
    new_ids = re.split(' ', ids)
    business_id = new_ids[3]
    estimate = new_ids[1]

    if await EstimatesRepository.IsEstimated(business_id, callback.from_user.id):
        if await EstimatesRepository.AddEstimation(estimate, business_id, callback.from_user.id):
            await callback.answer('Дякуєм за вашу оцінку')
        else:
            await callback.answer('Виникли деякі проблеми. Спробуйте, будь ласка, пізніше')
    else:
        if await EstimatesRepository.UpdateEstimation(estimate, business_id, callback.from_user.id):
            await callback.answer('Ми обновили вашу оцінку. Дякуєм за вашу оцінку')
        else:
            await callback.answer('Виникли деякі проблеми. Спробуйте, будь ласка, пізніше')

    await callback.answer()


async def command_appointment_day(callback: types.CallbackQuery):
    id = callback.data.replace('appointment ', ' ')
    kb_client_appointment_day = InlineKeyboardMarkup(row_width=6)

    b0 = InlineKeyboardButton(text='ПН', callback_data=f'day 0 {str(id)}')
    b1 = InlineKeyboardButton(text='ВТ', callback_data=f'day 1 {str(id)}')
    b2 = InlineKeyboardButton(text='СР', callback_data=f'day 2 {str(id)}')
    b3 = InlineKeyboardButton(text='ЧТ', callback_data=f'day 3 {str(id)}')
    b4 = InlineKeyboardButton(text='ПТ', callback_data=f'day 4 {str(id)}')
    b5 = InlineKeyboardButton(text='СБ', callback_data=f'day 5 {str(id)}')
    b6 = InlineKeyboardButton(text='Назад ↩️', callback_data=f'back ')

    kb_client_appointment_day.add(b0)
    kb_client_appointment_day.insert(b1).insert(b2).insert(b3).insert(b4).insert(b5)
    kb_client_appointment_day.add(b6)

    await callback.message.edit_reply_markup(reply_markup=kb_client_appointment_day)
    await callback.answer()


async def command_appointment_hour(callback: types.CallbackQuery):
    ids = callback.data.replace('day ', ' ')
    new_ids = re.split(' ', ids)
    day = new_ids[1]
    today = datetime.now()
    if day >= str(datetime.weekday(today)):
        worker_id = new_ids[3]
        business_id = new_ids[4]
        data = await BusinessRepository.GetBusinessByBusinessId(business_id)
        worker = await WorkerRepository.GetWorkerById(worker_id)
        date = datetime.now() + timedelta((int(day) - int(datetime.weekday(today))))

        work_time = re.split(' - ', data[0][5])
        open_time = datetime.strptime(work_time[0], "%H:%M")
        close_time = datetime.strptime(work_time[1], "%H:%M")

        one_session_time = int(worker[0][6])

        kb = InlineKeyboardMarkup(row_width=3)
        while open_time < close_time:
            sqldate = (str(date.date()) + ' ' + str(open_time.time()))
            if await RecordsRepository.IsBusy(worker_id, sqldate):
                kb.insert(InlineKeyboardButton(f'{open_time.time()}',
                                               callback_data=f'time {str(date.date())} {str(open_time.time())} {worker_id} {business_id}'))
            open_time = open_time + timedelta(minutes=one_session_time)

        kb.add(InlineKeyboardButton(text='Назад ↩️', callback_data=f'back '))
        await callback.message.edit_reply_markup(reply_markup=kb)
        await callback.answer()
    else:
        await callback.answer('Цей день уже минув. Оберіть, будь ласка, інший')


async def command_appointment_insert(callback: types.CallbackQuery):
    data = callback.data.replace('time ', ' ')
    new_data = data.split(' ')

    time = new_data[1] + ' ' + new_data[2]
    worker_id = new_data[3]
    business_id = new_data[4]

    if await RecordsRepository.AddAppointment(worker_id, business_id, callback.from_user.id, time):
        await callback.message.answer(f'Ви успішно записались\n Час: {time}')
    else:
        await callback.answer(f'Ми не змогли вас записати. Виникла помилка')


async def command_back(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.answer()


def reg_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_client, lambda message: 'Клієнт' in message.text)
    dp.register_message_handler(command_reg, content_types=['contact'])
    dp.register_message_handler(command_get_all, lambda message: 'Показати всі заклади' in message.text)
    dp.register_callback_query_handler(command_back, lambda x: x.data and x.data.startswith('back'))
    dp.register_callback_query_handler(command_show_workers, lambda x: x.data and x.data.startswith('workers '))
    dp.register_callback_query_handler(command_appointment_day, lambda x: x.data and x.data.startswith('appointment '))
    dp.register_callback_query_handler(command_appointment_hour, lambda x: x.data and x.data.startswith('day '))
    dp.register_callback_query_handler(command_appointment_insert, lambda x: x.data and x.data.startswith('time '))
    dp.register_callback_query_handler(command_leave_estimate, lambda x: x.data and x.data.startswith('estimation '))
    dp.register_callback_query_handler(command_estimate_insert, lambda x: x.data and x.data.startswith('estimate '))
