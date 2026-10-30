from flask import Blueprint
from controllers import estudiantes_controller as controller

estudiantes_bp = Blueprint("estudiantes", __name__)

estudiantes_bp.get("")(controller.listar_estudiantes)
estudiantes_bp.get("/<int:estudiante_id>")(controller.obtener_estudiante)
estudiantes_bp.post("")(controller.crear_estudiante)
estudiantes_bp.put("/<int:estudiante_id>")(controller.actualizar_estudiante)
estudiantes_bp.delete("/<int:estudiante_id>")(controller.eliminar_estudiante)
 