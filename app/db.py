import sqlite3
from pathlib import Path

import click
from flask import current_app, g

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "app.db"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH, timeout=10)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    db = get_db()
    schema_path = Path(__file__).resolve().parent / "schema.sql"
    with open(schema_path) as f:
        db.executescript(f.read())
    db.commit()
    _migrate(db)
    _seed_defaults(db)


def _migrate(db):
    """Small ad-hoc migrations for columns added after a table already
    existed -- CREATE TABLE IF NOT EXISTS alone won't add them."""
    columns = {row["name"] for row in db.execute("PRAGMA table_info(news_items)")}
    if "priority" not in columns:
        db.execute("ALTER TABLE news_items ADD COLUMN priority INTEGER NOT NULL DEFAULT 0")
        db.commit()
    if "image" not in columns:
        db.execute("ALTER TABLE news_items ADD COLUMN image TEXT")
        db.commit()


def _seed_defaults(db):
    """Placeholder blog post so the Stories column/Blog aren't empty on a
    fresh install -- only runs once, since it checks for an empty table."""
    row = db.execute("SELECT COUNT(*) AS c FROM posts").fetchone()
    if row["c"] == 0:
        db.execute(
            "INSERT INTO posts (title, body, author) VALUES (?, ?, ?)",
            (
                "Why I Still Love the Pirates",
                "Placeholder post -- edit or delete this from the Blog once you've got "
                "real content ready. This is just here so the homepage and Blog page "
                "aren't empty out of the box.",
                "Joe",
            ),
        )
        db.commit()


@click.command("init-db")
def init_db_command():
    """Create any tables that don't exist yet."""
    init_db()
    click.echo(f"Initialized database at {DB_PATH}")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    with app.app_context():
        init_db()
