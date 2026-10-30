CREATE DATABASE IF NOT EXISTS universidad_db;
USE universidad_db;

CREATE TABLE IF NOT EXISTS estudiantes (
    id INT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    edad INT NOT NULL,
    carrera VARCHAR(150) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Datos de ejemplo (el id no es AUTO_INCREMENT, por eso se indica manualmente)
INSERT IGNORE INTO estudiantes (id, nombre, apellido, edad, carrera) VALUES
(1, 'Juan', 'Pérez', 20, 'Ingeniería de Sistemas'),
(2, 'María', 'González', 22, 'Ingeniería Industrial'),
(3, 'Carlos', 'Rodríguez', 21, 'Ingeniería Electrónica');