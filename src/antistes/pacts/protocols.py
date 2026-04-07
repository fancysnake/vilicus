from typing import Protocol


class TmuxServerSubprocessLinkProtocol(Protocol):
    def check(self) -> bool: ...

    @staticmethod
    def start() -> None: ...

    @staticmethod
    def attach() -> None: ...


class ServerMillProtocol(Protocol):
    def __init__(self, subprocess_link: TmuxServerSubprocessLinkProtocol) -> None: ...

    def ensure_running(self) -> None: ...
