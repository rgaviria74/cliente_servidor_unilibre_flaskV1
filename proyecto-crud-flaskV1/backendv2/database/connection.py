from importlib import import_module

mysql_connector = import_module("mysql.connector")
from flask import current_app, g

def get_db():
    """Una conexión por contexto de solicitud; se reutiliza dentro de la solicitud."""
    try:
        if "db" not in g:
            g.db = mysql_connector.connect(
                host=current_app.config["MYSQL_HOST"],
                port=current_app.config["MYSQL_PORT"],
                user=current_app.config["MYSQL_USER"],
                password=current_app.config["MYSQL_PASSWORD"],
                database=current_app.config["MYSQL_DATABASE"],
                charset="utf8mb4",
            )
        return g.db
    except mysql_connector.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        # Se relanza para que el controlador responda con un JSON de error
        # en lugar de fallar con un AttributeError sobre None.
        raise
    

def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None and db.is_connected():
        db.close() 
