from flask import Flask
from flask_cors import CORS
from api_tarefas import bp 
from api_tarefas.routes import init_routes
import os

app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')
CORS(app)

# Inicializa as rotas passando o bp
init_routes(bp)


# Registra o blueprint
app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(debug=True)
