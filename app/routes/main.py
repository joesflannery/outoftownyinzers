from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from ..auth import check_password
from ..db import get_db
from ..merch_products import PRODUCTS as MERCH_PRODUCTS
from ..news_fetch import TEAMS
from ..schedule_fetch import get_upcoming_games
from ..social_feed import get_latest_long_form, get_recent_videos

bp = Blueprint("main", __name__)

# Fill these in once real show links exist -- the Hero CTAs on the
# homepage only render a button when the corresponding URL is set, so
# leaving these None just hides that button rather than linking nowhere.
SPOTIFY_URL = None
APPLE_PODCASTS_URL = None

# The homepage shows the full catalog as a scrollable strip, but these lead
# so the highest-appeal items are visible before anyone scrolls.
PRIMARY_HOME_PRODUCT_IMAGES = [
    "bridge-gray-t-shirt.png",
    "sweatshirt.png",
    "toddler-tee.png",
    "trucker-hat.png",
]


def _home_product_order():
    by_image = {p["image"].rsplit("/", 1)[-1]: p for p in MERCH_PRODUCTS}
    primary = [by_image[name] for name in PRIMARY_HOME_PRODUCT_IMAGES]
    rest = [p for p in MERCH_PRODUCTS if p["image"].rsplit("/", 1)[-1] not in PRIMARY_HOME_PRODUCT_IMAGES]
    return primary + rest


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
        merch_products=_home_product_order(),
        spotify_url=SPOTIFY_URL,
        apple_podcasts_url=APPLE_PODCASTS_URL,
    )


@bp.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    next_url = request.values.get("next") or url_for("blog.index")
    if request.method == "POST":
        if check_password(request.form.get("password", "")):
            session["is_admin"] = True
            flash("Logged in.", "info")
            return redirect(next_url)
        flash("Wrong password.", "error")
    return render_template("admin_login.html", next=next_url)


@bp.route("/admin/logout")
def admin_logout():
    session.pop("is_admin", None)
    flash("Logged out.", "info")
    return redirect(url_for("blog.index"))
