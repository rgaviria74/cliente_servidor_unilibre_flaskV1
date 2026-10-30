import importlib

class DatabaseConfig:
    HOST = 'localhost'
    USER = 'root'
    PASSWORD = ''
    DATABASE = 'universidad_db'

    @staticmethod
    def get_connection():
        try:
            mysql_connector = importlib.import_module('mysql.connector')
            connection = mysql_connector.connect(
                host=DatabaseConfig.HOST,
                user=DatabaseConfig.USER,
                password=DatabaseConfig.PASSWORD,
                database=DatabaseConfig.DATABASE,
                charset='utf8mb4'
            )
            if connection.is_connected():
                return connection
        except Exception as e:
            print(f"Error al conectar al Servidor de MySQL: {e}")
            return None
