from flask import Blueprint, render_template

from ..merch_products import PRODUCTS, STORE_URL

bp = Blueprint("shop", __name__, url_prefix="/shop")


@bp.route("/")
def index():
    return render_template("shop.html", products=PRODUCTS, store_url=STORE_URL)
