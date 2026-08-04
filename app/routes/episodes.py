from flask import Blueprint, render_template

from ..social_feed import get_all_long_form

bp = Blueprint("episodes", __name__, url_prefix="/episodes")


@bp.route("/")
def index():
    return render_template("episodes.html", episodes=get_all_long_form())
