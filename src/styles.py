from rich.console import Console
from rich.text import Text


console = Console()


def push_event_message(size, repo_name):
    message = Text.from_markup(f"- [bold #8ac209]Pushed {size} commits[/bold #8ac209] to [italic underline blue]{repo_name}[/italic underline blue]")
    console.print(message, end='')


def watch_event_message(repo_name):
    message = Text.from_markup(f"- [bold #ffca41]Starred[/bold #ffca41] [italic underline blue]{repo_name}[/italic underline blue]")
    console.print(message, end='')


def create_event_message(ref_type, ref, repo_name):
    message = Text.from_markup(f"- [bold #00ffff]Created {ref_type} '{ref}'[/bold #00ffff] in [italic underline blue]{repo_name}[/italic underline blue]")
    console.print(message, end='')


def delete_event_message(ref_type, ref, repo_name):
    message = Text.from_markup(f"- [bold red]Deleted {ref_type} '{ref}'[/bold red] in [italic underline blue]{repo_name}[/italic underline blue]")
    console.print(message, end='')


def fork_event_message(repo_name, forkee_full_name):
    message = Text.from_markup(f"- [bold]Forked [italic underline blue]{repo_name}[/italic underline blue] to [italic underline blue]{forkee_full_name}[/italic underline blue][/bold]")
    console.print(message, end='')


def issue_event_message(repo_name):
    message = Text.from_markup(f"- [bold]Opened a new issue in [italic underline blue]{repo_name}[/italic underline blue][/bold]")
    console.print(message, end='')


def release_event_message(repo_name, release_name):
    message = Text.from_markup(f"- [bold]Published a new release in [italic underline blue]{repo_name}[/italic underline blue]: [bold]{release_name}[/bold]")
    console.print(message, end='')


def pull_request_event_message(action, repo_name):
    if action == "closed":
        message = Text.from_markup(f"- [bold violet]Merged a pull request[/bold violet] in [italic underline blue]{repo_name}[/italic underline blue]")
        console.print(message, end='')
    else:
        message = Text.from_markup(f"- [bold]Opened a pull request[/bold] in [italic underline blue]{repo_name}[/italic underline blue]")
        console.print(message, end='')
