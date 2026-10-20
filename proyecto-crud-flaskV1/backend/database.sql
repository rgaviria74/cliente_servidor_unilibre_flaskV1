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

-- Datos de ejemplo
INSERT INTO estudiantes (nombre, apellido, edad, carrera) VALUES
('Juan', 'Pérez', 20, 'Ingeniería de Sistemas'),
('María', 'González', 22, 'Ingeniería Industrial'),
('Carlos', 'Rodríguez', 21, 'Ingeniería Electrónica');