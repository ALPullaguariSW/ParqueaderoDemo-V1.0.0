# calibrador.py (Versión para calibrar con una imagen estática - Restaurado)

import cv2
import yaml

print("--- INICIANDO CALIBRADOR DE ESPACIOS (IMAGEN FIJA) ---")

# --- 1. CARGAR CONFIGURACIÓN ---
try:
    with open('config.yml', 'r') as file:
        config = yaml.safe_load(file)
    print("Archivo 'config.yml' cargado correctamente.")
except FileNotFoundError:
    print("\nERROR: No se encontró 'config.yml'.")
    exit()

NOMBRE_IMAGEN = config.get('imagen_calibracion')
if not NOMBRE_IMAGEN:
    print("\nERROR: La clave 'imagen_calibracion' no se encontró en 'config.yml'.")
    exit()

NOMBRE_ARCHIVO_POS = 'posiciones.yml'

# --- 2. VARIABLES Y FUNCIONES ---
puntos_temporales = []
posiciones_guardadas = []

def manejador_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        puntos_temporales.append([x, y])
    if event == cv2.EVENT_RBUTTONDOWN and puntos_temporales:
        puntos_temporales.pop()

# --- 3. CARGAR DATOS Y LA IMAGEN ---
try:
    with open(NOMBRE_ARCHIVO_POS, 'r') as file:
        posiciones_guardadas = yaml.safe_load(file) or []
except FileNotFoundError:
    print(f"No se encontró '{NOMBRE_ARCHIVO_POS}'. Se creará uno nuevo.")

frame_original = cv2.imread(NOMBRE_IMAGEN)
if frame_original is None:
    print(f"\nERROR: No se pudo cargar la imagen '{NOMBRE_IMAGEN}'.")
    exit()

# --- LÍNEA DE OPTIMIZACIÓN AÑADIDA ---
# Redimensionamos la imagen a un tamaño fijo y manejable
ANCHO_PROCESADO = 800 # Puedes probar con 640
ratio = ANCHO_PROCESADO / frame_original.shape[1]
alto_procesado = int(frame_original.shape[0] * ratio)
TAMAÑO_MANEJABLE = (ANCHO_PROCESADO, alto_procesado)

frame_original = cv2.resize(frame_original, TAMAÑO_MANEJABLE)
# ------------------------------------
# --- 4. BUCLE PRINCIPAL DE CALIBRACIÓN ---
cv2.namedWindow('Calibrador de Imagen - Presiona Q para salir')
cv2.setMouseCallback('Calibrador de Imagen - Presiona Q para salir', manejador_mouse)

while True:
    frame_para_dibujar = frame_original.copy()
    
    # Dibujar las posiciones ya guardadas, puntos y rectángulos temporales...
    for i, pos in enumerate(posiciones_guardadas):
        cv2.rectangle(frame_para_dibujar, tuple(pos[0]), tuple(pos[1]), (255, 100, 0), 2)
    for punto in puntos_temporales:
        cv2.circle(frame_para_dibujar, tuple(punto), 7, (0, 255, 255), -1)
    if len(puntos_temporales) == 2:
        cv2.rectangle(frame_para_dibujar, tuple(puntos_temporales[0]), tuple(puntos_temporales[1]), (0, 255, 0), 2)

    cv2.imshow('Calibrador de Imagen - Presiona Q para salir', frame_para_dibujar)
    
    key = cv2.waitKey(20) & 0xFF

    if key == ord('q'): break
    if key == ord('s'):
        if len(puntos_temporales) == 2:
            p1_raw, p2_raw = puntos_temporales
            p1 = [min(p1_raw[0], p2_raw[0]), min(p1_raw[1], p2_raw[1])]
            p2 = [max(p1_raw[0], p2_raw[0]), max(p1_raw[1], p2_raw[1])]
            posiciones_guardadas.append([p1, p2])
            puntos_temporales = []
    if key == ord('d'):
        puntos_temporales = []

with open(NOMBRE_ARCHIVO_POS, 'w') as file:
    yaml.dump(posiciones_guardadas, file)

print(f"\nCalibración finalizada.")
cv2.destroyAllWindows()