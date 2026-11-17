# Página web El Monarca: servidor de producción (Gunicorn), sin modo depuración
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY datos ./datos
COPY templates ./templates
COPY static ./static

# Se ejecuta con un usuario sin privilegios
RUN useradd --create-home web
USER web

EXPOSE 5000
# PORT: puerto (5000 por defecto). WEB_WORKERS: procesos de Gunicorn (en el servidor de Google se usa 1 para cuidar la memoria)
CMD ["sh", "-c", "gunicorn app:app --bind 0.0.0.0:${PORT:-5000} --workers ${WEB_WORKERS:-2} --access-logfile -"]
