from subprocess import CalledProcessError
from unittest.mock import call, patch

from click.testing import CliRunner

from antistes.inits.scripts import init_command


class TestCommand:
    @staticmethod
    @patch("antistes.links.subprocess.check_output")
    def test_start(check_output_mock):
        check_output_mock.side_effect = CalledProcessError(1, "cmd"), None
        runner = CliRunner()

        result = runner.invoke(init_command())

        assert result.exit_code == 0
        check_output_mock.assert_has_calls(
            [
                call(["/usr/bin/tmux", "-L", "antistes", "list-sessions"]),
                call(["/usr/bin/tmux", "-L", "antistes", "new", "claude"]),
            ],
        )

    @staticmethod
    @patch("antistes.links.subprocess.check_output")
    def test_attach(check_output_mock):
        check_output_mock.side_effect = None, None
        runner = CliRunner()

        result = runner.invoke(init_command())

        assert result.exit_code == 0
        check_output_mock.assert_has_calls(
            [
                call(["/usr/bin/tmux", "-L", "antistes", "list-sessions"]),
                call(["/usr/bin/tmux", "-L", "antistes", "a"]),
            ],
        )
