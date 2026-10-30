from dataclasses import dataclass

@dataclass(frozen=True)
class CrearEstudianteDTO:
    id: int
    nombre: str
    apellido: str
    edad: int
    carrera: str

@dataclass(frozen=True)
class ActualizarEstudianteDTO:
    nombre: str
    apellido: str
    edad: int
    carrera: str
