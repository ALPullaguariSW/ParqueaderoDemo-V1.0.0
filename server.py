
# server.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime

# 1. INICIALIZACIÓN
app = Flask(__name__)
CORS(app) # Permite que nuestra app web (en otro "dominio") se comunique con este servidor

# 2. "BASE DE DATOS" EN MEMORIA
# Guardaremos no solo el estado, sino también la hora del último cambio.
# Ejemplo: estado_parqueaderos = {"E1": {"status": "ocupado", "timestamp": "2023-10-27 10:30:00"}}
estado_parqueaderos = {}

# --- RUTAS DE LA API ---

@app.route('/api/status', methods=['GET'])
def get_status():
    """Endpoint para que la app del usuario obtenga el estado de todos los parqueaderos."""
    print(f"[{datetime.datetime.now()}] Petición GET a /api/status recibida.")
    return jsonify(estado_parqueaderos)

@app.route('/api/update_status', methods=['POST'])
def update_status():
    """Endpoint para que el script de visión (detector.py) actualice un estado."""
    data = request.get_json()
    if not data or 'id_espacio' not in data or 'status' not in data:
        return jsonify({"error": "Datos inválidos"}), 400

    id_espacio = data['id_espacio']
    status = data['status']
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Actualizamos la información para ese espacio
    estado_parqueaderos[id_espacio] = {
        "status": status,
        "timestamp": timestamp
    }
    
    print(f"[{timestamp}] Petición POST: Espacio '{id_espacio}' actualizado a '{status}'.")
    return jsonify({"message": "Estado actualizado"}), 200

# --- PUNTO DE ENTRADA ---
if __name__ == '__main__':
    print("Iniciando servidor de Parqueadero...")
    # host='0.0.0.0' lo hace accesible desde otros dispositivos en la red
    app.run(host='0.0.0.0', port=5000, debug=False) # debug=False para un mejor rendimiento