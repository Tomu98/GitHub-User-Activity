import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from click.testing import CliRunner
from src.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


class MockResponse:
    def __init__(self, status_code, content):
        self.status = status_code
        self._content = content

    def read(self):
        return self._content


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


def test_username_found(runner, mocker):
    mocker.patch("src.cli.HTTPSConnection.getresponse", return_value=MockResponse(200, valid_data))
    result = runner.invoke(cli, ["Tomu98"])
    assert result.exit_code == 0
    assert "Pushed" in result.output


def test_user_not_found(runner, mocker):
    mocker.patch("src.cli.HTTPSConnection.getresponse", return_value=MockResponse(404, b""))
    result = runner.invoke(cli, ["NonExistentUser"])
    assert result.exit_code == 1
    assert "User not found" in result.output


def test_rate_limit_exceeded(runner, mocker):
    mocker.patch("src.cli.HTTPSConnection.getresponse", return_value=MockResponse(403, b""))
    result = runner.invoke(cli, ["Tomu98"])
    assert result.exit_code == 1
    assert "Request forbidden" in result.output
