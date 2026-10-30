Este proyecto permite profundizar la ruta de aprendizaje desarrollo y consumo de APIs. STACK Flask con API nativa, que es fundamental para aprender y enseñar conceptos de programación distribuida.

backend/ (V1)
- Validación de JSON, campos, id, edad y longitudes.
- Manejo de errores MySQL con respuestas JSON.
- 409 si el id ya existe.
- Cierre garantizado de conexiones y cursores con finally.
- rowcount leído antes de cerrar el cursor y manejo correcto del caso “sin cambios”.
- Conexión con charset='utf8mb4'.
- database.sql trabaja insertarndo id manualmente.

backendv2/ (V2)
- get_db() no devuelve None: relanza el error para que el controlador responda JSON.
- 409 cuando el id ya existe.
- PUT devuelve correctamente el estudiante aunque los valores no cambien.
- CORS registrado dentro de create_app.
- README actualizado con las rutas /api/v2/....

frontend/ (V1)
- API_URL apunta a http://localhost:5000/api/v1/estudiantes.
- Lee correctamente respuesta.data y también tolera un arreglo plano.
- Envía el id como entero en el POST.
- En el PUT no envía id en el cuerpo.
- Corrige el mensaje de creado/actualizado.
- El botón Cancelar sale del modo edición.
- El id queda bloqueado mientras se edita.
- Manejo de errores del backend con mensajes claros.

frontendv2/ (V2)
- API_URL apunta a http://localhost:5000/api/v2/estudiantes.
- Envía el id como entero en el POST.
- En el PUT no envía id en el cuerpo.
- Notificaciones de éxito/error usando el área ya existente del diseño.
- Botón Cancelar oculto inicialmente.
- Campo de búsqueda funcionando (nombre, apellido o carrera).
- Validaciones y mensajes del servidor mostrados al usuario.

Verificaciones realizadas
Ambos backends contra MySQL con: listar, consultar por ID, crear, crear duplicado, datos inválidos, actualizar, actualizar con los mismos valores, eliminar, eliminar inexistente y preflight OPTIONS/CORS. Todo respondió correctamente y los registros de prueba fueron eliminados.

Cómo ejecutar
Backend V1:
.\venv\Scripts\python.exe .\backend\app.py

Backend V2:
.\venv\Scripts\python.exe .\backendv2\app.py

Ambos usan el puerto 5000, así que ejecuta uno a la vez. Luego abre frontend/index.html o frontendv2/index.html.
Si quieres usar un frontend con el backend contrario, solo cambia la constante API_URL al inicio de su js/app.js; ambos ya son compatibles con las dos versiones de la API.