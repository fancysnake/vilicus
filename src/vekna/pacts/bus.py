from typing import Protocol

from vekna.pacts.notify import Event


class HandlerProtocol(Protocol):
    async def __call__(self, event: Event) -> None: ...


class EventBusProtocol(Protocol):
    def register(self, app: str, hook: str, handler: HandlerProtocol) -> None: ...

    def publish(self, event: Event) -> None: ...
