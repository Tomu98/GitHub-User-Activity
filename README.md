# GitHub User Activity

A simple CLI tool that allows you to query the recent activity of any user on GitHub. Through the GitHub API, it shows you many events such as commits, pull requests, issues created, starred repositories, and more.

This project is inspired by an idea from [roadmap.sh](https://roadmap.sh), a platform that offers community-created roadmaps, best practices, projects ideas and resources that help people grow in their technology careers.

Specific inspiration for this project comes from the following link: [GitHub User Activity in roadmap.sh](https://roadmap.sh/projects/github-user-activity)

<br>

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/Tomu98/GitHub-User-Activity.git
   ```

2. Within the project directory, create and activate a virtual environment:

   ```bash
   python -m venv .venv        # Create a virtual environment
   source .venv/bin/activate   # Activate the environment in Linux/MacOS
   .venv\Scripts\activate      # Activate the environment in Windows
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

<br>

## How to use it

To query the recent activity of a GitHub user, run the following command:

   ```bash
   python -m src/cli <username>
   ```

For example:

   ```bash
   python -m src/cli Tomu98
   ```

You can filter the events displayed using the `--event` option. The supported event types are:
- `push`: Commits pushed.
- `watch`: Starred repositories.
- `create`: Created repositories/branches.
- `delete`: Deleted repositories/branches.
- `fork`: Forked repositories.
- `issue`: Issues created.
- `release`: Releases made.
- `pr`: Opened/Merged pull requests.

For example, to display only the commits pushed by the user, use:

   ```bash
   python -m src/cli Tomu98 --event push
   ```

<br>

## Feedback & Contributions

This is my first CLI project, and I welcome any comments or contributions. If you find bugs or have suggestions to help me, feel free to open an issue or send a pull request, it will help me a lot to improve.

<br>

### **Thanks for checking out the project 🤍**
