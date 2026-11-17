#!/usr/bin/env bash
# =============================================================================
# Página web en el servidor de Google.
#   sudo bash scripts/servidor/actualizar.sh   # la primera vez (deja instalado el comando corto)
#   sudo pagina-actualizar                     # las siguientes: trae de GitHub y reconstruye
# Requiere que la herramienta ya esté arriba con la red «monarca_compartida».
# =============================================================================
set -euo pipefail
[[ $EUID -eq 0 ]] || { echo "Ejecuta con sudo."; exit 1; }
CARPETA="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$CARPETA"
if ! docker network inspect monarca_compartida >/dev/null 2>&1; then
  echo "No existe la red monarca_compartida. Primero actualiza la herramienta: sudo monarca-actualizar"; exit 1
fi
cat > /usr/local/bin/pagina-actualizar <<ACT
#!/usr/bin/env bash
set -euo pipefail
[[ \$EUID -eq 0 ]] || { echo "Ejecuta con sudo: sudo pagina-actualizar"; exit 1; }
cd "$CARPETA"
if [[ -d .git ]]; then
  DUENO="\$(stat -c %U .)"
  echo "==> Trayendo la versión nueva de la página desde GitHub"
  sudo -u "\$DUENO" git pull --ff-only origin main
  sudo -u "\$DUENO" git log -1 --format='Versión: %h · %s · %cd' --date=format:'%Y-%m-%d %H:%M'
fi
exec bash scripts/servidor/actualizar.sh
ACT
chmod 755 /usr/local/bin/pagina-actualizar
echo "==> Reconstruyendo la página web"
docker compose -f docker-compose.prod.yml up -d --build
docker image prune -f >/dev/null 2>&1 || true
sleep 5
docker compose -f docker-compose.prod.yml ps
echo "Página actualizada."
