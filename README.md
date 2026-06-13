# FinTech Nova — Motor de Riesgo Crediticio
> API de evaluacion de creditos — Roslaysoft Consulting

## Integrantes del Grupo
| Nombre | GitHub User | Rol |
|--------|-------------|-----|
| Juan Diaz | @JuanDiaz1224 | Coordinador |

## Laboratorio 1 — Estado: COMPLETADO
### URL del Codespace
https://cautious-space-funicular-wvrgqp7w5x6gc945-8000.app.github.dev/A
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
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```


---

## Laboratorio 2 — Estado: COMPLETADO

### Objetivo
Demostrar hardening de API mediante cabeceras de seguridad HTTP y prevencion de SQL Injection usando consultas parametrizadas.

### URL del Codespace
https://cautious-space-funicular-wvrgqp7w5x6gc945-8000.app.github.dev

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
uvicorn main:app --host 0.0.0.0 --port 8000
