// Frontend V2: consume la API V2 (backendv2/app.py)
// Si ejecutas el backend V1, cambia la URL a http://localhost:5000/api/v1/estudiantes
const API_URL = 'http://localhost:5000/api/v2/estudiantes';

let EDITA = false;
let temporizadorNotificacion = null;

// Referencias al DOM
const form = document.getElementById('estudiante-form');
const formTitle = document.getElementById('form-title');
const submitBtn = document.getElementById('submit-btn');
const cancelBtn = document.getElementById('cancel-btn');
const tbody = document.getElementById('estudiantes-tbody');
const idInput = document.getElementById('estudiante-id');
const searchInput = document.getElementById('search');
const notificacionExito = document.getElementById('notificacion-exito');
const notificacionError = document.getElementById('notificacion-error');

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
            : `Error ${respuesta.status} while contacting the server`;
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

function mostrarNotificacion(tipo, mensaje) {
    clearTimeout(temporizadorNotificacion);

    const caja = tipo === 'error' ? notificacionError : notificacionExito;
    const otra = tipo === 'error' ? notificacionExito : notificacionError;

    otra.classList.add('hidden');
    caja.classList.remove('hidden');
    caja.querySelector('p').textContent = mensaje;

    temporizadorNotificacion = setTimeout(() => {
        caja.classList.add('hidden');
    }, 5000);
}

function establecerBoton(texto, icono) {
    submitBtn.innerHTML = `
        <span class="material-symbols-outlined">${icono}</span>
        ${texto}
    `;
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
                    <td class="px-6 py-8 text-center text-sm text-gray-500 dark:text-gray-400" colspan="6">
                        No students registered yet.
                    </td>
                </tr>
            `;
            return;
        }

        estudiantes.forEach(estudiante => {
            const tr = document.createElement('tr');
            const textoBusqueda = `${estudiante.nombre || ''} ${estudiante.apellido || ''} ${estudiante.carrera || ''}`
                .toLowerCase();

            tr.dataset.search = textoBusqueda;
            tr.innerHTML = `
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-500 dark:text-gray-400">${escaparHtml(estudiante.id)}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-500 dark:text-gray-400">${escaparHtml(estudiante.nombre)}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-semibold text-gray-900 dark:text-white">${escaparHtml(estudiante.apellido)}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">${escaparHtml(estudiante.edad)}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">${escaparHtml(estudiante.carrera)}</td>
                <td class="px-6 py-4 whitespace-nowrap text-center text-sm font-medium">
                    <button class="text-primary hover:text-primary/80 p-1" title="Edit" onclick="editarEstudiante(${Number(estudiante.id)})">
                        <span class="material-symbols-outlined text-base">edit</span>
                    </button>
                    <button class="text-red-600 dark:text-red-500 hover:text-red-800 dark:hover:text-red-400 p-1" title="Delete" onclick="eliminarEstudiante(${Number(estudiante.id)})">
                        <span class="material-symbols-outlined text-base">delete</span>
                    </button>
                </td>
            `;
            tbody.appendChild(tr);
        });

        aplicarBusqueda();
    } catch (error) {
        console.error('Error al cargar estudiantes:', error);
        tbody.innerHTML = `
            <tr>
                <td class="px-6 py-8 text-center text-sm text-red-600 dark:text-red-400" colspan="6">
                    ${escaparHtml(error.message)}
                </td>
            </tr>
        `;
        mostrarNotificacion('error', 'Could not load students: ' + error.message);
    }
}

// Función para crear o actualizar estudiante (CREATE/UPDATE)
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const id = parseInt(idInput.value, 10);
    if (!Number.isInteger(id) || id <= 0) {
        mostrarNotificacion('error', 'The id must be a positive integer.');
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
        mostrarNotificacion('error', 'Name, last name and major are required.');
        return;
    }
    if (!Number.isInteger(estudiante.edad)) {
        mostrarNotificacion('error', 'The age must be an integer.');
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

        mostrarNotificacion('success', eraEdicion
            ? 'Student updated successfully.'
            : 'Student added successfully.');

        limpiarFormulario();
        await cargarEstudiantes();
    } catch (error) {
        console.error('Error al guardar estudiante:', error);
        mostrarNotificacion('error', 'Could not save the student: ' + error.message);
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
        formTitle.textContent = 'Edit Student';
        establecerBoton('Update Student', 'edit');
        cancelBtn.style.display = 'flex';

        form.scrollIntoView({ behavior: 'smooth' });
    } catch (error) {
        console.error('Error al cargar estudiante:', error);
        mostrarNotificacion('error', 'Could not load the student: ' + error.message);
    }
}

// Función para eliminar estudiante (DELETE)
async function eliminarEstudiante(id) {
    if (!confirm('Are you sure you want to delete this student?')) {
        return;
    }

    try {
        await peticion(`${API_URL}/${id}`, { method: 'DELETE' });
        mostrarNotificacion('success', 'Student deleted successfully.');

        if (EDITA && parseInt(idInput.value, 10) === id) {
            limpiarFormulario();
        }
        await cargarEstudiantes();
    } catch (error) {
        console.error('Error al eliminar estudiante:', error);
        mostrarNotificacion('error', 'Could not delete the student: ' + error.message);
    }
}

// Función para limpiar el formulario
function limpiarFormulario() {
    form.reset();
    EDITA = false;
    idInput.value = '';
    idInput.readOnly = false;
    formTitle.textContent = 'Create New Student';
    establecerBoton('Add Student', 'add');
    cancelBtn.style.display = 'none';
}

// Filtro de la tabla por nombre, apellido o carrera
function aplicarBusqueda() {
    const termino = (searchInput.value || '').toLowerCase().trim();

    document.querySelectorAll('#estudiantes-tbody tr[data-search]').forEach(tr => {
        const coincide = tr.dataset.search.includes(termino);
        tr.style.display = coincide ? '' : 'none';
    });
}

searchInput.addEventListener('input', aplicarBusqueda);

// Botón cancelar
cancelBtn.addEventListener('click', limpiarFormulario);
