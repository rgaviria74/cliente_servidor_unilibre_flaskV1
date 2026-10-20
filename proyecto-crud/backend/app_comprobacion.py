from flask import Flask, jsonify
from importlib import import_module

app = Flask(__name__)

# Configuración de MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'universidad_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'   # retorna dicts en vez de tuplas

try:
    MySQL = import_module('flask_mysqldb').MySQL
    mysql = MySQL(app)
except ModuleNotFoundError:
    mysql = None


# ── Función auxiliar de diagnóstico ───────────────────────────────
def test_conexion():
    """Intenta abrir cursor y ejecutar un ping. Retorna (ok, mensaje)."""
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT VERSION() AS version, DATABASE() AS base, NOW() AS servidor_hora")
        info = cur.fetchone()
        cur.close()
        return True, info
    except Exception as e:
        return False, str(e)


@app.route('/')
def inicio():
    ok, resultado = test_conexion()

    if ok:
        return jsonify({
            "estado":        "Conexion exitosa",
            "aplicacion":    "Universidad Libre",
            "base_de_datos": app.config['MYSQL_DB'],
            "host":          app.config['MYSQL_HOST'],
            "mysql_version": resultado['version'],
            "hora_servidor": str(resultado['servidor_hora']),
        }), 200
    else:
        return jsonify({
            "estado": "Error de conexion",
            "error":  resultado,
            "posibles_causas": [
                "MySQL/MariaDB no está corriendo",
                "Credenciales incorrectas",
                f"Base de datos '{app.config['MYSQL_DB']}' no existe",
                f"Puerto {app.config['MYSQL_PORT']} bloqueado",
            ]
        }), 500


@app.route('/ping')
def ping():
    """Endpoint liviano solo para verificar que Flask responde."""
    return jsonify({"estado": "ok", "mensaje": "Servidor Unilibre Funcionando sin prueba de BD"}), 200

@app.route('/tablas')
def listar_tablas():
    """Lista las tablas de la base de datos conectada."""
    try:
        cur = mysql.connection.cursor()
        cur.execute("SHOW TABLES")
        tablas = [list(fila.values())[0] for fila in cur.fetchall()]
        cur.close()
        return jsonify({
            "base_de_datos": app.config['MYSQL_DB'],
            "total_tablas":  len(tablas),
            "tablas":        tablas
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("\n─── Universidad Libre — Servidor Flask ───")
    print(f"  Host BD : {app.config['MYSQL_HOST']}:{app.config['MYSQL_PORT']}")
    print(f"  Base    : {app.config['MYSQL_DB']}")
    print(f"  Usuario : {app.config['MYSQL_USER']}")
    print("  Rutas disponibles:")
    print("    /         → diagnóstico completo de conexión")
    print("    /ping     → verificar que Flask responde")
    print("    /tablas   → listar tablas de la BD")
    print("──────────────────────────────────────────\n")
    app.run(debug=True)
