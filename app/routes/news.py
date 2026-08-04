from flask import Blueprint, render_template, redirect, url_for, flash

from ..db import get_db
from ..news_fetch import TEAMS, refresh_all
from ..schedule_fetch import get_upcoming_games

bp = Blueprint("news", __name__, url_prefix="/news")

BUCKET_LIMIT = 5


@bp.route("/")
def index():
    db = get_db()

    top_stories = db.execute(
        "SELECT * FROM news_items ORDER BY priority ASC, fetched_at DESC, id DESC LIMIT 4"
    ).fetchall()
    top_ids = [row["id"] for row in top_stories]

    team_logos = {g["team"]: g["my_logo"] for g in get_upcoming_games()}

    exclude_clause = f"AND id NOT IN ({','.join('?' * len(top_ids))})" if top_ids else ""
    stories_by_team = {}
    for team in TEAMS:
        stories_by_team[team] = db.execute(
            f"SELECT * FROM news_items WHERE team = ? {exclude_clause} "
            "ORDER BY priority ASC, fetched_at DESC, id DESC LIMIT ?",
            (team, *top_ids, BUCKET_LIMIT),
        ).fetchall()

    return render_template(
        "news.html",
        main_story=top_stories[0] if top_stories else None,
        primary_stories=top_stories[1:4],
        stories_by_team=stories_by_team,
        team_logos=team_logos,
    )


@bp.route("/refresh", methods=["POST"])
def refresh():
    results = refresh_all()
    total = sum(results.values())
    flash(f"Pulled {total} new headline(s): " + ", ".join(f"{t} +{n}" for t, n in results.items()), "info")
    return redirect(url_for("news.index"))
