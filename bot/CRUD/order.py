from sqlalchemy.future import select

from web.core.models import Order, FlowerOrderAssociation, Flower


class OrderCRUD:

    async def format_response(
            self,
            order: Order
    ) -> dict:
        flowers: list = []

        for flower_assoc in order.flowers:
            flower_assoc: FlowerOrderAssociation

            flowers.append(
                {
                    "title": flower_assoc.flower.title,
                    "price": flower_assoc.flower.price,
                    "count": flower_assoc.flower.count
                }
            )

        return {
            "id": order.id,
            "delivery_time": order.delivery_time,
            "flowers": flowers,
            "count": order.flowers.count,
            "price": order.flowers.price
        }

    async def create_order(
            self,
            session,
            user_id: int,
            flowers: list[dict],
            delivery_time: str
    ) -> dict | None:
        """
        Create Order
        """

        # Init Order with User ID
        order: Order = Order(
            user_id=user_id,
            delivery_time=delivery_time
        )

        for flower_data in flowers:
            flower_title: str = flower_data.get("title", None)
            flower_price: float = flower_data.get("price", None)
            flower_count: int = flower_data.get("count", None)

            # Get One Object
            flower_query = await session.execute(select(Flower).filter_by(title=flower_title))
            flower: Flower = flower_query.scalar()

            if flower:
                flower_order: FlowerOrderAssociation = FlowerOrderAssociation(
                    flower_id=flower.id,
                    price=flower_price,
                    count=flower_count
                )

                order.flowers.append(flower_order)

        await session.add(order)

        await session.commit()

        return await self.format_response(
            order=order
        )
