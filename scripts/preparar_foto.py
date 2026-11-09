"""
Prepara la foto de un profesional para la página Conócenos.

Uso (desde la carpeta de la página):
    pip install pillow
    python scripts/preparar_foto.py "ruta/a/la/foto.jpg" maria-perez

Recorta la foto en formato vertical 4:5 (desde arriba, para conservar el rostro)
y crea static/img/profesionales/maria-perez-320.webp y -640.webp.
El segundo argumento debe ser igual al "slug" del profesional en datos/profesionales.json.
"""
import sys
from pathlib import Path

from PIL import Image, ImageOps

if len(sys.argv) != 3:
    sys.exit(__doc__)

origen, slug = sys.argv[1], sys.argv[2]
destino = Path(__file__).resolve().parent.parent / "static" / "img" / "profesionales"
destino.mkdir(parents=True, exist_ok=True)

im = ImageOps.exif_transpose(Image.open(origen)).convert("RGB")
ancho, alto = im.size
alto_4_5 = round(ancho * 5 / 4)
if alto_4_5 <= alto:
    im = im.crop((0, 0, ancho, alto_4_5))            # foto alta: se recorta abajo
else:
    ancho_4_5 = round(alto * 4 / 5)                  # foto ancha: se recorta a los lados
    x = (ancho - ancho_4_5) // 2
    im = im.crop((x, 0, x + ancho_4_5, alto))
for t in (320, 640):
    im.resize((t, round(t * 5 / 4)), Image.LANCZOS).save(destino / f"{slug}-{t}.webp", "WEBP", quality=80, method=6)
    print("Creada:", destino / f"{slug}-{t}.webp")
