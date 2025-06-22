import os
from PIL import Image

# 1. Carpeta donde está este script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Construimos la ruta relativa
ruta_imagen = os.path.join(BASE_DIR, "imagenes", "ejemplo.png")

print("Ruta construida:", ruta_imagen)

# 3. Intentamos abrir la imagen
try:
    img = Image.open(ruta_imagen)
    print("La imagen se abrió correctamente.")
    img.show()  # Esto debería mostrar la imagen en tu visor de imágenes por defecto
except Exception as e:
    print("Error al abrir la imagen:", e)


