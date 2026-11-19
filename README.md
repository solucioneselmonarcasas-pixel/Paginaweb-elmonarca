# Paginaweb-elmonarca
Página web de Soluciones Empresariales El Monarca (Flask).

## Probar en tu equipo
```
pip install -r requirements.txt
python app.py            # http://127.0.0.1:5000
```

## Publicar (servidor de Google, el mismo de la herramienta HT)
Desde el 16 nov 2026 la página corre en el servidor de Google Cloud de la herramienta, en `~/paginaweb`,
con `docker-compose.prod.yml` (Gunicorn con 1 proceso, sin modo depuración, usuario sin privilegios).
La publica el Caddy de la herramienta con HTTPS automático y su propio subdominio de DuckDNS (variable
`DOMINIO_WEB` del `.env` de la herramienta). Instalación paso a paso: `DESPLIEGUE.md` de la herramienta, paso 8.

Cada cambio: `git add .`, `git commit -m "…"`, `git push` y en el servidor `sudo pagina-actualizar`.

Variable opcional (archivo `.env` de `~/paginaweb`, no va a GitHub):
- `HERRAMIENTA_URL`: dirección de la herramienta digital; si existe, aparece
  «Ingresar a la herramienta» en el menú.

**Render** (https://paginaweb-elmonarca.onrender.com) queda solo para redirigir la dirección anterior:
tiene la variable `REDIRIGIR_A` con la dirección nueva y envía cada visita a la misma página allá.
En el servidor de Google esa variable no se define.

## Dónde cambiar qué
- `app.py`: textos de programas, planes y la tabla comparativa; enlace del formulario.
- `app.py` → `EMPRESA_INFO`: número de WhatsApp (`whatsapp`, solo dígitos con el 57), cómo se muestra
  (`whatsapp_visible`) y el mensaje que aparece escrito al abrir el chat (`whatsapp_mensaje`).
  El botón «Escríbenos» queda fijo abajo a la derecha en todas las páginas y el número también sale en el pie.
  Logo de WhatsApp: descargar el oficial de https://www.meta.com/brand/resources/whatsapp/whatsapp-brand/ y
  guardarlo sin modificar como `static/img/whatsapp.svg` (o `.png`); el botón lo usa solo. Sin ese archivo, muestra una burbuja de chat.
- `app.py` → `VIDEO_HERRAMIENTA_YOUTUBE`: enlace del video de la herramienta en YouTube (sección «La herramienta en acción» de Inicio).
  YouTube se carga solo cuando la persona toca reproducir (`static/js/video.js`, dominio youtube-nocookie.com, permitido en la CSP con `frame-src`).
  Vacío = se muestra la pantalla de la herramienta sin botón de reproducir. `FUNCIONES`: las cuatro tarjetas de esa sección.
- `templates/`: estructura de las páginas.
- `templates/politica.html`: política de tratamiento de datos personales (`/politica-de-datos`, enlazada en el pie). Su texto viene del Word «Contrato empresas/2026-11-17 Politica de tratamiento de datos personales.docx»: si la política cambia, se cambia primero el Word y luego esta página, con nueva versión y fecha.
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
