"""
Página web de Soluciones Empresariales El Monarca.

En producción se ejecuta con Gunicorn (ver Dockerfile), nunca con el servidor
de desarrollo de Flask. Para probar en tu equipo:
    python app.py              -> http://127.0.0.1:5000
"""
import json
import os
from pathlib import Path

from flask import Flask, render_template, request
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
# Render entrega las peticiones a través de un proxy: así Flask sabe que la página va por HTTPS
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

# Los archivos estáticos (CSS, imágenes) se guardan en caché del navegador 7 días.
# Si cambias una imagen o el CSS, sube el número de VERSION_ESTATICOS para forzar la recarga.
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 60 * 60 * 24 * 7
VERSION_ESTATICOS = "5"

# ==========================================
# DATOS DE LA EMPRESA (se repiten en toda la web)
# ==========================================
EMPRESA_INFO = {
    "nombre": "El Monarca Soluciones Empresariales",
    "ciudad": "Bogotá, Colombia",
    # Formulario de solicitud (Google Forms)
    "formulario": "https://forms.gle/pNUa2vyz7UVZYxSu7",
    # Cuando la herramienta digital esté publicada, pon aquí su dirección y aparecerá
    # el botón «Ingresar a la herramienta» en el menú. Vacío = no se muestra.
    "herramienta_url": os.getenv("HERRAMIENTA_URL", ""),
}

# Los cuatro programas que exige la Resolución 2674 de 2013 (imagen = nombre base en static/img)
PROGRAMAS = [
    {"nombre": "Limpieza y desinfección", "imagen": "limpieza", "evidencia": "Manual, cronograma anual y registro diario",
     "detalle": "Procedimientos por área, sustancias y diluciones, cronograma anual y registro diario."},
    {"nombre": "Control de plagas", "imagen": "plagas", "evidencia": "Proveedor con concepto sanitario e inspecciones",
     "detalle": "Metodos pasivos, métodos activos, proveedor certificado, inspecciones y cronograma."},
    {"nombre": "Gestión de residuos", "imagen": "residuos", "evidencia": "Separación en la fuente, ruta y gestores",
     "detalle": "Separación en la fuente por colores, acopio, ruta interna y gestores autorizados."},
    {"nombre": "Abastecimiento de agua potable", "imagen": "agua", "evidencia": "Registro de pH y cloro, limpieza del tanque",
     "detalle": "Control de pH y cloro, características del agua y limpieza del tanque."},
]

# Planes: cada uno incluye todo lo del anterior. "incluye" marca en qué planes aparece cada componente.
PLANES = [
    {"clave": "saneamiento", "titulo": "Plan de saneamiento básico", "imagen": "saneamiento",
     "resumen": "Lo que exige la norma para obtener y mantener el concepto sanitario favorable."},
    {"clave": "calidad", "titulo": "Saneamiento + gestión de calidad", "imagen": "calidad",
     "resumen": "Suma estándares para tus productos y la medición de lo que piensan tus clientes."},
    {"clave": "ambiental", "titulo": "Programa de saneamiento básico + Calidad + gestión ambiental", "imagen": "ambiental",
     "resumen": "Suma buenas prácticas ambientales y control de consumos de agua y energía."},
]
COMPONENTES = [
    ("Programa de limpieza y desinfección", 1),
    ("Programa de control de plagas", 1),
    ("Programa de gestión de residuos", 1),
    ("Programa de abastecimiento de agua potable", 1),
    ("Fichas técnicas y estandarización de productos", 2),
    ("Encuesta e informe de satisfacción del cliente", 2),
    ("Indicadores de gestión y tablero de seguimiento", 2),
    ("Pesaje y disminución de residuos", 3),
    ("Control de consumo de agua y energía", 3),
    ("Buenas prácticas ambientales", 3),
]


# Profesionales del equipo (página Conócenos). Se editan en datos/profesionales.json:
# una entrada por profesional; agregar o quitar personas no requiere tocar el código.
# Fotos: static/img/profesionales/<slug>-320.webp y <slug>-640.webp (scripts/preparar_foto.py).
# Si un profesional aún no tiene foto se muestran sus iniciales.
BASE = Path(__file__).resolve().parent
CARPETA_FOTOS = BASE / "static" / "img" / "profesionales"


def cargar_profesionales() -> list[dict]:
    datos = json.loads((BASE / "datos" / "profesionales.json").read_text(encoding="utf-8"))
    lista = []
    for p in datos.get("profesionales", []):
        if not p.get("nombre") or not p.get("slug"):
            continue
        p["hay_foto"] = (CARPETA_FOTOS / f"{p['slug']}-320.webp").exists()
        partes = p["nombre"].split()
        p["iniciales"] = (partes[0][0] + (partes[1][0] if len(partes) > 1 else "")).upper()
        lista.append(p)
    return lista


# ==========================================
# SEGURIDAD: cabeceras HTTP en todas las respuestas
# ==========================================
POLITICA_CONTENIDO = "; ".join([
    "default-src 'self'",
    "img-src 'self' data:",
    "style-src 'self' https://fonts.googleapis.com",
    "font-src https://fonts.gstatic.com",
    "script-src 'self'",
    "object-src 'none'",
    "base-uri 'self'",
    "form-action 'self'",
    "frame-ancestors 'none'",
])


@app.after_request
def cabeceras_seguridad(respuesta):
    https = request.scheme == "https"
    respuesta.headers["Content-Security-Policy"] = POLITICA_CONTENIDO + ("; upgrade-insecure-requests" if https else "")
    respuesta.headers["X-Content-Type-Options"] = "nosniff"
    respuesta.headers["X-Frame-Options"] = "DENY"
    respuesta.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    respuesta.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=(), payment=()"
    respuesta.headers["Cross-Origin-Opener-Policy"] = "same-origin"
    # HSTS solo cuando la página llega por HTTPS (Render pone X-Forwarded-Proto)
    if https:
        respuesta.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    respuesta.headers.pop("Server", None)
    return respuesta


@app.context_processor
def datos_globales():
    return {"empresa": EMPRESA_INFO, "v": VERSION_ESTATICOS}


# ==========================================
# PÁGINAS
# ==========================================
@app.route("/")
def inicio():
    return render_template("inicio.html", programas=PROGRAMAS, pagina="inicio")


@app.route("/servicios")
def servicios():
    return render_template("servicios.html", planes=PLANES, componentes=COMPONENTES, pagina="servicios")


@app.route("/conocenos")
def conocenos():
    return render_template("conocenos.html", profesionales=cargar_profesionales(), pagina="conocenos")


@app.errorhandler(404)
def no_encontrada(_error):
    return render_template("404.html", pagina=""), 404


# ==========================================
# SOLO PARA PROBAR EN TU EQUIPO
# ==========================================
if __name__ == "__main__":
    # El modo depuración solo se activa si lo pides: FLASK_DEBUG=1 python app.py
    # Nunca lo actives en Render: expone una consola que permite ejecutar código.
    app.run(host="127.0.0.1", port=5000, debug=os.getenv("FLASK_DEBUG") == "1")
