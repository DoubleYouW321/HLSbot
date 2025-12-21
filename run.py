import asyncio

import asyncio

import logging as log
from aiogram import Bot, Dispatcher
from config import TOKEN
from app.handlers import router
from app.physics_handlers import physics_router
from app.psychology_handlers import psychology_router
from app.database.models import async_main

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    await async_main()
    dp.include_router(router)
    dp.include_router(physics_router)
    dp.include_router(psychology_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    log.basicConfig(level=log.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')