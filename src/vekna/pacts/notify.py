from typing import Protocol

from pydantic import BaseModel

OK_RESPONSE = '{"status": "ok"}'
ERROR_RESPONSE_INVALID = '{"status": "error", "reason": "invalid request"}'


class Event(BaseModel):
    app: str
    hook: str
    payload: str
    meta: dict[str, str]


class NotifyClientMillProtocol(Protocol):
    async def notify(
        self, app: str, hook: str, payload: str, meta: dict[str, str]
    ) -> None: ...
