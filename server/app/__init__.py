from flask import Flask

app = Flask(__name__)

# Configuración de la base de datos, sesiones, etc.
from .repositories import sqlite_repository, GoogleRepository
# Importar controladores
from .controllers import DepartamentoController
from .controllers import PuestoController
from .controllers import EmpleadoController
from .controllers.DepartamentoController import departamento_bp 
from .controllers.PuestoController import puesto_bp
from .controllers.EmpleadoController import empleado_bp
from .controllers.NetworkManagerController import network_bp
from .controllers.HistorialController import historial_bp

app.register_blueprint(departamento_bp, url_prefix='/api')
app.register_blueprint(puesto_bp, url_prefix='/api')
app.register_blueprint(empleado_bp, url_prefix='/api')
app.register_blueprint(network_bp, url_prefix='/api')
app.register_blueprint(historial_bp, url_prefix='/api')
