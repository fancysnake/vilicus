from subprocess import CalledProcessError, check_output  # noqa: S404


class TmuxServerSubprocessLink:
    @staticmethod
    def check() -> bool:
        try:
            check_output(["/usr/bin/tmux", "-L", "antistes", "list-sessions"])
        except CalledProcessError:
            return False

        return True

    @staticmethod
    def start() -> None:
        check_output(["/usr/bin/tmux", "-L", "antistes", "new", "claude"])

    @staticmethod
    def attach() -> None:
        check_output(["/usr/bin/tmux", "-L", "antistes", "a"])
