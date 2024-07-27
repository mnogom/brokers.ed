import argparse
import asyncio
import os
import uuid
from contextlib import contextmanager
from typing import Iterator

import zmq.asyncio
from loguru import logger


def generate_data() -> bytes:
    return str(uuid.uuid4()).encode()


@contextmanager
def open_socket(protocol: str, port: int) -> Iterator[zmq.asyncio.Socket]:
    context = zmq.asyncio.Context.instance()
    socket = context.socket(zmq.PUB)
    socket.bind(f"{protocol}://*:{port}")
    yield socket
    socket.close()


async def publish(socket: zmq.asyncio.Socket, session_id: bytes, message_id: int) -> None:
    message_id = str(message_id).encode()
    data = session_id + b" @ " + generate_data() + b" | " + message_id
    await socket.send(data)
    logger.info(f"Published {data!r}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--package-number", type=int, required=False, default=1)
    parser.add_argument("-t", "--timeout", type=int, required=False, default=0)
    args = parser.parse_args()
    return args.package_number, args.timeout


async def run(
    port: int,
    protocol: str,
    package_number: int,
    timeout: int,
    session_id: bytes,
) -> None:
    with open_socket(port=port, protocol=protocol) as socket:
        await asyncio.sleep(0.5)  # Wait for the socket to be ready
        for message_id in range(package_number):
            await publish(socket=socket, session_id=session_id, message_id=message_id)
            await asyncio.sleep(timeout)


def main() -> None:
    session_id = generate_data()[:8]
    port = int(os.environ.get("PORT", 5556))
    package_number, timeout = parse_args()
    protocol = os.environ.get("PROTOCOL", "tcp")
    asyncio.run(
        run(
            port=port,
            protocol=protocol,
            package_number=package_number,
            timeout=timeout,
            session_id=session_id,
        )
    )
