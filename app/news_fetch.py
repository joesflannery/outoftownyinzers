"""Pulls team news into the news_items table so the News page and homepage
Stories section don't have to hit RSS feeds on every request. Steelers and
Pirates have real official RSS feeds; Penguins and Pitt don't publish a
machine-readable feed we could find, so those two fall back to Google News
search feeds.

Pitt Athletics covers many sports under one program, so its coverage is
built from separate, priority-ordered queries (football, then men's
basketball, then women's volleyball) rather than one generic query -- that
keeps the Stories bucket from being dominated by whichever sport happens to
be in season/newsworthy at the moment. Other Pitt sports aren't queried at
all for now; there's no reliable automated way to judge "is this other-sport
story actually noteworthy," so that's left as a manual call (e.g. write a
blog post about it) rather than guessed at here.

Quality filtering for the two Google News teams: Penguins coverage is
restricted to a source allowlist (_ALLOWED_SOURCES) since open Google News
search pulls in low-quality secondary aggregators (Times of India picking
up NHL rumors, content-farm sites, etc.) alongside real Pittsburgh outlets.
Pitt's coverage overwhelmingly comes from pittsburghpanthers.com itself
(the team's own site, legitimately indexed), so an allowlist wouldn't help
there -- instead _TITLE_EXCLUDES filters out that site's routine practice-
report posts ("Wraps Up Practice No. 13", "Completes Seventh Spring
Practice"), which are real but not actually newsworthy.

Images: Steelers' feed includes a real per-story photo via <media:content>,
which feedparser parses natively. Pirates' feed has one too, but via a
nonstandard <image href="..."> tag feedparser doesn't recognize, so that's
pulled with a small raw-XML regex pass instead. Penguins/Pitt (Google News)
don't provide images at all -- those stay NULL here and the templates fall
back to the team logo instead.

Google News's RSS terms restrict use to "personal feed reader" purposes --
worth revisiting if this ever needs to be airtight, but fine for a hobby
podcast site aggregating headlines with links back to the original source.
"""

import difflib
import re

import click
import feedparser
import requests

from .db import get_db

TEAMS = ["Steelers", "Pirates", "Penguins", "Pitt"]

_GOOGLE_NEWS = "https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"

# team -> list of (feed url, priority, required-keyword-in-title-or-None)
# lower priority number = shown first within that team's bucket.
_SOURCES = {
    "Steelers": [
        ("https://www.steelers.com/rss/news", 0, None),
    ],
    "Pirates": [
        ("https://www.mlb.com/pirates/feeds/news/rss.xml", 0, None),
    ],
    "Penguins": [
        (_GOOGLE_NEWS.format(query="Pittsburgh+Penguins"), 0, "penguin"),
    ],
    "Pitt": [
        (_GOOGLE_NEWS.format(query="Pitt+Panthers+football"), 0, "pitt"),
        (_GOOGLE_NEWS.format(query="Pitt+Panthers+men%27s+basketball"), 1, "pitt"),
        (_GOOGLE_NEWS.format(query="Pitt+Panthers+women%27s+volleyball"), 2, "pitt"),
    ],
}

# Known-good outlets for teams sourced from open Google News search --
# anything not in this list gets skipped for that team. Lowercased for
# case-insensitive matching against feedparser's entry.source.title.
_ALLOWED_SOURCES = {
    "Penguins": {
        "pittsburgh hockey now",
        "pensburgh",
        "nhl.com",
        "pittsburgh post-gazette",
        "the hockey writers",
        "the hockey news",
        "the athletic",
        "espn",
        "triblive.com",
        "pittsburgh tribune-review",
        "the new york times",
        "dk pittsburgh sports",
    },
}

# team -> list of lowercased phrases; a title containing any of these gets
# skipped for that team (routine/low-value posts, not actual news).
_TITLE_EXCLUDES = {
    "Pitt": [
        "spring practice",
        "practice no.",
        "wraps up practice",
        "training camp report",
    ],
}

_DUPLICATE_THRESHOLD = 0.6
_RECENT_TITLES_CHECKED = 40


def _normalize_title(title):
    # Google News appends " - Source Name" -- strip it before comparing.
    if " - " in title:
        title = title.rsplit(" - ", 1)[0]
    return title.lower().strip()


def _is_near_duplicate(normalized_title, seen_normalized_titles):
    for other in seen_normalized_titles:
        if difflib.SequenceMatcher(None, normalized_title, other).ratio() >= _DUPLICATE_THRESHOLD:
            return True
    return False


def _mlb_images_by_link(url):
    """Pirates' <image href="..."> tag isn't in a namespace feedparser
    recognizes as per-item media, so pull it directly from the raw XML,
    keyed by each item's <link> so it can be matched up with feedparser's
    parsed entries."""
    try:
        resp = requests.get(url, timeout=8)
        resp.raise_for_status()
    except Exception:
        return {}

    images = {}
    for item_xml in re.findall(r"<item>.*?</item>", resp.text, re.S):
        link_match = re.search(r"<link>(.*?)</link>", item_xml)
        image_match = re.search(r'<image href="([^"]*)"', item_xml)
        if link_match and image_match:
            images[link_match.group(1)] = image_match.group(1)
    return images


def _image_for_entry(team, url, entry):
    if team == "Steelers":
        media = entry.get("media_content")
        if media:
            return media[0].get("url")
    return None


def refresh_team(team):
    """Fetch a team's feed(s) and upsert new, non-duplicate items into
    news_items. Returns the number of new items added."""
    db = get_db()
    seen_normalized = {
        _normalize_title(row["title"])
        for row in db.execute(
            "SELECT title FROM news_items WHERE team = ? ORDER BY fetched_at DESC, id DESC LIMIT ?",
            (team, _RECENT_TITLES_CHECKED),
        )
    }

    allowed_sources = _ALLOWED_SOURCES.get(team)
    title_excludes = _TITLE_EXCLUDES.get(team, [])

    added = 0
    for url, priority, required_keyword in _SOURCES[team]:
        parsed = feedparser.parse(url)
        mlb_images = _mlb_images_by_link(url) if team == "Pirates" else {}

        for entry in parsed.entries[:20]:
            title = entry.get("title", "").strip()
            link = entry.get("link", "").strip()
            if not title or not link:
                continue
            if required_keyword and required_keyword not in title.lower():
                continue
            if title_excludes and any(kw in title.lower() for kw in title_excludes):
                continue

            source = entry.get("source", {}).get("title") if entry.get("source") else None
            if allowed_sources is not None and (not source or source.lower() not in allowed_sources):
                continue

            normalized = _normalize_title(title)
            if _is_near_duplicate(normalized, seen_normalized):
                continue

            published_at = entry.get("published", "")
            image = _image_for_entry(team, url, entry) or mlb_images.get(link)
            cur = db.execute(
                "INSERT OR IGNORE INTO news_items (team, title, link, source, published_at, priority, image) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (team, title, link, source, published_at, priority, image),
            )
            if cur.rowcount:
                added += 1
                seen_normalized.add(normalized)
    db.commit()
    return added


def refresh_all():
    return {team: refresh_team(team) for team in TEAMS}


@click.command("refresh-news")
def refresh_news_command():
    """Fetch fresh headlines for all teams -- meant to be run on a schedule
    (e.g. a PythonAnywhere scheduled task) so the News page doesn't rely on
    someone remembering to click "Refresh headlines" in the browser."""
    results = refresh_all()
    total = sum(results.values())
    click.echo(f"Added {total} new headline(s): " + ", ".join(f"{t} +{n}" for t, n in results.items()))


def init_app(app):
    app.cli.add_command(refresh_news_command)
