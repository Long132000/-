from aiogram import executor, types, Bot, Dispatcher

token = '6811851117:AAFE3H8-_rmdJLcJoTW3kjf-yzam1NzCRBQ'
bot = Bot(token=token)
dp = Dispatcher(bot=bot)

@dp.message_handler(commands=['settings'])
async def settings(message: types.Message):
    await message.answer('Настройки вашего бота. Выберите /settings для настройки параметров.')

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer('Привет! Бреусов Денис!')

@dp.message_handler()
async def echo_handler(message: types.Message):
    await message.reply(message.text)

if __name__ == '__main__':
    executor.start_polling(dp)

