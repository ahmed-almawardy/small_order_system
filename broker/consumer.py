from aio_pika import connect_robust
import asyncio
import json

from db.models import Order
from db.repo import update_order
from schemas import OrderSchema
from settings import settings
from db import get_session_context
from sqlalchemy import update


async def consume():
    connection = await connect_robust(settings.rabbit_url)
    print("Consumer Connected to RabbitMQ")
    channel = await connection.channel()
    print(f"Consumer Channel created: {channel}")
    rabbit_queue = await channel.declare_queue(
        "orders.created", durable=True, auto_delete=False
    )
    print(f"Consumer Queue declared: orders: {rabbit_queue}")
    async with rabbit_queue.iterator() as q:
        async for message in q:
            async with message.process():
                message_json = json.loads(message.body)
                print(f"message_json: {message_json}")
                message_json["price"] = float(message_json["price"]) * 2
                message_json = OrderSchema.model_validate(message_json).model_dump()
                print(f"Processed message: {message_json}")
                async with get_session_context() as session:
                    await update_order(
                        session, message_json["id"], {"price": message_json["price"]}
                    )


if __name__ == "__main__":
    asyncio.run(consume())
