import asyncio
import os
import uuid

import zmq.asyncio
from loguru import logger


async def reply(protocol: str, port: int, consumer_id: bytes) -> None:
    context = zmq.asyncio.Context.instance()
    socket = context.socket(zmq.REP)
    socket.bind(f"{protocol}://*: {port}")
    logger.info(f"Consumer {consumer_id!r} listening on {protocol}://*:{port}")
    while True:
        message = await socket.recv()
        await socket.send(b"ACK:" + message)
        logger.info(f"Consumer {consumer_id!r} received message: {message!r} and acknowledged it")


async def run() -> None:
    consumer_id = str(uuid.uuid4()).encode()[:8]
    protocol = os.environ.get("PROTOCOL", "tcp")
    port = int(os.environ.get("PORT", 5556))
    await reply(protocol=protocol, port=port, consumer_id=consumer_id)


def main() -> None:
    asyncio.run(run())
