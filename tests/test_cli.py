import pytest
import socket
from click.testing import CliRunner
from src.cli import cli


# Fixtures
@pytest.fixture
def runner():
    """
    Provides a CliRunner instance for invoking CLI commands.
    """
    return CliRunner()


class MockResponse:
    """
    Simulates an HTTP response.
    """
    def __init__(self, status_code, content, headers=None):
        self.status = status_code
        self._content = content
        self.headers = headers or {}

    def read(self):
        """
        Returns the response content.
        """
        return self._content

    def getheader(self, name, default=None):
        """
        Retrieves a header value or default.
        """
        return self.headers.get(name, default)



# Data Mocks
valid_data = b"""
[
    {
        "type": "PushEvent",
        "repo": {"name": "Tomu98/test-repo"},
        "payload": {"size": 2}
    }
]
"""

create_event_data = b"""
[
    {
        "type": "CreateEvent",
        "repo": {"name": "Tomu98/test-repo"},
        "payload": {"ref_type": "branch", "ref": "main"}
    }
]
"""

fork_event_data = b"""
[
    {
        "type": "ForkEvent",
        "repo": {"name": "Tomu98/test-repo"},
        "payload": {"forkee": {"full_name": "Tomu98/forked-repo"}}
    }
]
"""

no_activity_data = b"[]"


# Tests
# 1. API Response Status Tests
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


# 2. Specific Event Handling
def test_fork_event(runner, mocker):
    mocker.patch("src.cli.HTTPSConnection.getresponse", return_value=MockResponse(200, fork_event_data))
    result = runner.invoke(cli, ["Tomu98"])
    assert result.exit_code == 0
    assert "- Forked Tomu98/test-repo to 'Tomu98/forked-repo'" in result.output


def test_create_event(runner, mocker):
    mocker.patch("src.cli.HTTPSConnection.getresponse", return_value=MockResponse(200, create_event_data))
    result = runner.invoke(cli, ["Tomu98"])
    assert result.exit_code == 0
    assert "- Created branch 'main' in Tomu98/test-repo" in result.output


# 3. Event Filtering and No Activity
def test_event_filter(runner, mocker):
    mocker.patch("src.cli.HTTPSConnection.getresponse", return_value=MockResponse(200, valid_data))
    result = runner.invoke(cli, ["Tomu98", "--event", "push"])
    assert result.exit_code == 0
    assert "Pushed" in result.output

    result_no_match = runner.invoke(cli, ["Tomu98", "--event", "fork"])
    assert "No activity found for event type: fork" in result_no_match.output


def test_no_activity(runner, mocker):
    mocker.patch("src.cli.HTTPSConnection.getresponse", return_value=MockResponse(200, no_activity_data))
    result = runner.invoke(cli, ["Tomu98"])
    assert result.exit_code == 0
    assert "No recent activity found" in result.output
