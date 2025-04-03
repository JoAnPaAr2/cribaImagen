import os
import shutil
import cv2
import numpy as np
from tkinter import filedialog, Tk

# 👉 Selección de carpeta al ejecutar
Tk().withdraw()
carpeta_origen = filedialog.askdirectory(title="Selecciona la carpeta con imágenes a clasificar")
if not carpeta_origen:
    print("No se seleccionó ninguna carpeta.")
    exit()

# Carpetas destino (se crean en la misma ruta)
carpeta_yay = os.path.join(carpeta_origen, "yay")
carpeta_nay = os.path.join(carpeta_origen, "nay")
os.makedirs(carpeta_yay, exist_ok=True)
os.makedirs(carpeta_nay, exist_ok=True)

# Detectar resolución de pantalla
screen_width = 1920
screen_height = 1080

try:
    import tkinter as tk
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()
except:
    pass

# Filtrar imágenes
imagenes = [f for f in os.listdir(carpeta_origen) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
total = len(imagenes)

if total == 0:
    print("No hay imágenes en la carpeta origen.")
    exit()

# Ventana única
ventana_nombre = "Clasificador de imágenes"
cv2.namedWindow(ventana_nombre, cv2.WINDOW_NORMAL)

# 📦 Función para mantener aspecto y centrar con bordes
def encajar_en_pantalla_con_bordes(img, max_w, max_h):
    h, w = img.shape[:2]
    scale = min(max_w / w, max_h / h, 1.0)
    new_w, new_h = int(w * scale), int(h * scale)
    resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

    # Crear lienzo negro
    canvas = np.zeros((max_h, max_w, 3), dtype=np.uint8)
    x_offset = (max_w - new_w) // 2
    y_offset = (max_h - new_h) // 2

    # Colocar la imagen centrada
    canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized
    return canvas

# Controles
print("Controles: 1 = yay | 2 = nay | Esc = saltar | 6 = salir")

for i, imagen in enumerate(imagenes, start=1):
    ruta_imagen = os.path.join(carpeta_origen, imagen)
    img = cv2.imread(ruta_imagen)

    if img is None:
        print(f"No se pudo cargar {imagen}")
        continue

    h, w = img.shape[:2]
    resolucion_original = f"{w}x{h}"

    # Aplicar el centrado con bordes
    imagen_final = encajar_en_pantalla_con_bordes(img, screen_width, screen_height)

    # Actualizar título
    titulo = f"{i}/{total} - Resolución: {resolucion_original} - 1:Yay | 2:Nay | Esc:Saltar | 6:Salir"
    cv2.setWindowTitle(ventana_nombre, titulo)
    cv2.imshow(ventana_nombre, imagen_final)

    while True:
        key = cv2.waitKey(0)
        if key == ord('1'):
            shutil.move(ruta_imagen, os.path.join(carpeta_yay, imagen))
            break
        elif key == ord('2'):
            shutil.move(ruta_imagen, os.path.join(carpeta_nay, imagen))
            break
        elif key == 27:  # ESC
            break
        elif key == ord('6'):
            cv2.destroyAllWindows()
            print("Programa cerrado por el usuario.")
            exit()

cv2.destroyAllWindows()
print("Clasificación finalizada.")