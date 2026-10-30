from flask import jsonify, request
from importlib import import_module

try:
    MySQLError = import_module("mysql.connector").Error
except ModuleNotFoundError:
    MySQLError = Exception
    
from repositories import estudiante_repository as repo
from serializers.estudiante_serializer import (
    cargar_crear_estudiante,
    cargar_actualizar_estudiante,
    estudiante_a_json,
)

#Controller asociado al Endpoint para obtener todos los estudiantes (GET - SELECT) 
def listar_estudiantes():
    try:
        data = [estudiante_a_json(row) for row in repo.listar()]
        return jsonify({"data": data}), 200 
    except MySQLError:
        return jsonify({"error": "No fue posible consultar los estudiantes."}), 500


#Controller asociado al Endpoint para obtener un estudiante por ID (GET - SELECT) 
def obtener_estudiante(estudiante_id):
    try:
        row = repo.obtener_por_id(estudiante_id)
        if row is None:
            return jsonify({"error": "Estudiante no encontrado."}), 404
        return jsonify({"data": estudiante_a_json(row)}), 200
    except MySQLError:
        return jsonify({"error": "No fue posible consultar el estudiante."}), 500

#Controller asociado al Endpoint para crear un estudiante (POST - INSERT)
def crear_estudiante():
    try:
        dto = cargar_crear_estudiante(request.get_json(silent=True))
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    try:
        row = repo.crear(dto)
        return jsonify({"mensaje": "Estudiante creado correctamente.", "data": estudiante_a_json(row)}), 201
    except MySQLError as exc:
        if getattr(exc, "errno", None) == 1062:
            return jsonify({"error": f"Ya existe un estudiante con el id {dto.id}."}), 409
        return jsonify({"error": "No fue posible crear el estudiante."}), 500

#Controller asociado al Endpoint para actualizar un estudiante por ID (PUT - UPDATE)
def actualizar_estudiante(estudiante_id):
    try:
        dto = cargar_actualizar_estudiante(request.get_json(silent=True))
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    try:
        row = repo.actualizar(estudiante_id, dto)
        if row is None:
            return jsonify({"error": "Estudiante no encontrado."}), 404
        return jsonify({"mensaje": "Estudiante actualizado correctamente.", "data": estudiante_a_json(row)}), 200
    except MySQLError:
        return jsonify({"error": "No fue posible actualizar el estudiante."}), 500

#Controller asociado al Endpoint para eliminar un estudiante por ID (DELETE - DELETE)
def eliminar_estudiante(estudiante_id):
    try:
        eliminado = repo.eliminar(estudiante_id)
        if not eliminado:
            return jsonify({"error": "Estudiante no encontrado."}), 404
        return jsonify({"mensaje": "Estudiante eliminado correctamente."}), 200
    except MySQLError:
        return jsonify({"error": "No fue posible eliminar el estudiante."}), 500
