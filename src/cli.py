import click
import json
import socket
from styles import *
from http.client import HTTPSConnection


@click.command()
@click.version_option(version="0.4.0", prog_name="Github User Activity")
@click.argument("username", type=str)
def cli(username):
    try:
        connection = HTTPSConnection("api.github.com", timeout=10)

        headers = {"User-Agent": "github-user-activity-cli"}
        connection.request("GET", f"/users/{username}/events", headers=headers)

        response = connection.getresponse()
        data = response.read()

        # Error handling
        if response.status == 404:
            raise click.ClickException("User not found")
        elif response.status == 403:
            raise click.ClickException("Request forbidden: possible rate limit exceeded")
        elif response.status != 200:
            raise click.ClickException(f"Unexpected error: {response.status}")

        # Data decoding
        events = json.loads(data.decode("utf-8"))
        if not events:
            click.echo("No recent activity found.")
            return

        # Events dictionary
        event_handlers = {
            "PushEvent": lambda e: push_event_message(e['payload']['size'], e['repo']['name']),
            "WatchEvent": lambda e: watch_event_message(e['repo']['name']),
            "CreateEvent": lambda e: create_event_message(e['payload']['ref_type'], e['payload']['ref'], e['repo']['name']),
            "DeleteEvent": lambda e: delete_event_message(e['payload']['ref_type'], e['payload']['ref'], e['repo']['name']),
            "ForkEvent": lambda e: fork_event_message(e['repo']['name'], e['payload']['forkee']['full_name']),
            "IssueEvent": lambda e: issue_event_message(e['repo']['name']),
            "ReleaseEvent": lambda e: release_event_message(e['repo']['name'], e['payload']['release']['name']),
            "PullRequestEvent": lambda e: pull_request_event_message(e["payload"]["action"], e["repo"]["name"])
        }

        # Show events
        for event in events:
            handler = event_handlers.get(event["type"])
            if handler:
                click.echo(handler(event))

    except socket.timeout:
        raise click.ClickException("Request timed out. Please try again later")


if __name__ == "__main__":
    cli()
