#!/bin/bash
MEMORY_THRESHOLD=80
DISK_THRESHOLD=85

log() { echo "[$(date +"%H:%M:%S")] $1"; }

log "=== Monitor de Recursos — FinTech Nova ==="

MEMORY_USED=$(free | grep Mem | awk '{print int($3/$2 * 100)}')
log "Memoria RAM en uso: ${MEMORY_USED}%"
if [ "$MEMORY_USED" -ge "$MEMORY_THRESHOLD" ]; then
    log "WARNING: RAM supera el umbral (${MEMORY_USED}% >= ${MEMORY_THRESHOLD}%)"
else
    log "OK: RAM dentro del limite (${MEMORY_USED}% < ${MEMORY_THRESHOLD}%)"
fi

DISK_USED=$(df -h . | tail -1 | awk '{print $5}' | tr -d '%')
log "Disco en uso: ${DISK_USED}%"
if [ "$DISK_USED" -ge "$DISK_THRESHOLD" ]; then
    log "WARNING: Disco supera el umbral (${DISK_USED}% >= ${DISK_THRESHOLD}%)"
else
    log "OK: Disco dentro del limite (${DISK_USED}% < ${DISK_THRESHOLD}%)"
fi

log "RESUMEN: RAM=${MEMORY_USED}% | DISCO=${DISK_USED}%"
