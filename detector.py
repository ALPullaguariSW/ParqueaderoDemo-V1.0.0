import cv2
import numpy as np
import yaml
import requests
import time

# --- 1. CARGAR CONFIGURACIÓN Y POSICIONES ---
try:
    with open('config.yml', 'r') as file:
        config = yaml.safe_load(file)
except FileNotFoundError:
    print("Error: No se encontró 'config.yml'.")
    exit()

try:
    with open('posiciones.yml', 'r') as file:
        posiciones = yaml.safe_load(file)
except FileNotFoundError:
    print("Error: No se encontró 'posiciones.yml'. Ejecuta 'calibrador.py' primero.")
    exit()

VIDEO_SOURCE = config.get('video_source')
BACKEND_URL = config.get('backend_url')
UMBRAL_DETECCION = config.get('umbral_deteccion')
IMAGEN_CALIBRACION = config.get('imagen_calibracion') # Leemos el nombre de la imagen

# --- 2. OBTENER LA RESOLUCIÓN DE REFERENCIA (MODIFICADO) ---
ANCHO_PROCESADO = 800 # DEBE SER EL MISMO VALOR QUE EN EL CALIBRADOR

# Leemos la imagen original para calcular el ratio de aspecto
img_ref = cv2.imread(IMAGEN_CALIBRACION) 
if img_ref is None:
    exit()
ratio = ANCHO_PROCESADO / img_ref.shape[1]
alto_procesado = int(img_ref.shape[0] * ratio)

TAMAÑO_REFERENCIA = (ANCHO_PROCESADO, alto_procesado) # (ancho, alto)
print(f"OPTIMIZACIÓN: Detección se ejecutará a la resolución fija de: {TAMAÑO_REFERENCIA}")
# ----------------------------------------------------
estado_anterior = {}

def procesar_frame(frame, posiciones, umbral, backend_url): # Añadimos backend_url como argumento
    frame_procesado = frame.copy()
    
    for i, pos in enumerate(posiciones):
        id_espacio = f"E{i+1}"
        p1, p2 = tuple(pos[0]), tuple(pos[1])
        espacio_recortado = frame[p1[1]:p2[1], p1[0]:p2[0]]

        if espacio_recortado.shape[0] == 0 or espacio_recortado.shape[1] == 0:
            continue
        
        gray = cv2.cvtColor(espacio_recortado, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        count = cv2.countNonZero(thresh)
        
        estado_actual = "ocupado" if count > umbral else "libre"
        color = (0, 0, 255) if estado_actual == "ocupado" else (0, 255, 0)
        
        cv2.rectangle(frame_procesado, p1, p2, color, 2)
        cv2.putText(frame_procesado, id_espacio, (p1[0], p1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 1)

        # --- LÓGICA DE COMUNICACIÓN ACTIVA ---
        if id_espacio not in estado_anterior or estado_anterior[id_espacio] != estado_actual:
            estado_anterior[id_espacio] = estado_actual
            print(f"CAMBIO: {id_espacio} ahora está {estado_actual}. Notificando al backend...")
            try:
                payload = {'id_espacio': id_espacio, 'status': estado_actual}
                requests.post(backend_url, json=payload, timeout=1.5)
            except requests.exceptions.RequestException as e:
                print(f"-> ERROR de conexión con el backend: {e}")
        # ------------------------------------

    return frame_procesado
# --- BUCLE PRINCIPAL (MODIFICADO) ---
cap = cv2.VideoCapture(VIDEO_SOURCE)
if not cap.isOpened():
    print(f"Error: No se pudo conectar a la fuente de video: {VIDEO_SOURCE}")
    exit()

# En el bucle principal de detector.py

contador_frames = 0
while True:
    ret, frame = cap.read()
    if not ret:
        # ... lógica de reconexión
        continue

    contador_frames += 1
    # Solo procesamos 1 de cada 3 frames (aprox. 10 FPS si el video es de 30 FPS)
    if contador_frames % 3 != 0:
        continue

    # Redimensionamos
    frame = cv2.resize(frame, TAMAÑO_REFERENCIA)

    frame_resultado = procesar_frame(frame, posiciones, UMBRAL_DETECCION, config.get('backend_url'))
    cv2.imshow('Detector de Parqueadero', frame_resultado)

    if cv2.waitKey(1) & 0xFF == ord('q'): # Usamos waitKey(1) para una respuesta más fluida
        break

cap.release()
cv2.destroyAllWindows()