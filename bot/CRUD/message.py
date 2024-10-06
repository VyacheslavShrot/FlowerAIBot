from sqlalchemy.future import select

from web.core.models import Message


class MessageCRUD:

    async def format_response_for_gpt(
            self,
            messages: list[Message]
    ) -> list[dict]:
        """
        Format Response for GPT History Dialog
        """
        response: list = []

        for message in messages:
            message: Message

            response.append(
                {
                    "user": message.text,
                    "you": message.response
                }
            )

        return response

    async def create_message(
            self,
            session,
            user_id: int,
            text: str,
            response: str
    ) -> None:
        """
        Create Message
        """

        session.add(
            Message(
                user_id=user_id,
                text=text,
                response=response
            )
        )

        await session.commit()

    async def get_all_messages(
            self,
            session,
            user_id: int,
    ) -> list[dict] | None:
        """
        Get ALL User Messages ( Chat History ) by User id and Sort from Old to New Objects
        """

        messages_query = await session.execute(
            select(Message)
            .filter(Message.user_id == user_id)
            .order_by(Message.date.asc())
        )

        messages = messages_query.scalars().all()

        return await self.format_response_for_gpt(
            messages=messages
        ) if messages else None
