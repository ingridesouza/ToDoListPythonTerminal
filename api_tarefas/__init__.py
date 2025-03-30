from flask import Blueprint
from . import routes

bp = Blueprint('api', __name__, url_prefix='/api')

def init_app(app):
    from . import routes 
    app.register_blueprint(bp)
    routes.register_routes(bp)