# Paginaweb-elmonarca
Página web de Soluciones Empresariales El Monarca (Flask).

## Probar en tu equipo
```
pip install -r requirements.txt
python app.py            # http://127.0.0.1:5000
```

## Publicar (Render con Docker)
El `Dockerfile` arranca la página con Gunicorn, sin modo depuración y con un
usuario sin privilegios. Render asigna el puerto en la variable `PORT`.

Variable opcional en Render → Environment:
- `HERRAMIENTA_URL`: dirección de la herramienta digital; si existe, aparece
  «Ingresar a la herramienta» en el menú.

## Dónde cambiar qué
- `app.py`: textos de programas, planes y la tabla comparativa; enlace del formulario.
- `app.py` → `EMPRESA_INFO`: número de WhatsApp (`whatsapp`, solo dígitos con el 57), cómo se muestra
  (`whatsapp_visible`) y el mensaje que aparece escrito al abrir el chat (`whatsapp_mensaje`).
  El botón «Escríbenos» queda fijo abajo a la derecha en todas las páginas y el número también sale en el pie.
- `templates/`: estructura de las páginas.
- `static/css/estilos.css`: colores (manual de marca), tipografía y diseño.
- `static/img/`: imágenes en WebP (versión pequeña y grande de cada una).
  Para cambiar una imagen, genera las dos versiones y sube `VERSION_ESTATICOS` en `app.py`.
- `datos/profesionales.json`: equipo de la página Conócenos. Una entrada por profesional
  (nombre, cargo, resumen corto, resumen, experiencia, formación, LinkedIn); el orden de la
  lista es el de la página. Para la foto: `python scripts/preparar_foto.py foto.jpg <slug>`.
- `originales/`: imágenes PNG originales (no se publican).

## Seguridad incluida
Gunicorn en producción (sin consola de depuración), cabeceras CSP,
X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy
y HSTS en HTTPS, enlaces externos con `rel="noopener noreferrer"`,
Flask 3.1.3 (corrige CVE-2026-27205).
