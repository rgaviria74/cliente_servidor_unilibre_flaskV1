// Frontend V1: consume la API V1 (backend/app.py)
// Si ejecutas el backend V2, cambia la URL a http://localhost:5000/api/v2/estudiantes
const API_URL = 'http://localhost:5000/api/v1/estudiantes';

let EDITA = false;

// Referencias al DOM
const form = document.getElementById('estudiante-form');
const formTitle = document.getElementById('form-title');
const submitBtn = document.getElementById('submit-btn');
const cancelBtn = document.getElementById('cancel-btn');
const tbody = document.getElementById('estudiantes-tbody');
const idInput = document.getElementById('estudiante-id');

// Cargar estudiantes al iniciar
document.addEventListener('DOMContentLoaded', () => {
    cargarEstudiantes();
});

// Realiza una petición y normaliza los errores devueltos por el backend.
async function peticion(url, opciones = {}) {
    const respuesta = await fetch(url, opciones);
    const tipoContenido = respuesta.headers.get('content-type') || '';
    let cuerpo = null;

    if (tipoContenido.includes('application/json')) {
        cuerpo = await respuesta.json();
    }

    if (!respuesta.ok) {
        const mensaje = cuerpo && cuerpo.error
            ? cuerpo.error
            : `Error ${respuesta.status} al comunicarse con el servidor`;
        throw new Error(mensaje);
    }

    return cuerpo;
}

// La API V1 y V2 devuelven { data: [...] }; se acepta también un arreglo plano.
function extraerDatos(respuesta) {
    if (Array.isArray(respuesta)) {
        return respuesta;
    }
    return respuesta && Array.isArray(respuesta.data) ? respuesta.data : [];
}

function escaparHtml(valor) {
    const texto = valor === null || valor === undefined ? '' : String(valor);
    return texto
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

// Función para cargar todos los estudiantes (READ)
async function cargarEstudiantes() {
    try {
        const respuesta = await peticion(API_URL);
        const estudiantes = extraerDatos(respuesta);

        tbody.innerHTML = '';

        if (estudiantes.length === 0) {
            tbody.innerHTML = `
                <tr class="empty-row">
                    <td colspan="6">No hay estudiantes registrados todavía.</td>
                </tr>
            `;
            return;
        }

        estudiantes.forEach(estudiante => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${escaparHtml(estudiante.id)}</td>
                <td>${escaparHtml(estudiante.nombre)}</td>
                <td>${escaparHtml(estudiante.apellido)}</td>
                <td>${escaparHtml(estudiante.edad)}</td>
                <td>${escaparHtml(estudiante.carrera)}</td>
                <td>
                    <button class="btn-editar" onclick="editarEstudiante(${Number(estudiante.id)})">
                        Editar
                    </button>
                    <button class="btn-eliminar" onclick="eliminarEstudiante(${Number(estudiante.id)})">
                        Eliminar
                    </button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (error) {
        console.error('Error al cargar estudiantes:', error);
        tbody.innerHTML = `
            <tr class="empty-row">
                <td colspan="6">${escaparHtml(error.message)}</td>
            </tr>
        `;
        alert('No fue posible cargar los estudiantes:\n' + error.message);
    }
}

// Función para crear o actualizar estudiante (CREATE/UPDATE)
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const id = parseInt(idInput.value, 10);
    if (!Number.isInteger(id) || id <= 0) {
        alert('El id debe ser un número entero positivo.');
        idInput.focus();
        return;
    }

    const estudiante = {
        nombre: document.getElementById('nombre').value.trim(),
        apellido: document.getElementById('apellido').value.trim(),
        edad: parseInt(document.getElementById('edad').value, 10),
        carrera: document.getElementById('carrera').value.trim(),
    };

    if (!estudiante.nombre || !estudiante.apellido || !estudiante.carrera) {
        alert('Todos los campos de texto son obligatorios.');
        return;
    }
    if (!Number.isInteger(estudiante.edad)) {
        alert('La edad debe ser un número entero.');
        return;
    }

    const eraEdicion = EDITA;
    submitBtn.disabled = true;

    try {
        if (eraEdicion) {
            // UPDATE: el id viaja en la URL, no en el cuerpo.
            await peticion(`${API_URL}/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(estudiante),
            });
        } else {
            // CREATE: el id se envía como entero.
            await peticion(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id, ...estudiante }),
            });
        }

        alert(eraEdicion
            ? 'Estudiante actualizado exitosamente.'
            : 'Estudiante creado exitosamente.');
        limpiarFormulario();
        await cargarEstudiantes();
    } catch (error) {
        console.error('Error al guardar estudiante:', error);
        alert('No fue posible guardar el estudiante:\n' + error.message);
    } finally {
        submitBtn.disabled = false;
    }
});

// Función para editar estudiante
async function editarEstudiante(id) {
    try {
        const respuesta = await peticion(`${API_URL}/${id}`);
        const estudiante = respuesta && respuesta.data ? respuesta.data : respuesta;

        idInput.value = estudiante.id;
        idInput.readOnly = true;
        document.getElementById('nombre').value = estudiante.nombre;
        document.getElementById('apellido').value = estudiante.apellido;
        document.getElementById('edad').value = estudiante.edad;
        document.getElementById('carrera').value = estudiante.carrera;

        EDITA = true;
        formTitle.textContent = 'Editar Estudiante';
        submitBtn.textContent = 'Actualizar Estudiante';
        cancelBtn.style.display = 'inline-block';

        form.scrollIntoView({ behavior: 'smooth' });
    } catch (error) {
        console.error('Error al cargar estudiante:', error);
        alert('No fue posible cargar los datos del estudiante:\n' + error.message);
    }
}

// Función para eliminar estudiante (DELETE)
async function eliminarEstudiante(id) {
    if (!confirm('¿Estás seguro de eliminar este estudiante?')) {
        return;
    }

    try {
        await peticion(`${API_URL}/${id}`, { method: 'DELETE' });
        alert('Estudiante eliminado exitosamente.');
        if (EDITA && parseInt(idInput.value, 10) === id) {
            limpiarFormulario();
        }
        await cargarEstudiantes();
    } catch (error) {
        console.error('Error al eliminar estudiante:', error);
        alert('No fue posible eliminar el estudiante:\n' + error.message);
    }
}

// Función para limpiar el formulario
function limpiarFormulario() {
    form.reset();
    EDITA = false;
    idInput.value = '';
    idInput.readOnly = false;
    formTitle.textContent = 'Agregar Nuevo Estudiante';
    submitBtn.textContent = 'Agregar Estudiante';
    cancelBtn.style.display = 'none';
}

// Botón cancelar
cancelBtn.addEventListener('click', limpiarFormulario);
