#!/usr/bin/env python3
import re, sys
from datetime import datetime
from collections import defaultdict

SQL_PATTERNS = [
    (r"'\s*OR\s*'?1'?\s*=\s*'?1",  "Bypass de login (OR 1=1)"),
    (r"'\s*--",                      "Comentario SQL para ignorar password"),
    (r"UNION\s+SELECT",              "Exfiltración UNION SELECT"),
    (r"DROP\s+TABLE",                "Destrucción de tabla DROP TABLE"),
    (r"INSERT\s+INTO.*SELECT",       "Inyección de datos"),
    (r"EXEC\s*\(",                   "Ejecución de comandos EXEC"),
]

def analyze_log(log_path):
    incidents, by_ip, total = [], defaultdict(int), 0
    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            for num, line in enumerate(f, 1):
                total += 1
                line = line.strip()
                if not line: continue
                for pattern, desc in SQL_PATTERNS:
                    if re.search(pattern, line, re.IGNORECASE):
                        m = re.search(r'IP:(\S+)', line)
                        ip = m.group(1) if m else 'desconocida'
                        incidents.append({'line': num, 'type': desc, 'ip': ip, 'content': line[:100]})
                        by_ip[ip] += 1
                        break
    except FileNotFoundError:
        print(f'ERROR: Archivo no encontrado: {log_path}'); sys.exit(1)
    return {'total': total, 'clean': total - len(incidents), 'incidents': incidents, 'by_ip': dict(by_ip)}

def print_report(r, path):
    print(f'\n{"="*60}')
    print(f'  REPORTE DE SEGURIDAD — FinTech Nova')
    print(f'  Archivo: {path} | Fecha: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'  Total: {r["total"]} | Limpias: {r["clean"]} | Incidentes: {len(r["incidents"])}')
    print(f'{"="*60}')
    for i, inc in enumerate(r['incidents'], 1):
        print(f'  [{i}] Linea {inc["line"]} | {inc["type"]} | IP: {inc["ip"]}')
    print('\n  IPs activas:')
    for ip, c in sorted(r['by_ip'].items(), key=lambda x: -x[1]):
        print(f'    {ip}: {c} ataque(s)')

if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else 'server.log'
    print_report(analyze_log(path), path)
