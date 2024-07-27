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
def open_socket(protocol: str, host: str, port: int) -> Iterator[zmq.asyncio.Socket]:
    context = zmq.asyncio.Context.instance()
    socket = context.socket(zmq.PUSH)
    socket.bind(f"{protocol}://{host}:{port}")
    yield socket
    socket.close()


async def push(socket: zmq.asyncio.Socket, session_id: bytes, message_id: int) -> None:
    message_id = str(message_id).encode()
    data = session_id + b" @ " + generate_data() + b" | " + message_id
    await socket.send(data)
    logger.info(f"Pushed {data!r}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--package-number", type=int, required=False, default=1)
    parser.add_argument("-t", "--timeout", type=int, required=False, default=0)
    args = parser.parse_args()
    return args.package_number, args.timeout


async def run(
    host: str,
    port: int,
    protocol: str,
    package_number: int,
    timeout: int,
    session_id: bytes,
) -> None:
    with open_socket(host=host, port=port, protocol=protocol) as socket:
        for message_id in range(package_number):
            await push(socket=socket, session_id=session_id, message_id=message_id)
        await asyncio.sleep(timeout)


def main() -> None:
    session_id = generate_data()[:8]
    host = os.environ.get("HOST", "localhost")
    port = int(os.environ.get("PORT", 5556))
    package_number, timeout = parse_args()
    protocol = os.environ.get("PROTOCOL", "tcp")
    asyncio.run(
        run(
            host=host,
            port=port,
            protocol=protocol,
            package_number=package_number,
            timeout=timeout,
            session_id=session_id,
        )
    )
