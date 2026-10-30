import os

class Config:
    # Ajusta estas variables según tu instalación local de MySQL/MariaDB.
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "universidad_db")
    DEBUG = os.getenv("FLASK_DEBUG", "1") == "1"
