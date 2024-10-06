import asyncio
import json
from asyncio import AbstractEventLoop
from functools import partial
from json import JSONDecodeError

import openai
from openai.types.chat import ChatCompletion

from bot.AI.prompts import Prompts
from bot.CRUD.flower import FlowerCRUD
from bot.config.logger import logger
from bot.config.settings import env


class GPTChat(
    FlowerCRUD,
    Prompts
):
    # OpenAI
    OPENAI_API_KEY = env("OPENAI_API_KEY")

    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    async def create_response(
            self
    ):
        self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": ""
                }
            ]
        )

    async def create_admin_response(
            self,
            session,
            message: str,
            previous_messages: list
    ) -> str:
        loop: AbstractEventLoop = asyncio.get_running_loop()

        status: bool = False

        data: list = []

        while not status:
            self.ADMIN_PROMPT.append(
                {
                    "role": "user",
                    "content":
                        f"""
                        1. {previous_messages}
                        2. "{message}"
                        3. {data}
                        """
                }
            )

            create_call: partial = partial(
                self.client.chat.completions.create,
                model="gpt-4o",
                messages=self.ADMIN_PROMPT,
                temperature=1.25
            )

            response: ChatCompletion = await loop.run_in_executor(None, create_call)

            # Get Generated Text
            generated_json_str: str = response.choices[0].message.content
            try:
                # Format to Dict
                generated_json: dict = json.loads(generated_json_str)
            except JSONDecodeError:
                logger.error(f"\n----Invalid String to Format into JSON")
                continue

            response: str = generated_json.get("response", None)
            if response:
                status: bool = True
                return response

            model: str = generated_json.get("model", None)

            # Work with model Flower
            if model == "flower":

                action: str = generated_json.get("action", None)

                title: str = generated_json.get("title", None)
                price: float = generated_json.get("price", None)
                count: int = generated_json.get("count", None)

                # Create Flower Object
                if action == "create":
                    if title and price and int:
                        flower: dict | None = await self.create_flower(
                            session=session,
                            title=title,
                            price=float(price),
                            count=int(count)
                        )
                        if flower:
                            data.append(flower)

                # Get One Flower Object
                if action == "get_one":
                    if title:
                        flower: dict | None = await self.get_one_or_all_flowers(
                            session=session,
                            title=title
                        )
                        if flower:
                            data.append(flower)

                # Get ALL Flowers
                if action == "get_all":
                    flowers: list[dict] | None = await self.get_one_or_all_flowers(
                        session=session
                    )
                    if flowers:
                        for flower in flowers:
                            flower: dict

                            data.append(flower)

                # Update Flower
                if action == "update":
                    if title:
                        flower: dict | None = await self.update_flower(
                            session=session,
                            title=title,
                            price=price,
                            count=count
                        )
                        if flower:
                            data.append(flower)

                # Delete Flower
                if action == "delete":
                    if title:
                        deleted_flower: dict | None = await self.delete_flower(
                            session=session,
                            title=title
                        )
                        if deleted_flower:
                            data.append(deleted_flower)
