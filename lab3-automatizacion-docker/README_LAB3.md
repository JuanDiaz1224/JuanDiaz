# Sesión 13 — Laboratorio 3
## Automatización, Observabilidad y Contenedores
### Proyecto FinTech Nova

---

## Integrantes del Grupo

| Nombre    | GitHub User   | Rol         |
|-----------|---------------|-------------|
| Juan Diaz | @JuanDiaz1224 | Coordinador |

---

## Laboratorio 3 — Estado: COMPLETADO

### Archivos entregados

| Archivo                    | Bloque   | Descripción                                |
|----------------------------|----------|--------------------------------------------|
| backup_db.sh               | Bloque 1 | Script Bash de backup automático           |
| log_analyzer.py            | Bloque 1 | Detector de SQL Injection en logs          |
| resource_monitor.sh        | Ej. 1    | Monitor de CPU/RAM/disco con alertas       |
| health_check.py            | Bloque 2 | Verificaciones de BD, disco, backup y RAM  |
| main.py                    | Bloque 2 | API FastAPI con endpoint /health integrado |
| Dockerfile                 | Bloque 3 | Imagen de producción con usuario no-root   |
| deploy.sh                  | Ej. 6    | Script de despliegue automatizado          |
| docker-compose.yml         | Ej. 7    | Orquestación API + Redis                   |

---

## 1. PREREQUISITOS

```bash
git    --version   # >= 2.x
docker --version   # >= 24.x
python3 --version  # >= 3.11
```

## 2. CONFIGURACIÓN INICIAL

```bash
git clone https://github.com/JuanDiaz1224/JuanDiaz.git
cd JuanDiaz/lab3-automatizacion-docker
chmod +x backup_db.sh deploy.sh
docker build -t fintech-nova:1.0 .
```

## 3. EJECUCIÓN

```bash
# Iniciar contenedor
docker run -d -p 8000:8000 --name fintech-api fintech-nova:1.0

# Verificar que corre
docker ps

# Consultar health check
curl -s http://localhost:8000/health | python3 -m json.tool
```

## 4. AUTOMATIZACIÓN

```bash
# Backup manual
./backup_db.sh

# Configurar cron (backup diario a las 2AM)
crontab -e
# Agregar: 0 2 * * * /workspaces/JuanDiaz/lab3-automatizacion-docker/backup_db.sh

# Analizar logs
python3 log_analyzer.py server.log

# Monitorear recursos
./resource_monitor.sh
```

## 5. SOLUCIÓN DE PROBLEMAS

| Error | Solución |
|-------|----------|
| port is already allocated | Detén la API local o usa -p 9000:8000 |
| ModuleNotFoundError | Ejecuta pip install -r requirements.txt y reconstruye |
| health check unhealthy | Ejecuta docker logs fintech-api para ver el error |
