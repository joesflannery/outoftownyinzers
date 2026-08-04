import os
from datetime import datetime

from flask import Flask


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", "yinzers-local-dev-only")

    from . import db
    db.init_app(app)

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
