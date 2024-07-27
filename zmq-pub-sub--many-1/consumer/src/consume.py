import asyncio
import os
import uuid

import zmq.asyncio
from loguru import logger


async def sub(host: str, protocol: str, port: int, consumer_id: bytes) -> None:
    context = zmq.asyncio.Context.instance()
    socket = context.socket(zmq.SUB)
    socket.bind(f"{protocol}://*:{port}")
    socket.setsockopt(zmq.SUBSCRIBE, b'')
    logger.info(f"Consumer {consumer_id!r} listening to {protocol}://{host}:{port}")
    while True:
        message = await socket.recv()
        logger.info(f"Consumer {consumer_id!r} pulled message: {message!r}")


async def run() -> None:
    consumer_id = str(uuid.uuid4()).encode()[:8]
    host = os.environ.get("HOST", "localhost")
    protocol = os.environ.get("PROTOCOL", "tcp")
    port = int(os.environ.get("PORT", 5556))
    await sub(host=host, protocol=protocol, port=port, consumer_id=consumer_id)


def main() -> None:
    asyncio.run(run())
