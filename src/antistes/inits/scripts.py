from typing import TYPE_CHECKING

from antistes.gates.click import ClickGate
from antistes.links.subprocess import TmuxServerSubprocessLink
from antistes.mills.server import ServerMill

if TYPE_CHECKING:
    from click import Command


def init_command() -> Command:
    subprocess_link = TmuxServerSubprocessLink()

    server_mill = ServerMill(subprocess_link=subprocess_link)

    click_gate = ClickGate(server_mill=server_mill)

    return click_gate.build_command()


def run() -> None:
    init_command()  # pragma: no cover
