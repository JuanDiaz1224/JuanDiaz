from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from health_check import run_all_checks
import sqlite3, os

app = FastAPI(title="FinTech Nova", description="API de evaluacion crediticia con health checks")
DB_PATH = "database.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""CREATE TABLE IF NOT EXISTS solicitudes (
        id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, ingresos REAL,
        deudas REAL, score REAL, resultado TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)""")
    conn.commit(); conn.close()

init_db()

class Solicitud(BaseModel):
    nombre: str
    ingresos: float
    deudas: float

@app.get("/status")
def status(): return {"status": "ok", "service": "FinTech Nova", "version": "1.0.0"}

@app.post("/evaluar-riesgo")
def evaluar(s: Solicitud):
    if s.ingresos <= 0: raise HTTPException(400, "Ingresos deben ser > 0")
    ratio = s.deudas / s.ingresos
    score, resultado = (850, "APROBADO - Riesgo bajo") if ratio < 0.3 else \
                       (650, "APROBADO - Riesgo medio") if ratio < 0.5 else \
                       (400, "RECHAZADO - Riesgo alto")
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO solicitudes (nombre,ingresos,deudas,score,resultado) VALUES (?,?,?,?,?)",
                 (s.nombre, s.ingresos, s.deudas, score, resultado))
    conn.commit(); conn.close()
    return {"nombre": s.nombre, "score": score, "resultado": resultado, "ratio": round(ratio,2)}

@app.get("/health")
def health():
    result = run_all_checks()
    if result['status'] == 'unhealthy': raise HTTPException(503, detail=result)
    return result
