from aiogram import Dispatcher

from src.handlers.private import start


def setup(dp: Dispatcher):
    start.setup(dp)

