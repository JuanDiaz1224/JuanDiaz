#!/bin/bash
DB_FILE="database.db"
BACKUP_DIR="backups"
RETENTION_DAYS=7
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_FILE="backup_${TIMESTAMP}.tar.gz"

log() { echo "[$(date +"%H:%M:%S")] $1"; }

log "Iniciando backup de FinTech Nova..."
if [ ! -f "$DB_FILE" ]; then
    log "ERROR: No se encontró $DB_FILE. Abortando."
    exit 1
fi
DB_SIZE=$(du -sh "$DB_FILE" | cut -f1)
log "Archivo encontrado: $DB_FILE ($DB_SIZE)"

if [ ! -d "$BACKUP_DIR" ]; then
    mkdir -p "$BACKUP_DIR"
fi

tar -czf "$BACKUP_DIR/$BACKUP_FILE" "$DB_FILE"
if [ $? -eq 0 ]; then
    log "OK: Backup creado exitosamente"
else
    log "ERROR: Falló la creación del backup."
    exit 1
fi

find "$BACKUP_DIR" -name "*.tar.gz" -mtime "+$RETENTION_DAYS" -delete
log "Proceso de backup finalizado correctamente."
exit 0
