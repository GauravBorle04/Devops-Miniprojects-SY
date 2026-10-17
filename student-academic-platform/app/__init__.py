from flask import Flask


def create_app():
    app = Flask(__name__)
    from app.routes.api import api_bp
    from app.routes.web import web_bp
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(web_bp)
    return app
