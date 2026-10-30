from flask import Flask, jsonify
from config import Config
from database.connection import close_db
from routes.estudiantes_routes import estudiantes_bp
from middlewares.error_middleware import register_error_handlers
from middlewares.logging_middleware import register_logging_middleware


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Middlewares / hooks transversales
    register_logging_middleware(app)
    register_error_handlers(app)

    # Permite solicitudes de origen cruzado (CORS) para todas las rutas sin una dependencia adicional.
    @app.after_request
    def agregar_encabezados_cors(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

    app.register_blueprint(estudiantes_bp, url_prefix="/api/v2/estudiantes")
    app.teardown_appcontext(close_db)

    @app.get("/api/v2/health")
    def health():
        return jsonify({"status": "ok", "mensaje": "API V2 universidad disponible"}), 200

    @app.route('/')
    def index():
        return {'mensaje': 'API V2 de Estudiantes - Universidad Libre'}, 200

    return app


app = create_app()

if __name__ == "__main__":
    print("\n─── Universidad Libre — Servidor Iniciado")
    app.run(debug=app.config.get("DEBUG", True))
