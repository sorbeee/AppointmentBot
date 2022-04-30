import datetime
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import kb_start, worker_kb
from create_bot import bot
from SQLScripts import WorkerRepository

async def command_start(message: types.Message):
    if len(await WorkerRepository.GetWorkerById(message.from_user.id)) > 0:
        await bot.send_message(message.from_user.id, 'Вітаю. Чим можу вам допомогти?', reply_markup=worker_kb.kb_worker)
    else:
        await message.reply('Ви не є працівником')

async def command_schedule(message: types.Message):
    if len(await WorkerRepository.GetWorkerById(message.from_user.id)) > 0:
        day = message.text.replace('Розклад на ', ' ')
        days =[' сьогодні', ' завтра']
        if day == days[0]:
            time = str(datetime.datetime.now().date()) + ' 00:00:00'
            date = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
            data = await WorkerRepository.GetThisDatSchedule(date, message.from_user.id)
            info = ''
            for ret in data:
                info += f'Час: {ret[3]}\nІм\'я: {ret[5]}\nНомер телефону: {ret[6]}\n\n'
            await message.reply(info)
        elif day == days[1]:
            time = str(datetime.datetime.now().date() + datetime.timedelta(days=1)) + ' 00:00:00'
            date = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
            data = await WorkerRepository.GetThisDatSchedule(date, message.from_user.id)
            info = ''
            for ret in data:
                info += f'Час: {ret[3]}\nІм\'я: {ret[5]}\nНомер телефону: {ret[6]}\n\n'
            await message.reply(info)
    else:
        await message.reply('Ви не є працівником')

class States(StatesGroup):
    start = State()
    date = State()

async def command_current_schedule(message: types.Message):
    if len(await WorkerRepository.GetWorkerById(message.from_user.id)) > 0:
        await States.start.set()
        await message.reply('Введіть дату у форматі "YYYY-MM-DD"')
    else:
        await message.reply('Ви не є працівником')

async def comaand_get_day(message: types.Message, state: FSMContext):
    if len(await WorkerRepository.GetWorkerById(message.from_user.id)) > 0:
        try:
            day = datetime.datetime.strptime(message.text, "%Y-%m-%d")
            await bot.send_message(message.from_user.id, f'{day}')
            data = await WorkerRepository.GetThisDatSchedule(day, message.from_user.id)
            info = ''
            for ret in data:
                info += f'Час: {ret[3]}\nІм\'я: {ret[5]}\nНомер телефону: {ret[6]}\n\n'
            await message.reply(info)
            await state.finish()
        except Exception as _ex:
            print("[INFO] error ", _ex)
    else:
        await message.reply('Ви не є працівником')

async def command_back(message: types.Message):
    await message.reply('Так, мій госопдарю', reply_markup=kb_start)

def reg_handlers_other(dp: Dispatcher):
    dp.register_message_handler(command_start, lambda message: 'Працівник' in message.text )
    dp.register_message_handler(command_back, lambda message: 'Назад' in message.text)
    dp.register_message_handler(command_current_schedule, lambda message: 'Розклад на конкретну дату' in message.text, state=None)
    dp.register_message_handler(comaand_get_day, content_types=['text'], state=States.start)
    dp.register_message_handler(command_schedule, lambda x: x.text and x.text.startswith('Розклад на '))