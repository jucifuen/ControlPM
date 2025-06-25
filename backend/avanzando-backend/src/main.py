import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.routes.auth import auth_bp
from src.routes.projects import projects_bp
from src.routes.kpis import kpis_bp
from src.routes.riesgos import riesgos_bp
from src.routes.recursos import recursos_bp
from src.routes.portfolio import portfolio_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Habilitar CORS
CORS(app)
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(projects_bp, url_prefix='/api')
app.register_blueprint(kpis_bp, url_prefix='/api')
app.register_blueprint(riesgos_bp, url_prefix='/api')
app.register_blueprint(recursos_bp, url_prefix='/api')
app.register_blueprint(portfolio_bp, url_prefix='/api')

# Configurar base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    # Importar todos los modelos para crear las tablas
    from src.models.user import User
    from src.models.project import Proyecto, Fase
    from src.models.kpi import KPI
    from src.models.riesgo import Riesgo
    from src.models.recurso import Recurso
    db.create_all()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
