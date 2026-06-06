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
