import logging
from flask import request, g
from time import perf_counter

def register_logging_middleware(app):
    logging.basicConfig(level=logging.INFO)
    @app.before_request
    def log_request_start():
        g.request_start = perf_counter()
        app.logger.info("Solicitud %s %s", request.method, request.path)

    @app.after_request
    def log_request_end(response):
        inicio = getattr(g, "request_start", None)
        if inicio is not None:
            duracion_ms = (perf_counter() - inicio) * 1000
            app.logger.info("Respuesta %s %s -> %s (%.2f ms)",
                            request.method, request.path, response.status_code, duracion_ms)
        return response
