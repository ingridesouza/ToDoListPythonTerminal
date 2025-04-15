from flask import Blueprint

bp = Blueprint('api_tarefas', __name__)


def init_app(app):
    from . import routes 
    app.register_blueprint(bp)
    routes.register_routes(bp)