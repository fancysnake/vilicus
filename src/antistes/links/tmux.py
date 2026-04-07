import libtmux


class TmuxLink:
    def __init__(self) -> None:
        self._server = libtmux.Server(socket_name="antistes")
