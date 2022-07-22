from flask import Flask

from .app1.views import api_bp
from config import Config


def init_app():
    flask_app = Flask(__name__)
    flask_app.config.from_object(Config)
    flask_app.register_blueprint(api_bp)
    return flask_app

# https://www.cnblogs.com/chaojiyingxiong/p/15058833.html
