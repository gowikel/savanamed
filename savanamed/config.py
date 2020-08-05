from flask import Flask

import os
import inject

base_dir = os.path.abspath(os.path.dirname(__file__))
default_secret = ('6e7db0423fcdc2a5495209954a0d3192'
                  'e6ef3385eba8c037ee2dd75dbab456f5')


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', default_secret)

    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
    MONGO_DATABASE = os.environ.get('MONGO_DATABASE', 'savanamed_development')
    MONGO_USERNAME = os.environ.get('MONGO_USERNAME')
    MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')

    JSON_SORT_KEYS = True

    @staticmethod
    def init_app(app: Flask) -> None:
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    JSONIFY_PRETTYPRINT_REGULAR = True
    EXPLAIN_TEMPLATE_LOADING = True


class TestingConfig(Config):
    TESTING = True
    JSONIFY_PRETTYPRINT_REGULAR = True
    MONGO_DATABASE = 'savanamed_test'


class ProductionConfig(Config):
    pass


def configure_app(app: Flask) -> None:
    env = os.environ.get('FLASK_ENV')

    config_obj = DevelopmentConfig
    if env == 'testing':
        config_obj = TestingConfig
    elif env == 'production':
        config_obj = ProductionConfig

    app.config.from_object(config_obj)


def configure_routes(app: Flask) -> None:
    from .pdf2text.routes import create_blueprint as pdf2text_bp
    app.register_blueprint(pdf2text_bp(), url_prefix='/api/v1/pdf2text')

    from .service_status.routes import create_blueprint as service_status_bp
    app.register_blueprint(service_status_bp(), url_prefix='/status')


def configure_inject() -> None:
    def config(binder: inject.Binder) -> None:
        from .pdf2text import inject_configuration
        binder.install(inject_configuration)

    inject.configure(config)
