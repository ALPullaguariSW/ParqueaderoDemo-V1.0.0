// URL de nuestro backend. ¡Asegúrate de que el puerto 5000 coincida!
const API_URL = 'http://127.0.0.1:5000/api/status';

// Elementos del DOM
const parkingMap = document.getElementById('parking-map');
const summaryDiv = document.getElementById('summary');

// Función para obtener y mostrar los datos del parqueadero
async function actualizarEstadoParqueadero() {
    try {
        const response = await fetch(API_URL);
        if (!response.ok) {
            throw new Error(`Error de red: ${response.statusText}`);
        }
        const data = await response.json();

        // Limpiamos el mapa antes de volver a dibujar
        parkingMap.innerHTML = '';

        let espaciosLibres = 0;
        let totalEspacios = 0;

        // Ordenamos los espacios por nombre (E1, E2, E10, etc.)
        const sortedIds = Object.keys(data).sort((a, b) => {
            return parseInt(a.substring(1)) - parseInt(b.substring(1));
        });

        // Por cada espacio en los datos, creamos un elemento en la página
        for (const id of sortedIds) {
            const espacio = data[id];
            totalEspacios++;

            // Creamos el div para el espacio
            const spotDiv = document.createElement('div');
            spotDiv.id = id;
            spotDiv.className = 'parking-spot';
            spotDiv.classList.add(espacio.status); // Añade la clase 'libre' u 'ocupado'
            spotDiv.textContent = id; // Muestra el ID del espacio (E1, E2...)

            // Añadimos el div al mapa en el HTML
            parkingMap.appendChild(spotDiv);

            // Contamos los espacios libres
            if (espacio.status === 'libre') {
                espaciosLibres++;
            }

            // Simulación de pago
            if (espacio.status === 'ocupado') {
                spotDiv.onclick = () => {
                    alert(`Simulación de pago para el espacio ${id}.\n\nAquí iría la integración con una pasarela de pago.`);
                }
            }
        }
        
        // Actualizamos el resumen
        summaryDiv.textContent = `Disponibles: ${espaciosLibres} de ${totalEspacios}`;

    } catch (error) {
        console.error('No se pudo obtener el estado del parqueadero:', error);
        summaryDiv.textContent = 'Error al conectar con el servidor.';
    }
}

// --- BUCLE PRINCIPAL DEL FRONTEND ---
// Llamamos a la función una vez al inicio
actualizarEstadoParqueadero();

// Y luego la configuramos para que se repita cada 3 segundos (3000 milisegundos)
setInterval(actualizarEstadoParqueadero, 3000);