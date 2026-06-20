# FinTech Nova — Motor de Riesgo Crediticio
> API de evaluacion de creditos — Roslaysoft Consulting

## Integrantes del Grupo
| Nombre | GitHub User | Rol |
|--------|-------------|-----|
| Juan Diaz | @JuanDiaz1224 | Coordinador |

## Laboratorio 1 — Estado: COMPLETADO
### URL del Codespace
https://cautious-space-funicular-wvrgqp7w5x6gc945-8001.app.github.dev/A
### Endpoints disponibles
| Endpoint | Metodo | Descripcion |
|----------|--------|-------------|
| /status | GET | Health check del sistema |
| /evaluar-riesgo | POST | Motor de scoring crediticio |
| /datos-financieros/{id} | GET | Historial (VULNERABLE - Lab 2) |

### Diagrama Arquitectonico As-Is
![Arquitectura As-Is Lab 1](docs/diagramas/arquitectura_as_is_lab1.png)

## Como ejecutar
```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```


---

## Laboratorio 2 — Estado: COMPLETADO

### Objetivo
Demostrar hardening de API mediante cabeceras de seguridad HTTP y prevencion de SQL Injection usando consultas parametrizadas.

### URL del Codespace
https://cautious-space-funicular-wvrgqp7w5x6gc945-8001.app.github.dev

### Endpoints disponibles

| Endpoint | Metodo | Descripcion |
|----------|--------|-------------|
| /vulnerable/users/{username} | GET | Endpoint vulnerable a SQLi |
| /secure/users/{username} | GET | Endpoint protegido con prepared statements |

### Hallazgos de Seguridad

#### Hallazgo 1 - SQL Injection (A03:2021)
- Endpoint afectado: /vulnerable/users/{username}
- Payload usado: juan OR 1=1
- Impacto: Expuso todos los usuarios incluyendo admin/superadmin
- Remediacion: Endpoint /secure/ con consultas parametrizadas neutraliza el ataque

#### Hallazgo 2 - Cabeceras de Seguridad HTTP
- Cabeceras implementadas: X-Content-Type-Options, X-Frame-Options, X-XSS-Protection, Strict-Transport-Security, Content-Security-Policy
- Verificacion: securityheaders.com - Calificacion C (limitacion del proxy de Codespaces)

### Como ejecutar
cd lab2-hardening-sqli
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8001

---
## Laboratorio 3 — Estado: COMPLETADO
### Objetivo
Implementar automatización completa con scripts Bash y Python, observabilidad mediante health checks, y empaquetado seguro con Docker para la API FinTech Nova.

### Archivos entregados
| Archivo | Bloque | Descripción |
|---------|--------|-------------|
| backup_db.sh | Bloque 1 | Script Bash de backup automático con retención 7 días |
| log_analyzer.py | Bloque 1 | Detector de SQL Injection en logs con regex |
| resource_monitor.sh | Ejercicio 1 | Monitor de CPU/RAM/disco con alertas |
| health_check.py | Bloque 2 | Verificaciones de BD, disco, backup y RAM |
| main.py | Bloque 2 | API FastAPI con endpoint /health integrado |
| Dockerfile | Bloque 3 | Imagen de producción con usuario no-root |
| deploy.sh | Ejercicio 6 | Script de despliegue automatizado |
| docker-compose.yml | Ejercicio 7 | Orquestación API + Redis |
| README_LAB3.md | Ejercicio 8 | Documentación completa del stack |

### Endpoints disponibles
| Endpoint | Metodo | Descripcion |
|----------|--------|-------------|
| /status | GET | Estado de la API |
| /evaluar-riesgo | POST | Motor de scoring crediticio |
| /health | GET | Health check con BD, disco, backup y RAM |

### Como ejecutar
```bash
cd lab3-automatizacion-docker
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Como ejecutar con Docker
```bash
cd lab3-automatizacion-docker
docker build -t fintech-nova:1.0 .
docker run -d -p 8000:8000 --name fintech-api fintech-nova:1.0
curl -s http://localhost:8000/health | python3 -m json.tool
```

### Conceptos implementados
| Concepto | Implementación |
|----------|----------------|
| Toil | Eliminado con backup_db.sh y log_analyzer.py |
| Golden Signals | Latencia y saturación en health_check.py |
| RPO/RTO | RPO=24h con backup diario via cron |
| Minimo Privilegio | Usuario no-root en Dockerfile |
| IaC declarativo | docker-compose.yml versionado en Git |
