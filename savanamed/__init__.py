from flask import Flask
from .config import configure_app, configure_routes, configure_inject
from .db import init_db


def create_app() -> Flask:
    app = Flask(__name__)

    configure_app(app)
    configure_inject()
    configure_routes(app)

    with app.app_context():
        init_db()

    return app
