from aiogram.types import Message
from sqlalchemy import Result
from sqlalchemy.future import select

from bot.AI.GPTChat import GPTChat
from bot.CRUD.message import MessageCRUD
from bot.config.logger import logger
from bot.config.settings import env
from web.config.database import async_session
from web.core.models import User


class Handlers(
    GPTChat,
    MessageCRUD
):
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

        try:
            async with async_session() as session:
                # Get Data
                username: str = message.from_user.username or message.from_user.id
                chat_id: int = message.chat.id

                # Get User by Chat Id
                existing_user: Result = await session.execute(select(User).filter_by(chat_id=chat_id))
                if not existing_user.scalar():
                    # Create User
                    session.add(
                        User(
                            username=username,
                            chat_id=chat_id
                        )
                    )
                    await session.commit()

                    await message.answer(
                        text=f"Hi {username}, I'm AI flower store bot)\n Need any help? Service? Or want to order something?"
                    )
        except Exception as e:
            logger.error(
                f"An unexpected error in Start Handler | {e}"
            )

    async def handle_text_input(
            self,
            message: Message
    ) -> None:
        """
        Any Text Message
        :param message: Default Aiogram Telegram Message
        :type message: Message
        """
        logger.info("\n----Text Input Handler is Starting")
        try:
            async with async_session() as session:
                # Get Data
                input_message: str = message.text
                username: str = message.from_user.username or message.from_user.id
                chat_id: int = message.chat.id

                # Get User
                existing_user: Result = await session.execute(select(User).filter_by(chat_id=chat_id))

                user: User = existing_user.scalar()
                if user:
                    if env("ADMIN_PASSWORD") in list(input_message.split(" ")):
                        if user.admin:
                            user.admin = False

                            # Save
                            await session.commit()

                            await message.answer(
                                text="Disable Admin Status"
                            )

                        elif not user.admin:
                            user.admin = True

                            # Save
                            await session.commit()

                            await message.answer(
                                text="Enable Admin Status"
                            )

                    if user.admin:
                        # Get Dialog
                        previous_messages: list[dict] | None = await self.get_all_messages(
                            session=session,
                            user_id=user.id
                        )

                        # Create Response
                        response: str = await self.create_admin_response(
                            session=session,
                            message=message.text,
                            previous_messages=previous_messages if previous_messages else []
                        )

                        # Answer
                        await message.answer(
                            text=response
                        )

                        # Create Message for Continue Saving Dialog
                        await self.create_message(
                            session=session,
                            user_id=user.id,
                            text=message.text,
                            response=response
                        )
                    else:
                        ...

                else:
                    await message.answer(
                        text=f"No Such User {username} in Database"
                    )
        except Exception as e:
            logger.error(
                f"An unexpected error in Text Input Handler | {e}"
            )
