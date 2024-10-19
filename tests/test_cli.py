import pytest
import socket
from click.testing import CliRunner
from src.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


class MockResponse:
    def __init__(self, status_code, content, headers=None):
        self.status = status_code
        self._content = content
        self.headers = headers or {}

    def read(self):
        return self._content

    def getheader(self, name, default=None):
        return self.headers.get(name, default)


# Valid data simulation
valid_data = b"""
[
    {
        "type": "PushEvent",
        "repo": {"name": "Tomu98/test-repo"},
        "payload": {"size": 2}
    }
]
"""


# Additional event simulation data
create_event_data = b"""
[
    {
        "type": "CreateEvent",
        "repo": {"name": "Tomu98/test-repo"},
        "payload": {"ref_type": "branch", "ref": "main"}
    }
]
"""


# Fork event simulation data
fork_event_data = b"""
[
    {
        "type": "ForkEvent",
        "repo": {"name": "Tomu98/test-repo"},
        "payload": {"forkee": {"full_name": "Tomu98/forked-repo"}}
    }
]
"""


# No activity simulation
no_activity_data = b"[]"


@pytest.mark.parametrize("status_code, response_data, expected_output", [
    (200, valid_data, "Pushed"),
    (404, b"", "User not found"),
    (403, b"", "Request forbidden"),
])

def test_various_responses(runner, mocker, status_code, response_data, expected_output):
    mocker.patch("src.cli.HTTPSConnection.getresponse", return_value=MockResponse(status_code, response_data))
    result = runner.invoke(cli, ["Tomu98"])
    assert expected_output in result.output

def test_timeout_error(runner, mocker):
    mocker.patch("src.cli.HTTPSConnection.request", side_effect=socket.timeout)
    result = runner.invoke(cli, ["Tomu98"])
    assert result.exit_code == 1
    assert "Request timed out" in result.output

def test_fork_event(runner, mocker):
    mocker.patch("src.cli.HTTPSConnection.getresponse", return_value=MockResponse(200, fork_event_data))
    result = runner.invoke(cli, ["Tomu98"])
    assert result.exit_code == 0
    assert "- Forked Tomu98/test-repo to 'Tomu98/forked-repo'" in result.output
