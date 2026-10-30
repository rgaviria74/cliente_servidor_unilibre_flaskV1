import re
from dtos.estudiante_dto import CrearEstudianteDTO, ActualizarEstudianteDTO

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")  # reservado si luego agregas correo

def _validar_texto(data, campo, maximo):
    valor = data.get(campo)
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f"'{campo}' es obligatorio y debe ser texto.")
    valor = valor.strip()
    if len(valor) > maximo:
        raise ValueError(f"'{campo}' no puede superar {maximo} caracteres.")
    return valor

def _validar_edad(data):
    valor = data.get("edad")
    # bool es subclase de int en Python; se rechaza explícitamente.
    if isinstance(valor, bool) or not isinstance(valor, int):
        raise ValueError("'edad' debe ser un número entero.")
    if valor < 0 or valor > 120:
        raise ValueError("'edad' debe estar entre 0 y 120.")
    return valor

def _validar_campos(data, campos):
    if not isinstance(data, dict):
        raise ValueError("El cuerpo debe ser un objeto JSON.")
    desconocidos = set(data) - set(campos)
    if desconocidos:
        raise ValueError(f"Campos no permitidos: {', '.join(sorted(desconocidos))}.")
    faltantes = set(campos) - set(data)
    if faltantes:
        raise ValueError(f"Faltan campos obligatorios: {', '.join(sorted(faltantes))}.")

def _validar_id(data):
    valor = data.get("id")
    if isinstance(valor, bool) or not isinstance(valor, int):
        raise ValueError("'id' es obligatorio y debe ser un número entero.")
    if valor <= 0:
        raise ValueError("'id' debe ser un entero positivo.")
    return valor

def cargar_crear_estudiante(data):
    campos = {"id", "nombre", "apellido", "edad", "carrera"}
    _validar_campos(data, campos)
    return CrearEstudianteDTO(
        id=_validar_id(data),
        nombre=_validar_texto(data, "nombre", 100),
        apellido=_validar_texto(data, "apellido", 100),
        edad=_validar_edad(data),
        carrera=_validar_texto(data, "carrera", 150),
    )

def cargar_actualizar_estudiante(data):
    campos = {"nombre", "apellido", "edad", "carrera"}
    _validar_campos(data, campos)
    return ActualizarEstudianteDTO(
        nombre=_validar_texto(data, "nombre", 100),
        apellido=_validar_texto(data, "apellido", 100),
        edad=_validar_edad(data),
        carrera=_validar_texto(data, "carrera", 150),
    )

def estudiante_a_json(row):
    """Convierte una fila de MySQL (dict) en un objeto JSON serializable."""
    return {
        "id": row["id"],
        "nombre": row["nombre"],
        "apellido": row["apellido"],
        "edad": row["edad"],
        "carrera": row["carrera"],
        "fecha_creacion": row["fecha_creacion"].isoformat(sep=" ") if row.get("fecha_creacion") else None,
    }
