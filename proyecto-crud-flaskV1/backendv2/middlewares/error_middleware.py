from flask import jsonify
from werkzeug.exceptions import HTTPException

def register_error_handlers(app):
    @app.errorhandler(HTTPException)
    def manejar_http_error(error):
        return jsonify({"error": error.description}), error.code

    @app.errorhandler(Exception)
    def manejar_error_no_controlado(error):
        app.logger.exception("Error no controlado")
        return jsonify({"error": "Error interno del servidor."}), 500
