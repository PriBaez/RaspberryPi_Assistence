from flask import Flask

app = Flask(__name__)

# Configuración de la base de datos, sesiones, etc.
from app.repositories import sqlite_repository, init_sqlite_db
# Importar controladores
from app.controllers import DepartamentoController
from app.controllers import PuestoController
from app.controllers import EmpleadoController
from app.controllers.DepartamentoController import departamento_bp 
from app.controllers.PuestoController import puesto_bp
from app.controllers.EmpleadoController import empleado_bp

app.register_blueprint(departamento_bp, url_prefix='/api')
app.register_blueprint(puesto_bp, url_prefix='/api')
app.register_blueprint(empleado_bp, url_prefix='/api')
