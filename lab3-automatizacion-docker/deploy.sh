#!/bin/bash
VERSION=$(date +%Y%m%d)
IMAGE_NAME="fintech-nova"
CONTAINER_NAME="fintech-api"
PORT=8000

log() { echo "[$(date +"%H:%M:%S")] $1"; }

log "=== Iniciando despliegue de FinTech Nova v${VERSION} ==="

if ! docker --version &>/dev/null; then
    log "ERROR: Docker no está instalado."
    exit 1
fi
log "OK: $(docker --version)"

if [ ! -f "requirements.txt" ]; then
    log "ERROR: No se encontró requirements.txt"
    exit 1
fi
log "OK: requirements.txt encontrado"

log "Construyendo imagen ${IMAGE_NAME}:${VERSION}..."
docker build -t "${IMAGE_NAME}:${VERSION}" .
if [ $? -ne 0 ]; then
    log "ERROR: Falló la construcción de la imagen."
    exit 1
fi
log "OK: Imagen construida exitosamente"

if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    log "Deteniendo contenedor anterior..."
    docker stop "${CONTAINER_NAME}" &>/dev/null
    docker rm   "${CONTAINER_NAME}" &>/dev/null
    log "OK: Contenedor anterior eliminado"
fi

log "Iniciando nuevo contenedor en puerto ${PORT}..."
docker run -d -p "${PORT}:${PORT}" --name "${CONTAINER_NAME}" "${IMAGE_NAME}:${VERSION}"
if [ $? -ne 0 ]; then
    log "ERROR: Falló el inicio del contenedor."
    exit 1
fi

log "Esperando 10 segundos para que la API inicie..."
sleep 10

STATUS=$(curl -s "http://localhost:${PORT}/health" | python3 -c \
    "import sys,json; print(json.load(sys.stdin).get('status','unknown'))" 2>/dev/null)

if [ "$STATUS" = "healthy" ] || [ "$STATUS" = "degraded" ]; then
    log "==========================================="
    log "  Despliegue exitoso! Estado: ${STATUS}"
    log "  API en http://localhost:${PORT}"
    log "==========================================="
else
    log "ERROR: El despliegue falló. Revisa: docker logs ${CONTAINER_NAME}"
    exit 1
fi
