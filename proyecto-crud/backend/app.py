from flask import Flask, jsonify
from routes.estudiantes import estudiantes_bp
from models import estudiantes


app = Flask(__name__)

# Permite solicitudes de origen cruzado (CORS) para todas las rutas sin una dependencia adicional.
@app.after_request
def agregar_encabezados_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

app.register_blueprint(estudiantes_bp)
#app.register_blueprint(estudiantes_bp, url_prefix='/api/v1/estudiantes')

@app.route('/')
def index():
    return {'mensaje': 'API de Estudiantes - Universidad Libre'}, 200

if __name__ == '__main__':
    # Crear la tabla de estudiantes si no existe
    estudiantes.crear_tabla()
    print("\n─── Universidad Libre — Servidor Iniciado")
    app.run(debug=True)
