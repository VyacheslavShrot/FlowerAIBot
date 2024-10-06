from sqlalchemy import delete
from sqlalchemy.ext.baked import Result
from sqlalchemy.future import select

from web.core.models import Flower


class FlowerCRUD:
    FLOWER_RESPONSE_FIELDS: list = [
        "title",
        "price",
        "count"
    ]

    async def format_response(
            self,
            flower: Flower
    ) -> dict:
        """
        Format Flower Response
        """
        response: dict = {field: getattr(flower, field) for field in self.FLOWER_RESPONSE_FIELDS}
        return response

    async def create_flower(
            self,
            session,
            title: str,
            price: float,
            count: int
    ) -> dict | None:
        """
        Create Flower
        """
        existing_flower: Result = await session.execute(select(Flower).filter_by(title=title))
        if not existing_flower.scalar():
            # Create Flower
            session.add(
                Flower(
                    title=title,
                    price=price,
                    count=count
                )
            )
            await session.commit()

            existing_flower: Result = await session.execute(select(Flower).filter_by(title=title))
            flower: Flower = existing_flower.scalar()
            if flower:
                response: dict = await self.format_response(
                    flower=flower
                )
                return response
            else:
                return None
        else:
            return None

    async def get_one_or_all_flowers(
            self,
            session,
            title: str = None,
    ) -> list[dict] | dict | None:
        """
        Get One Flower by Title or ALL Flowers
        """
        formatted_flowers: list = []

        if not title:
            # Get ALL Objects
            flowers_query = await session.execute(select(Flower))
            flowers = flowers_query.scalars().all()

            if flowers:
                for flower in flowers:
                    flower: Flower

                    formatted_flower: dict = await self.format_response(flower)
                    formatted_flowers.append(formatted_flower)
            return formatted_flowers if formatted_flowers else None

        elif title:
            # Get One Object
            flower_query = await session.execute(select(Flower).filter_by(title=title))
            flower: Flower = flower_query.scalar()
            if not flower:
                return None

            return await self.format_response(flower)

        else:
            return None

    async def update_flower(
            self,
            session,
            title: str,
            price: float = None,
            count: int = None
    ) -> dict | None:
        """
        Update Flower by Title
        """
        flower_query = await session.execute(select(Flower).filter_by(title=title))
        flower: Flower = flower_query.scalar()

        if not flower:
            return None

        # Update
        if price is not None:
            flower.price = price
        if count is not None:
            flower.count = count

        # Save
        await session.commit()

        return await self.format_response(flower)

    async def delete_flower(
            self,
            session,
            title
    ) -> dict | None:
        """
        Delete Flower by Title
        """

        # Get One Flower by Title
        flower_query = await session.execute(select(Flower).filter_by(title=title))
        flower: Flower = flower_query.scalar()

        if not flower:
            return None

        # Delete
        await session.execute(delete(Flower).where(Flower.id == flower.id))

        # Save
        await session.commit()

        return {
            "deleted": "success"
        }
