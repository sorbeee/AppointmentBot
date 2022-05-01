from aiogram.utils import executor
from create_bot import dp
from handlers import client, admin, other, worker
from SQLScripts import BusinessRepository, WorkerRepository, OwnerRepository, RecordsRepository, ClientRepository, EstimatesRepository


async def on_start(_):
    print('Bot online')
    await BusinessRepository.StartDB(_)
    await WorkerRepository.StartDB(_)
    await OwnerRepository.StartDB(_)
    await RecordsRepository.StartDB(_)
    await ClientRepository.StartDB(_)
    await EstimatesRepository.StartDB(_)
client.reg_handlers_client(dp)
admin.reg_handlers_admin(dp)
worker.reg_handlers_other(dp)
other.reg_handlers_other(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_start)
