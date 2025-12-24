import asyncio

import logging as log
from aiogram import Bot, Dispatcher
from config import TOKEN
from app.handlers import router
from app.physics_handlers import physics_router
from app.psychology_handlers import psychology_router
from app.social_handlers import social_router
from app.database.models import async_main
from app.mini_tests import mini_tests_router
from app.feedback import feedback_router

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    await async_main()
    dp.include_router(router)
    dp.include_router(physics_router)
    dp.include_router(psychology_router)
    dp.include_router(social_router)
    dp.include_router(mini_tests_router)
    dp.include_router(feedback_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    log.basicConfig(level=log.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')