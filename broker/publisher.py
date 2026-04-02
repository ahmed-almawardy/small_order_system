from aio_pika import connect_robust, Message
import uuid

from settings import settings


async def publish_order(order_dict: str):
    connection = await connect_robust(settings.rabbit_url)
    print("Publisher Connected to RabbitMQ")
    channel = await connection.channel(channel_number=1)
    print(f"Publisher Channel created: {channel}")
    queue = await channel.declare_queue(
        "orders.created", durable=True, auto_delete=False
    )
    print(f"Publisher Queue declared: orders: {queue}")
    await channel.default_exchange.publish(
        routing_key="orders.created",
        message=Message(
            body=order_dict.encode("utf-8"), correlation_id=str(uuid.uuid4())
        ),
    )
