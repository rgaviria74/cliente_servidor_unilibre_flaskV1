from database.connection import get_db

COLUMNAS = "id, nombre, apellido, edad, carrera, fecha_creacion"

def listar():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(f"SELECT {COLUMNAS} FROM estudiantes ORDER BY id")
        return cursor.fetchall()
    finally:
        cursor.close()

def obtener_por_id(estudiante_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(f"SELECT {COLUMNAS} FROM estudiantes WHERE id = %s", (estudiante_id,))
        return cursor.fetchone()
    finally:
        cursor.close()

def crear(dto):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            """INSERT INTO estudiantes (id, nombre, apellido, edad, carrera)
               VALUES (%s, %s, %s, %s, %s)""",
            (dto.id, dto.nombre, dto.apellido, dto.edad, dto.carrera),
        )
        db.commit()
        nuevo_id = dto.id
    except Exception:
        db.rollback()
        raise
    finally:
        cursor.close()
    return obtener_por_id(nuevo_id)

def actualizar(estudiante_id, dto):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            """UPDATE estudiantes
               SET nombre = %s, apellido = %s, edad = %s, carrera = %s
               WHERE id = %s""",
            (dto.nombre, dto.apellido, dto.edad, dto.carrera, estudiante_id),
        )
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        cursor.close()
    # Se consulta la fila para distinguir "no existe" de "sin cambios":
    # MySQL devuelve rowcount 0 si los valores enviados son idénticos.
    return obtener_por_id(estudiante_id)

def eliminar(estudiante_id):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM estudiantes WHERE id = %s", (estudiante_id,))
        eliminado = cursor.rowcount > 0
        db.commit()
        return eliminado
    except Exception:
        db.rollback()
        raise
    finally:
        cursor.close()
