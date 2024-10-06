from aiogram import Dispatcher
from aiogram.filters import Command

from bot.core.handlers import Handlers


def register_handlers(
        dp: Dispatcher,
        handlers: Handlers
) -> None:
    """
    Register Handlers with Instance of Classes
    """
    dp.message.register(handlers.handle_start_command, Command(commands=["start"]))
