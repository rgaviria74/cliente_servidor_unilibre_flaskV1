from config import DatabaseConfig

class estudiantes:
    def __init__(self, id=None, nombre=None, apellido=None, edad=None, carrera=None):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.carrera = carrera

    @staticmethod
    def crear_tabla():
        connection = DatabaseConfig.get_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS estudiantes (
                    id INT PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    apellido VARCHAR(100) NOT NULL,
                    edad INT NOT NULL,
                    carrera VARCHAR(100) NOT NULL,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            connection.commit()
            cursor.close()
            connection.close() 