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

    @staticmethod
    def obtener_todos():
        connection = DatabaseConfig.get_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM estudiantes")
            resultados = cursor.fetchall()
            cursor.close()
            connection.close()
            return resultados
        else:
            return None

    @staticmethod
    def obtener_por_id(estudiante_id):
        connection = DatabaseConfig.get_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM estudiantes WHERE id = %s", (estudiante_id,))
            resultado = cursor.fetchone()
            cursor.close()
            connection.close()
            return resultado
        else:
            return None

    def guardar(self):
        connection = DatabaseConfig.get_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO estudiantes (nombre, apellido, edad) VALUES (%s, %s, %s)",
                (self.nombre, self.apellido, self.edad)
            )
            connection.commit()
            self.id = cursor.lastrowid
            cursor.close()
            connection.close()

    def actualizar(self):
        connection = DatabaseConfig.get_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE estudiantes SET nombre=%s, apellido=%s, edad=%s WHERE id=%s",
                (self.nombre, self.apellido, self.edad, self.id)
            )
            connection.commit()
            cursor.close()
            connection.close()

    def eliminar(self):
        connection = DatabaseConfig.get_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM estudiantes WHERE id=%s", (self.id,))
            connection.commit()
            cursor.close()
            connection.close()