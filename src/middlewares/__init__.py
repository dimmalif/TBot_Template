from aiogram import Dispatcher
from sqlalchemy.orm import sessionmaker

from src.middlewares.database import DatabaseMiddleware


def setup(dp: Dispatcher, session_pool: sessionmaker):
    dp.setup_middleware(DatabaseMiddleware(session_pool))