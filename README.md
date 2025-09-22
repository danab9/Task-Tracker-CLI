
A simple command-line task manager written in Python using CLick and SQLite.<br />
This project is based on the [Task Tracker CLI project](https://roadmap.sh/projects/task-tracker).

## Installation
1. Clone the repository
```bash
git clone https://github.com/danab9/task-cli.git
cd task-cli
```
2. Install the CLI
```bash
pip install -e .
```

## Usage
After installing, run the CLI with:<br />
`task-cli [COMMAND] [OPTIONS]`

#### Examples
```bash
# Add tasks
task-cli add "Read a book"
task-cli add "Finish project"

# List all TODO tasks
task-cli list todo

# Mark one task as in progress
task-cli mark-in-progress 1

# Mark a task as done
task-cli done 2

# Delete a task
task-cli delete 1
```
