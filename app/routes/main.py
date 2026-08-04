from flask import Blueprint, render_template

from ..db import get_db
from ..merch_products import PRODUCTS as MERCH_PRODUCTS
from ..news_fetch import TEAMS
from ..schedule_fetch import get_upcoming_games
from ..social_feed import get_latest_long_form, get_recent_videos

bp = Blueprint("main", __name__)


@bp.route("/")
def home():
    db = get_db()
    featured_post = db.execute(
        "SELECT * FROM posts WHERE published = 1 ORDER BY created_at DESC LIMIT 1"
    ).fetchone()

    upcoming_games = get_upcoming_games()
    team_logos = {g["team"]: g["my_logo"] for g in upcoming_games}

    stories_by_team = {}
    for team in TEAMS:
        stories_by_team[team] = db.execute(
            "SELECT * FROM news_items WHERE team = ? ORDER BY priority ASC, fetched_at DESC, id DESC LIMIT 3",
            (team,),
        ).fetchall()

    videos = get_recent_videos(limit=4)
    return render_template(
        "home.html",
        main_video=videos[0] if videos else None,
        more_videos=videos[1:4],
        long_form=get_latest_long_form(),
        featured_post=featured_post,
        upcoming_games=upcoming_games,
        team_logos=team_logos,
        stories_by_team=stories_by_team,
        merch_products=MERCH_PRODUCTS,
    )
