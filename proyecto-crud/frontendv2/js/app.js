const API_URL = 'http://localhost:5000/api/v1/estudiantes';
let EDITA = false;

// Referencias al DOM
const form = document.getElementById('estudiante-form');
const formTitle = document.getElementById('form-title');
const submitBtn = document.getElementById('submit-btn');
const cancelBtn = document.getElementById('cancel-btn');
const tbody = document.getElementById('estudiantes-tbody');

// Cargar estudiantes al iniciar
document.addEventListener('DOMContentLoaded', () => {
    cargarEstudiantes();
});

// Función para cargar todos los estudiantes (READ)
async function cargarEstudiantes() {
    try {
        const response = await fetch(API_URL);
        const estudiantes = await response.json();
        
        tbody.innerHTML = '';
        
        estudiantes.forEach(estudiante => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
				<td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-500 dark:text-gray-400">${estudiante.id}</td>
				<td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-500 dark:text-gray-400">${estudiante.nombre}</td>
				<td class="px-6 py-4 whitespace-nowrap text-sm font-semibold text-gray-900 dark:text-white">${estudiante.apellido}</td>
				<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">${estudiante.edad}</td>
				<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">${estudiante.carrera}</td>
				<td class="px-6 py-4 whitespace-nowrap text-center text-sm font-medium">
					<button class="text-primary hover:text-primary/80 p-1" onclick="editarEstudiante(${estudiante.id})">
					<span class="material-symbols-outlined text-base">edit</span>
					</button>
					<button class=" text-red-600 dark:text-red-500 hover:text-red-800 dark:hover:text-red-400 p-1" onclick="eliminarEstudiante(${estudiante.id})">
					<span class="material-symbols-outlined text-base">delete</span>
					</button>
				</td>
            `;
            tbody.appendChild(tr);
        });
    } catch (error) {
        console.error('Error al cargar estudiantes:', error);
        alert('Error al cargar los datos del servidor');
    }
}

// Función para crear o actualizar estudiante (CREATE/UPDATE)
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const id = document.getElementById('estudiante-id').value;
    const estudiante = {
		id : document.getElementById('estudiante-id').value,
        nombre: document.getElementById('nombre').value,
        apellido: document.getElementById('apellido').value,
        edad: parseInt(document.getElementById('edad').value),
        carrera: document.getElementById('carrera').value
    };
    
    try {
        let response;
        
        if (EDITA) {
            // UPDATE
            response = await fetch(`${API_URL}/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(estudiante)
            });
            EDITA = false;
        } else {
            // CREATE
            response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(estudiante)
            });
        }
        
        if (response.ok) {
            alert(id ? 'Estudiante actualizado exitosamente' : 'Estudiante creado exitosamente');
            limpiarFormulario();
            cargarEstudiantes();
        } else {
            alert('Error al guardar el estudiante');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error de conexión con el servidor');
    }
});

// Función para editar estudiante
async function editarEstudiante(id) {
    EDITA = true;
    try {
        const response = await fetch(`${API_URL}/${id}`);
        const estudiante = await response.json();
		console.log(estudiante);
        
        document.getElementById('estudiante-id').value = estudiante.id;
        document.getElementById('nombre').value = estudiante.nombre;
        document.getElementById('apellido').value = estudiante.apellido;
        document.getElementById('edad').value = estudiante.edad;
        document.getElementById('carrera').value = estudiante.carrera;
        
        formTitle.textContent = 'Editar Estudiante';
        submitBtn.textContent = 'Actualizar Estudiante';
        cancelBtn.style.display = 'block';
        
        // Scroll al formulario
        form.scrollIntoView({ behavior: 'smooth' });
    } catch (error) {
        console.error('Error al cargar estudiante:', error);
        alert('Error al cargar los datos del estudiante');
    }
}

// Función para eliminar estudiante (DELETE)
async function eliminarEstudiante(id) {
    if (!confirm('¿Estás seguro de eliminar este estudiante?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            alert('Estudiante eliminado exitosamente');
            cargarEstudiantes();
        } else {
            alert('Error al eliminar el estudiante');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error de conexión con el servidor');
    }
}

// Función para limpiar el formulario
function limpiarFormulario() {
    form.reset();
    document.getElementById('estudiante-id').value = '';
    formTitle.textContent = 'Agregar Nuevo Estudiante';
    submitBtn.textContent = 'Agregar Estudiante';
    cancelBtn.style.display = 'none';
}

// Botón cancelar
cancelBtn.addEventListener('click', limpiarFormulario);