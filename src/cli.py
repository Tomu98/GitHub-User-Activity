import click
import json
from http.client import HTTPSConnection

@click.command()
@click.argument("username", type=str)
def cli(username):
    connection = HTTPSConnection("api.github.com")

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
        "PushEvent": lambda e: f"Pushed {e['payload']['size']} commits to {e['repo']['name']}",
        "WatchEvent": lambda e: f"Starred {e['repo']['name']}",
        "CreateEvent": lambda e: f"Created {e['payload']['ref_type']} '{e['payload']['ref']}' in {e['repo']['name']}",
        "DeleteEvent": lambda e: f"Deleted {e['payload']['ref_type']} '{e['payload']['ref']}' in {e['repo']['name']}",
        "ForkEvent": lambda e: f"Forked {e['repo']['name']} to {e['payload']['forkee']['full_name']}",
        "IssueEvent": lambda e: f"Opened a new issue in {e['repo']['name']}",
        "ReleaseEvent": lambda e: f"Published a new release in {e['repo']['name']}: {e['payload']['release']['name']}",
        "PullRequestEvent": lambda e: (
            f"Merged a pull request in {e['repo']['name']}" if e['payload']['action'] == "closed" and e['payload']['pull_request']['merged']
            else f"Opened a pull request in {e['repo']['name']}"
        )
    }

    # Show events
    for event in events:
        handler = event_handlers.get(event["type"])
        if handler:
            click.echo(handler(event))


if __name__ == "__main__":
    cli()
