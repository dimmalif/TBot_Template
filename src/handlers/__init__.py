from aiogram import Dispatcher

from src.handlers import private


def setup(dp: Dispatcher):
    private.setup(dp)
