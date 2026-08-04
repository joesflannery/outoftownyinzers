import os
from datetime import datetime

from flask import Flask


def create_app():
    app = Flask(__name__)

    # FLASK_ENV isn't set anywhere by default (not locally, not by
    # PythonAnywhere), so it defaults to "development" here -- meaning this
    # only actually enforces anything once FLASK_ENV=production is added to
    # the WSGI file (see DEPLOY.md). Local dev keeps using the fallback key
    # either way, since a leaked local dev session cookie isn't a real risk.
    flask_env = os.environ.get("FLASK_ENV", "development")
    secret_key = os.environ.get("SECRET_KEY")
    if flask_env != "development" and not secret_key:
        raise ValueError(
            "SECRET_KEY must be set in the environment when FLASK_ENV is not "
            "'development' -- set it in the WSGI file alongside ADMIN_PASSWORD."
        )
    app.secret_key = secret_key or "yinzers-local-dev-only"

    from . import db
    db.init_app(app)

    from . import news_fetch
    news_fetch.init_app(app)

    from .routes import main, news, blog, shop, episodes
    app.register_blueprint(main.bp)
    app.register_blueprint(news.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(shop.bp)
    app.register_blueprint(episodes.bp)

    @app.context_processor
    def inject_current_year():
        return {"current_year": datetime.now().year}

    return app
