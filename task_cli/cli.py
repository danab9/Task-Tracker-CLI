"""cli implementation"""
import sqlite3
from pathlib import Path

import click

DB_PATH = Path(__file__).parent / "tasks.db"

def get_connection():
    """establish sqlite3 connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """initialize seqlite3 database"""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                status TEXT CHECK(status IN ('todo', 'in-progress', 'done')) NOT NULL DEFAULT 'todo',
                createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
                updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

@click.group()
def cli():
    """Task CLI"""
    init_db()

@cli.command()
@click.argument("description")
def add(description):
    """Add a new task"""
    with get_connection() as conn:
        cursor = conn.execute("INSERT INTO tasks (description) VALUES (?)", (description,))
        task_id = cursor.lastrowid

    click.echo(f"Task added successfully (ID: {task_id})")

@cli.command()
@click.argument("task_id", type=int)
@click.argument("new_description")
def update(task_id, new_description):
    """Update description of task with <id>"""
    with get_connection() as conn:
        conn.execute(
                "UPDATE tasks SET description = ? WHERE id = ?",
                (new_description, task_id)
            )
    conn.commit()



@cli.command()
@click.argument("task_id", type=int)
def delete(task_id):
    """Delete task with task id <id>"""
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM tasks WHERE id = ?;",
            (task_id,)
        )
    conn.commit()


@cli.command(name="mark-in-progress")
@click.argument("task_id", type=int)
def mark_in_progress(task_id):
    """Update status to in-progress"""
    with get_connection() as conn:
        conn.execute(
            """UPDATE tasks
            SET status = 'in-progress',
            updatedAt = CURRENT_TIMESTAMP
            WHERE id = ?;""",
            (task_id,)
        )
    conn.commit()

@cli.command(name="mark-done")
@click.argument("task_id", type=int)
def mark_done(task_id):
    """Update status to done"""
    with get_connection() as conn:
        conn.execute(
            """UPDATE tasks
            SET status = 'done',
            updatedAt = CURRENT_TIMESTAMP
            WHERE id = ?;""",
            (task_id,)
        )
    conn.commit()

@cli.command(name="list")
@click.argument("status")
def list_by_status(status):
    """List all tasks with status [todo | in-progress | done]"""
    if status not in ['todo', 'done', 'in-progress']:
        click.echo("Invalid status. Use: todo | in-progress | done")
        return
    # else
    with get_connection() as conn:
        cursor = conn.execute("""
            SELECT *
            FROM tasks
            WHERE status = ?;
        """, (status,))
        rows = cursor.fetchall()

    for row in rows:
        click.echo(f"{row['id']}: {row['description']}")

if __name__ == '__main__':
    cli()
