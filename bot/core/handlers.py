from aiogram.types import Message

from bot.config.logger import logger
from bot.config.settings import bot


class Handlers:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Handlers, cls).__new__(cls)
            return cls._instance
        if cls._instance:
            raise Exception("Only one instance of Handlers can be created.")

    async def handle_start_command(
            self,
            message: Message
    ) -> None:
        """
        /start Command
        :param message: Default Aiogram Telegram Message
        :type message: Message
        """

        logger.info("\n----Start Command is Starting")

        await message.answer(
            text="Test"
        )
