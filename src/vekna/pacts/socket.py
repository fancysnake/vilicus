from collections.abc import Awaitable, Callable
from typing import Protocol


class SocketServerLinkProtocol(Protocol):
    async def start(self, handler: Callable[[str], Awaitable[str]]) -> None: ...

    async def stop(self) -> None: ...


class SocketClientLinkProtocol(Protocol):
    async def send(self, message: str) -> str: ...
