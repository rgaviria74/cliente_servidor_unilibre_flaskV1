from flask import Blueprint, jsonify, request

from config import DatabaseConfig

try:
    from mysql.connector import Error as MySQLError
except ImportError:  # pragma: no cover - solo si falta la dependencia
    MySQLError = Exception

estudiantes_bp = Blueprint('estudiantes', __name__)

CAMPOS_EDITABLES = ('nombre', 'apellido', 'edad', 'carrera')
LONGITUDES = {'nombre': 100, 'apellido': 100, 'carrera': 150}


class ConexionError(Exception):
    """Se lanza cuando no es posible abrir la conexión con MySQL."""


def _error(mensaje, codigo=400):
    return jsonify({'error': mensaje}), codigo


def _obtener_json(campos_obligatorios):
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ValueError('El cuerpo de la solicitud debe ser un objeto JSON.')
    faltantes = [campo for campo in campos_obligatorios if campo not in data]
    if faltantes:
        raise ValueError('Faltan campos obligatorios: ' + ', '.join(faltantes) + '.')
    return data


def _validar_texto(data, campo):
    valor = data.get(campo)
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f"El campo '{campo}' es obligatorio y debe ser texto.")
    valor = valor.strip()
    if len(valor) > LONGITUDES[campo]:
        raise ValueError(
            f"El campo '{campo}' no puede superar {LONGITUDES[campo]} caracteres."
        )
    return valor


def _validar_edad(data):
    valor = data.get('edad')
    if isinstance(valor, bool) or not isinstance(valor, (int, str)):
        raise ValueError("El campo 'edad' debe ser un número entero.")
    try:
        valor = int(valor)
    except (TypeError, ValueError):
        raise ValueError("El campo 'edad' debe ser un número entero.") from None
    if valor < 0 or valor > 120:
        raise ValueError("El campo 'edad' debe estar entre 0 y 120.")
    return valor


def _validar_id(data):
    valor = data.get('id')
    if isinstance(valor, bool) or not isinstance(valor, (int, str)):
        raise ValueError("El campo 'id' debe ser un número entero.")
    try:
        valor = int(valor)
    except (TypeError, ValueError):
        raise ValueError("El campo 'id' debe ser un número entero.") from None
    if valor <= 0:
        raise ValueError("El campo 'id' debe ser un entero positivo.")
    return valor


def _validar_estudiante(data):
    """Valida los campos editables y devuelve los valores normalizados."""
    return {
        'nombre': _validar_texto(data, 'nombre'),
        'apellido': _validar_texto(data, 'apellido'),
        'edad': _validar_edad(data),
        'carrera': _validar_texto(data, 'carrera'),
    }


def _conectar():
    conexion = DatabaseConfig.get_connection()
    if conexion is None:
        raise ConexionError('No fue posible conectar con la base de datos.')
    return conexion


def _cerrar(conexion, cursor):
    if cursor is not None:
        try:
            cursor.close()
        except Exception:
            pass
    if conexion is not None:
        try:
            if conexion.is_connected():
                conexion.close()
        except Exception:
            pass


# Endpoint para obtener todos los estudiantes (GET - SELECT)
@estudiantes_bp.route('/api/v1/estudiantes', methods=['GET'])
def obtener_estudiantes():
    conexion = cursor = None
    try:
        conexion = _conectar()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute('SELECT * FROM estudiantes ORDER BY id')
        filas = cursor.fetchall()
        return jsonify({'data': filas}), 200
    except ConexionError as exc:
        return _error(str(exc), 503)
    except MySQLError as exc:
        print(f'Error al obtener los estudiantes: {exc}')
        return _error('No fue posible obtener los estudiantes.', 500)
    finally:
        _cerrar(conexion, cursor)


# Endpoint para obtener un estudiante por ID (GET - SELECT)
@estudiantes_bp.route('/api/v1/estudiantes/<int:id>', methods=['GET'])
def obtener_estudiante(id):
    conexion = cursor = None
    try:
        conexion = _conectar()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute('SELECT * FROM estudiantes WHERE id = %s', (id,))
        estudiante = cursor.fetchone()
        if estudiante is None:
            return _error('Estudiante no encontrado.', 404)
        return jsonify({'data': estudiante}), 200
    except ConexionError as exc:
        return _error(str(exc), 503)
    except MySQLError as exc:
        print(f'Error al obtener el estudiante: {exc}')
        return _error('No fue posible obtener el estudiante.', 500)
    finally:
        _cerrar(conexion, cursor)


# Endpoint para crear un nuevo estudiante (POST - INSERT)
@estudiantes_bp.route('/api/v1/estudiantes', methods=['POST'])
def crear_estudiante():
    try:
        data = _obtener_json(('id',) + CAMPOS_EDITABLES)
        id_estudiante = _validar_id(data)
        valores = _validar_estudiante(data)
    except ValueError as exc:
        return _error(str(exc), 400)

    conexion = cursor = None
    try:
        conexion = _conectar()
        cursor = conexion.cursor()
        cursor.execute(
            """INSERT INTO estudiantes (id, nombre, apellido, edad, carrera)
               VALUES (%s, %s, %s, %s, %s)""",
            (
                id_estudiante,
                valores['nombre'],
                valores['apellido'],
                valores['edad'],
                valores['carrera'],
            ),
        )
        conexion.commit()
        return jsonify({
            'mensaje': 'Estudiante creado exitosamente.',
            'id': id_estudiante,
        }), 201
    except ConexionError as exc:
        return _error(str(exc), 503)
    except MySQLError as exc:
        if conexion is not None:
            conexion.rollback()
        if getattr(exc, 'errno', None) == 1062:
            return _error(f'Ya existe un estudiante con el id {id_estudiante}.', 409)
        print(f'Error al crear el estudiante: {exc}')
        return _error('No fue posible crear el estudiante.', 500)
    finally:
        _cerrar(conexion, cursor)


# Endpoint para actualizar un estudiante por ID (PUT - UPDATE)
@estudiantes_bp.route('/api/v1/estudiantes/<int:id>', methods=['PUT'])
def actualizar_estudiante(id):
    try:
        data = _obtener_json(CAMPOS_EDITABLES)
        valores = _validar_estudiante(data)
    except ValueError as exc:
        return _error(str(exc), 400)

    conexion = cursor = None
    try:
        conexion = _conectar()
        cursor = conexion.cursor()
        cursor.execute(
            """UPDATE estudiantes
               SET nombre = %s, apellido = %s, edad = %s, carrera = %s
               WHERE id = %s""",
            (
                valores['nombre'],
                valores['apellido'],
                valores['edad'],
                valores['carrera'],
                id,
            ),
        )
        filas_afectadas = cursor.rowcount
        conexion.commit()

        # MySQL devuelve 0 cuando los valores enviados son idénticos a los
        # existentes; se comprueba la existencia para no responder 404 por error.
        if filas_afectadas == 0:
            cursor.execute('SELECT id FROM estudiantes WHERE id = %s', (id,))
            if cursor.fetchone() is None:
                return _error('Estudiante no encontrado.', 404)

        return jsonify({'mensaje': 'Estudiante actualizado exitosamente.'}), 200
    except ConexionError as exc:
        return _error(str(exc), 503)
    except MySQLError as exc:
        if conexion is not None:
            conexion.rollback()
        print(f'Error al actualizar el estudiante: {exc}')
        return _error('No fue posible actualizar el estudiante.', 500)
    finally:
        _cerrar(conexion, cursor)


# Endpoint para eliminar un estudiante por ID (DELETE - DELETE)
@estudiantes_bp.route('/api/v1/estudiantes/<int:id>', methods=['DELETE'])
def eliminar_estudiante(id):
    conexion = cursor = None
    try:
        conexion = _conectar()
        cursor = conexion.cursor()
        cursor.execute('DELETE FROM estudiantes WHERE id = %s', (id,))
        eliminados = cursor.rowcount
        conexion.commit()
        if eliminados == 0:
            return _error('Estudiante no encontrado.', 404)
        return jsonify({'mensaje': 'Estudiante eliminado exitosamente.'}), 200
    except ConexionError as exc:
        return _error(str(exc), 503)
    except MySQLError as exc:
        if conexion is not None:
            conexion.rollback()
        print(f'Error al eliminar el estudiante: {exc}')
        return _error('No fue posible eliminar el estudiante.', 500)
    finally:
        _cerrar(conexion, cursor)
