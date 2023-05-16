from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message

from src.database.services.repos import UserRepo


async def start_cmd(message: Message, user_db: UserRepo):
    await message.answer('Вітаннячка')
    user = await user_db.get_user(message.from_user.id)
    if not user:
        await user_db.add(user_id=message.from_user.id,
                          full_name=message.from_user.full_name,
                          mention=message.from_user.get_mention()
                          )


def setup(dp: Dispatcher):
    dp.register_message_handler(start_cmd, CommandStart(), state='*')


