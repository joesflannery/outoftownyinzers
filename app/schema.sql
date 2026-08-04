CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    author TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    published INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS news_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team TEXT NOT NULL,
    title TEXT NOT NULL,
    link TEXT NOT NULL,
    source TEXT,
    published_at TEXT,
    fetched_at TEXT NOT NULL DEFAULT (datetime('now')),
    priority INTEGER NOT NULL DEFAULT 0,
    image TEXT,
    UNIQUE(team, link)
);

CREATE TABLE IF NOT EXISTS newsletter_signups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
