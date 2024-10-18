from rich.console import Console
from rich.text import Text


console = Console()


def print_message(message):
    console.print(message, end='')


def push_event_message(size, repo_name):
    message = Text.from_markup(f"- [bold #8ac209]Pushed [italic]{size}[/italic] commits[/bold #8ac209] to [italic dim]{repo_name}[/italic dim]")
    print_message(message)


def watch_event_message(repo_name):
    message = Text.from_markup(f"- [bold #fdcd21]Starred[/bold #fdcd21] [italic dim]{repo_name}[/italic dim]")
    print_message(message)


def create_event_message(ref_type, ref, repo_name):
    message = Text.from_markup(f"- [bold #64acff]Created {ref_type} [italic]'{ref}'[/italic][/bold #64acff] in [italic dim]{repo_name}[/italic dim]")
    print_message(message)


def delete_event_message(ref_type, ref, repo_name):
    message = Text.from_markup(f"- [bold #ff4747]Deleted {ref_type} [italic]'{ref}'[/italic][/bold #ff4747] in [italic dim]{repo_name}[/italic dim]")
    print_message(message)


def fork_event_message(repo_name, forkee_full_name):
    message = Text.from_markup(f"- [bold #6880ff]Forked[/bold #6880ff] [italic dim]{repo_name}[/italic dim] to [italic dim]'{forkee_full_name}'[/italic dim]")
    print_message(message)


def issue_event_message(repo_name):
    message = Text.from_markup(f"- [bold #ff7c26]Opened a new issue[/bold #ff7c26] in [italic dim]{repo_name}[/italic dim]")
    print_message(message)


def release_event_message(repo_name, release_name):
    message = Text.from_markup(f"- [bold #03a348]Published a new release[/bold #03a348] in [italic dim]{repo_name}[/italic dim]: [italic dim]'{release_name}'[/italic dim]")
    print_message(message)


def pull_request_event_message(action, repo_name):
    if action == "closed":
        message = Text.from_markup(f"- [bold #d255ff]Merged a pull request[/bold #d255ff] in [italic dim]{repo_name}[/italic dim]")
        print_message(message)
    else:
        message = Text.from_markup(f"- [bold #ff7c26]Opened a pull request[/bold #ff7c26] in [italic dim]{repo_name}[/italic dim]")
        print_message(message)
