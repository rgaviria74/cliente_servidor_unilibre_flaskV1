# Backend Flask - Universidad

CRUD REST para la tabla `estudiantes` en `universidad_db`, con Router, Controller, DTO, Serializer, Middleware y SQL nativo.

## Suposiciones de esquema

La imagen muestra una tabla con estas columnas: `id INT` (PK, no autoincremental), `nombre VARCHAR(100)`, `apellido VARCHAR(100)`, `edad INT`, `carrera VARCHAR(150)` y `fecha_creacion TIMESTAMP`, todas NOT NULL. El código supone que la tabla se llama `estudiantes`, que `id` es una clave primaria y se proporciona manualmente en cada creación, y que `fecha_creacion` tiene un valor por defecto como `CURRENT_TIMESTAMP`. Si tu tabla tiene otro nombre o `fecha_creacion` no tiene valor por defecto, ajusta el SQL.

## 1. Crear entorno e instalar dependencias (Windows PowerShell)

```powershell
py -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

Usar `venv\Scripts\python.exe` evita tener que activar el entorno si PowerShell bloquea scripts.

## 2. Configurar conexión

Define variables de entorno antes de ejecutar, o adapta `config.py`:

```powershell
$env:MYSQL_HOST="localhost"
$env:MYSQL_PORT="3306"
$env:MYSQL_USER="root"
$env:MYSQL_PASSWORD="tu_clave"
$env:MYSQL_DATABASE="universidad_db"
$env:FLASK_DEBUG="1"
```

No subas credenciales reales a Git.

## 3. Verificar la tabla

Si aún no existe, puedes crearla con:

```sql
USE universidad_db;

CREATE TABLE estudiantes (
    id INT NOT NULL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    edad INT NOT NULL,
    carrera VARCHAR(150) NOT NULL,
    fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

No ejecutes el `CREATE TABLE` si ya existe; compara primero su estructura con la de arriba. El campo `id` no es `AUTO_INCREMENT`: debes enviar un `id` entero y único en cada solicitud POST.

## 4. Ejecutar

Desde la carpeta `backendv2`:

```powershell
.\venv\Scripts\python.exe app.py
```

API: `http://127.0.0.1:5000`. Este backend y el de `backend` usan el mismo puerto,
así que ejecuta solo uno a la vez (o cambia el puerto al iniciar el segundo).

## 5. Endpoints

| Método | URL | Acción |
|---|---|---|
| GET | `/api/v2/health` | Verificar API |
| GET | `/api/v2/estudiantes` | Listar |
| GET | `/api/v2/estudiantes/1` | Consultar por ID |
| POST | `/api/v2/estudiantes` | Crear |
| PUT | `/api/v2/estudiantes/1` | Actualizar todos los campos editables |
| DELETE | `/api/v2/estudiantes/1` | Eliminar |

### JSON para POST y PUT

```json
{
  "id": 1001,
  "nombre": "Laura",
  "apellido": "Pérez",
  "edad": 20,
  "carrera": "Ingeniería de Sistemas"
}
```

En Postman selecciona `Body > raw > JSON`. Para POST usa `http://127.0.0.1:5000/api/v2/estudiantes`.
En los PUT no envíes `id` en el cuerpo: el id viaja en la URL y el DTO rechaza campos desconocidos.

## Notas

- Las consultas usan parámetros `%s` de MySQL Connector; no concatenes datos del usuario al SQL.
- El `id` se envía manualmente en el JSON de creación. Debe ser único; si ya existe, MySQL rechazará el INSERT por clave primaria duplicada.
- El controlador devuelve mensajes de error sin exponer detalles internos de la base de datos.
- El middleware de autenticación no se incluye porque no se definió un mecanismo de usuarios/tokens. El logging y el manejo general de errores sí están implementados.
- Este ejemplo no implementa paginación; se recomienda añadirla si la tabla crece.
