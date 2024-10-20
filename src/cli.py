import click
import json
import socket
from .styles import *
from http.client import HTTPSConnection


@click.command()
@click.version_option(version="1.2.0", prog_name="Github User Activity")
@click.argument("username", type=str)
@click.option("--event", type=str, help="FIlter events by type (push, watch, create, delete, fork, issue, release, pr)",)
def cli(username, event):
    """
    Fetches and displays recent activity for the specified GitHub username.
    """
    list_events = ['push', 'watch', 'create', 'delete', 'fork', 'issue', 'release', 'pr']

    # Validate the type of event provided
    if event and event not in list_events:
        raise click.ClickException(f"Invalid event type '{event}'. Valid options are: {', '.join(list_events)}")

    # Event type mapping (what the user passes -> the actual name of the event in GitHub)
    event_map = {
        'push': 'PushEvent',
        'watch': 'WatchEvent',
        'create': 'CreateEvent',
        'delete': 'DeleteEvent',
        'fork': 'ForkEvent',
        'issue': 'IssueEvent',
        'release': 'ReleaseEvent',
        'pr': 'PullRequestEvent'
    }

    # Event mapping if one was provided
    event_type = event_map.get(event)

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

        # Filtered events counter
        matched_events = 0

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

        # Show events and count events matching the filter
        for github_event in events:
            if event_type and github_event["type"] != event_type:
                continue

            handler = event_handlers.get(github_event["type"])
            if handler:
                click.echo(handler(github_event))
                matched_events += 1

        # Check if any events were found with the filter
        if matched_events == 0:
            click.echo(f"No activity found for event type: {event}")

    except socket.timeout:
        raise click.ClickException("Request timed out. Please try again later")


if __name__ == "__main__":
    cli()
