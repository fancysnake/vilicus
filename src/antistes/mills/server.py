from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from antistes.pacts.protocols import TmuxServerSubprocessLinkProtocol


class ServerMill:
    def __init__(self, subprocess_link: TmuxServerSubprocessLinkProtocol) -> None:
        self._subprocess_link = subprocess_link

    def ensure_running(self) -> None:
        if not self._subprocess_link.check():
            self._subprocess_link.start()
        else:
            self._subprocess_link.attach()
