import asyncio
import contextlib
from collections.abc import Callable, Coroutine, Sequence

from pydantic import ValidationError

from vekna.pacts.bus import App, EventBusProtocol, Hook
from vekna.pacts.notify import ERROR_RESPONSE_INVALID, OK_RESPONSE, Event
from vekna.pacts.socket import Response, SocketServerLinkProtocol
from vekna.pacts.tmux import TmuxLinkProtocol


class ServerMill:
    def __init__(
        self,
        tmux: TmuxLinkProtocol,
        socket_server: SocketServerLinkProtocol,
        bus: EventBusProtocol,
        session_name_for_cwd: Callable[[str], str],
        background: Sequence[Callable[[], Coroutine[None, None, None]]] = (),
    ) -> None:
        self._tmux = tmux
        self._socket_server = socket_server
        self._bus = bus
        self._session_name_for_cwd = session_name_for_cwd
        self._background = background
        self._pending: dict[str, int] = {}  # session_name → notification count
        self._stop_event: asyncio.Event | None = None

    async def run(self) -> None:
        self._stop_event = asyncio.Event()
        await self._socket_server.start(self.handle)
        bg_tasks: list[asyncio.Task[None]] = [
            asyncio.create_task(coro()) for coro in self._background
        ]
        try:
            await asyncio.sleep(0)  # let background tasks reach their first await
            await self._stop_event.wait()
        finally:
            for task in bg_tasks:
                task.cancel()
                with contextlib.suppress(asyncio.CancelledError):
                    await task
            await self._bus.drain()
            await self._socket_server.stop()

    async def handle(self, message: str) -> str:
        try:
            event = Event.model_validate_json(message)
        except ValidationError:
            return ERROR_RESPONSE_INVALID.model_dump_json()
        if event.app == App.VEKNA and event.hook == Hook.ENSURE_SESSION:
            return self._handle_ensure_session(event)
        if event.app == App.VEKNA and event.hook == Hook.STATUS_BAR:
            return self._handle_status_bar()
        if (
            event.app == App.CLAUDE
            and event.hook == Hook.NOTIFICATION
            and (pane_id := event.meta.get("TMUX_PANE", ""))
            and (session_name := self._tmux.session_name_for_pane(pane_id))
        ):
            self._pending[session_name] = self._pending.get(session_name, 0) + 1
        self._bus.publish(event)
        return OK_RESPONSE.model_dump_json()

    def _handle_ensure_session(self, event: Event) -> str:
        cwd = event.meta["cwd"]
        session_name = self._session_name_for_cwd(cwd)
        self._tmux.ensure_session(session_name, cwd)
        self._pending[session_name] = 0
        return Response(
            status="ok", data={"session_name": session_name}
        ).model_dump_json()

    def clear_pending(self, session_name: str) -> None:
        self._pending.pop(session_name, None)

    def _handle_status_bar(self) -> str:
        parts = ["vekna 💀"] + [
            f"{name}({count})" for name, count in self._pending.items() if count > 0
        ]
        return Response(status="ok", data={"text": " ".join(parts)}).model_dump_json()
