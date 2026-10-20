from flask import jsonify, request, Blueprint
from config import DatabaseConfig

estudiantes_bp = Blueprint('estudiantes', __name__)

#Rutas CRUD para la entidad "estudiantes"
#Endpoint para crear un nuevo estudiante (POST -INSERT) 
@estudiantes_bp.route('/api/v1/estudiantes', methods=['POST'])
def crear_estudiante():
    data = request.get_json()
    connection = DatabaseConfig.get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO estudiantes (id, nombre, apellido, edad, carrera)
            VALUES (%s, %s, %s, %s, %s)
        """, (data['id'], data['nombre'], data['apellido'], data['edad'], data['carrera']))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"mensaje": "Estudiante creado exitosamente", "id": data['id']}), 201
    
    return jsonify({"error": "Error al crear el estudiante"}), 500

#Endpoint para obtener todos los estudiantes (GET - SELECT)
@estudiantes_bp.route('/api/v1/estudiantes', methods=['GET'])
def obtener_estudiantes():
    connection = DatabaseConfig.get_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM estudiantes ORDER BY id")
        estudiantes = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(estudiantes), 200
    
    return jsonify({"error": "Error al obtener los estudiantes"}), 500

#Endpoint para obtener un estudiante por ID (GET - SELECT)
@estudiantes_bp.route('/api/v1/estudiantes/<int:id>', methods=['GET'])
def obtener_estudiante(id):
    connection = DatabaseConfig.get_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM estudiantes WHERE id = %s", (id,))
        estudiante = cursor.fetchone()
        cursor.close()
        connection.close()
        if estudiante:
            return jsonify(estudiante), 200
        else:
            return jsonify({"error": "Estudiante no encontrado"}), 404
    
    return jsonify({"error": "Error al obtener el estudiante"}), 500

#Endpoint para actualizar un estudiante por ID (PUT - UPDATE)
@estudiantes_bp.route('/api/v1/estudiantes/<int:id>', methods=['PUT'])
def actualizar_estudiante(id):
    data = request.get_json()
    connection = DatabaseConfig.get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE estudiantes
            SET nombre = %s, apellido = %s, edad = %s, carrera = %s
            WHERE id = %s
        """, (data['nombre'], data['apellido'], data['edad'], data['carrera'], id))
        connection.commit()
        cursor.close()
        connection.close()
        if cursor.rowcount > 0:
            return jsonify({"mensaje": "Estudiante actualizado exitosamente"}), 200
        else:
            return jsonify({"error": "Estudiante no encontrado"}), 404
    
    return jsonify({"error": "Error al actualizar el estudiante"}), 500 

#Endpoint para eliminar un estudiante por ID (DELETE - DELETE)
@estudiantes_bp.route('/api/v1/estudiantes/<int:id>', methods=['DELETE'])
def eliminar_estudiante(id):
    connection = DatabaseConfig.get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM estudiantes WHERE id = %s", (id,))
        connection.commit()
        cursor.close()
        connection.close()
        if cursor.rowcount > 0:
            return jsonify({"mensaje": "Estudiante eliminado exitosamente"}), 200
        else:
            return jsonify({"error": "Estudiante no encontrado"}), 404
    
    return jsonify({"error": "Error al eliminar el estudiante"}), 500