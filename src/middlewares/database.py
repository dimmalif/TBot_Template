from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiogram.types.base import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from src.database.services.repos import UserRepo


class DatabaseMiddleware(LifetimeControllerMiddleware):
    def __init__(self, session_pool: sessionmaker):
        self.session_pool = session_pool
        super().__init__()

    async def pre_process(self, obj: TelegramObject, data: dict, *args):
        session: AsyncSession = self.session_pool()
        data['session'] = session
        data['user_db'] = UserRepo(session)

    async def post_process(self, obj, data, *args):
        if session := data.get('session', None):
            session: AsyncSession
            await session.close()
