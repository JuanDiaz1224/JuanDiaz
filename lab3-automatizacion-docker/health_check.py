import sqlite3, shutil, os, time
from datetime import datetime

def check_database(db_path='database.db'):
    if not os.path.exists(db_path):
        return 'error', f'BD no encontrada: {db_path}'
    try:
        start = time.time()
        conn = sqlite3.connect(db_path, timeout=5)
        conn.execute('SELECT 1')
        conn.close()
        ms = (time.time() - start) * 1000
        return ('warning', f'BD lenta: {ms:.1f}ms') if ms > 500 else ('ok', f'BD OK en {ms:.1f}ms')
    except sqlite3.OperationalError as e:
        return 'error', f'Error BD: {e}'

def check_disk(path='/'):
    try:
        u = shutil.disk_usage(path)
        pct = (u.used / u.total) * 100
        gb = u.free / (1024**3)
        if pct >= 95: return 'error',   f'Disco critico: {pct:.1f}% ({gb:.1f}GB libre)'
        if pct >= 80: return 'warning', f'Disco alto: {pct:.1f}% ({gb:.1f}GB libre)'
        return 'ok', f'Disco OK: {pct:.1f}% ({gb:.1f}GB libre)'
    except Exception as e:
        return 'error', f'Error disco: {e}'

def check_backup(backup_dir='backups'):
    if not os.path.isdir(backup_dir):
        return 'warning', 'Directorio backups no existe (ejecuta backup_db.sh primero)'
    backups = sorted([f for f in os.listdir(backup_dir) if f.endswith('.tar.gz')])
    if not backups: return 'error', 'No hay backups'
    age = (time.time() - os.path.getmtime(os.path.join(backup_dir, backups[-1]))) / 3600
    return ('warning', f'Backup antiguo: {age:.1f}h') if age > 25 else ('ok', f'Backup OK: {age:.1f}h')

def check_memory():
    try:
        import psutil
        pct = psutil.virtual_memory().percent
        if pct >= 90: return 'error',   f'RAM critica: {pct:.1f}%'
        if pct >= 75: return 'warning', f'RAM alta: {pct:.1f}%'
        return 'ok', f'RAM OK: {pct:.1f}%'
    except ImportError:
        return 'warning', 'psutil no instalado'

def run_all_checks():
    checks = {
        'database': dict(zip(['status','message'], check_database())),
        'disk':     dict(zip(['status','message'], check_disk())),
        'backup':   dict(zip(['status','message'], check_backup())),
        'memory':   dict(zip(['status','message'], check_memory())),
    }
    statuses = [v['status'] for v in checks.values()]
    overall = 'unhealthy' if 'error' in statuses else 'degraded' if 'warning' in statuses else 'healthy'
    return {'status': overall, 'timestamp': datetime.utcnow().isoformat()+'Z', 'version': '1.0.0', 'checks': checks}

if __name__ == '__main__':
    import json
    print(json.dumps(run_all_checks(), indent=2, ensure_ascii=False))
