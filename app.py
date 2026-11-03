from flask import Flask, render_template

app = Flask(__name__)

# ==========================================
# CONFIGURACIÓN GENERAL DE LA EMPRESA
# ==========================================
# Puedes cambiar aquí los datos globales que se repiten en la web
EMPRESA_INFO = {
    "nombre": "El Monarca Soluciones Empresariales",
    "slogan": "Soluciones empresariales para tu negocio",
    "color_primario": "#0F4C5C",  # [PERSONALIZACIÓN] Cambia el color principal (Ej. Azul oscuro)
    "color_secundario": "#F28C28" # [PERSONALIZACIÓN] Cambia el color de acento (Ej. Azul claro)
}

# ==========================================
# RUTAS / PESTAÑAS DE LA WEB
# ==========================================

@app.route('/')
def inicio():
    """Ruta para la página de Inicio (Pestaña 1)"""
    return render_template('inicio.html', empresa=EMPRESA_INFO)

@app.route('/servicios')
def servicios():
    """Ruta para la página de Servicios (Pestaña 2)
       [PERSONALIZACIÓN] Puedes agregar más rutas aquí si necesitas 'Contacto', 'Nosotros', etc.
    """
    # Lista de servicios de ejemplo que puedes modificar fácilmente
    lista_servicios = [
        {
            "titulo": "Plan de Saneamiento Básico", 
            "descripcion": "Incluye manual de limpieza y desinfección, gestión de residuos, control de plagas y control de abastecimiento de agua potable."
        },
        {
            "titulo": "Gestión de Calidad", 
            "descripcion": "Incluye plan de saneamiento básico, criterios de calidad de productos y fichas técnicas."
        },
        {
            "titulo": "Gestión Calidad y Ambiental", 
            "descripcion": "Incluye plan de saneamiento básico, gestión de calidad, análisis de aspectos e impactos ambientales y buenas prácticas ambientales."
        }
    ]
    return render_template('servicios.html', empresa=EMPRESA_INFO, servicios=lista_servicios)

# ==========================================
# EJECUCIÓN DE LA APLICACIÓN
# ==========================================
if __name__ == '__main__':
    # host='0.0.0.0' permite que Docker exponga la app correctamente
    app.run(host='0.0.0.0', port=5000, debug=True)
