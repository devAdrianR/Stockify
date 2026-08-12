from flask import Flask
import os
import mysql.connector as mysql
from dotenv import load_dotenv
from config import DB_CONFIG

from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp
from routes.usuarios_routes import usuarios_bp
from routes.inventario_routes import inventario_bp
from routes.ventas_routes import ventas_bp
from routes.finanzas_routes import finanzas_bp
from routes.reportes_routes import reportes_bp
from routes.empresas_routes import empresas_bp
from routes.crud_usuarios_routes import crud_usuarios_bp
from routes.ingresos_routes import ingresos_bp

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

try:
    con = mysql.connect(**DB_CONFIG)
    cursor = con.cursor()
    cursor.execute("SELECT DATABASE()")
    cursor.fetchone()
    print("Conexión exitosa a la base de datos")
    con.close()
except Exception as e:
    print(f"Error en la conexión: {e}")

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(inventario_bp)
app.register_blueprint(ventas_bp)
app.register_blueprint(finanzas_bp)
app.register_blueprint(reportes_bp)
app.register_blueprint(empresas_bp)
app.register_blueprint(crud_usuarios_bp)
app.register_blueprint(ingresos_bp)

if __name__ == "__main__":
    app.run(debug=True)