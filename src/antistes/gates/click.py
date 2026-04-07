from typing import TYPE_CHECKING

import click

if TYPE_CHECKING:
    from antistes.pacts.protocols import ServerMillProtocol


class ClickGate:
    def __init__(self, server_mill: ServerMillProtocol) -> None:
        self._server_mill = server_mill

    def build_command(self) -> click.Command:
        @click.command()
        def main() -> None:
            self._server_mill.ensure_running()

        return main
