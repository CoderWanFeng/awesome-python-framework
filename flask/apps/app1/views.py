from flask import Blueprint

api_bp = Blueprint("app_orders", __name__)


@api_bp.route('/index')
def index():
    return 'index'
