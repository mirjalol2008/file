import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import API_TOKEN
from database import init_db
from middleware import SubscriptionMiddleware
from handlers import router

async def main():
    init_db()
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.message.middleware(SubscriptionMiddleware())
    dp.callback_query.middleware(SubscriptionMiddleware())
    dp.include_router(router)

    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())