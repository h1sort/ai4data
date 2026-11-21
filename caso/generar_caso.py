#!/usr/bin/env python3
"""Caso del programa, versión 0: 500 transacciones del comercio ficticio y el set dorado.

Uso: python generar_caso.py   (escribe transacciones.csv y set_dorado.jsonl aquí mismo)

Mismas reglas que el lab de nanoGPT (sesión 1). 500 filas ≈ 16 mil tokens: caben en el
contexto de cualquier modelo, así que la sesión 1 mide al modelo leyendo la tabla
directamente. Cada respuesta del set dorado se calcula dos veces (Python y SQL en DuckDB)
y el script falla si no coinciden.
"""
import csv, json, random
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).parent
rnd = random.Random(20261121)
comercios = {
    'Abarrotes La Esperanza': (12, 180), 'Farmacia del Centro': (35, 900),
    'Papelería El Lápiz': (8, 240), 'Café Tres Volcanes': (38, 140),
    'Ferretería Don Beto': (15, 1600), 'Panadería La Espiga': (6, 95),
    'Librería Mar Abierto': (120, 780), 'Taller Mecánico Ruiz': (250, 4200),
    'Tortillería Lupita': (14, 60), 'Óptica Visión Clara': (300, 3800),
    'Lavandería Burbujas': (45, 320), 'Veterinaria Patitas': (150, 1900),
}
metodos = ['TDC', 'TDD', 'EFECTIVO', 'SPEI']
clientes = [f'CLI-{i:04d}' for i in range(1, 121)]
filas = []
for k in range(500):
    d = date(2026, 1, 1) + timedelta(days=rnd.randrange(181))
    m = rnd.choice(list(comercios))
    lo, hi = comercios[m]
    precio = round(rnd.uniform(lo, hi) * 2) / 2
    cant = rnd.choices([1, 2, 3, 4, 5], weights=[50, 22, 12, 9, 7])[0]
    filas.append({'id': f'TX-{k + 1:05d}', 'fecha': d.isoformat(), 'cliente': rnd.choice(clientes), 'comercio': m,
                  'metodo': rnd.choice(metodos), 'cantidad': cant, 'precio_unitario': precio, 'total': round(cant * precio, 2)})
filas.sort(key=lambda f: (f['fecha'], f['id']))
cols = list(filas[0])
with open(HERE / 'transacciones.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, cols, lineterminator='\n'); w.writeheader()
    for r in filas:
        w.writerow({**r, 'precio_unitario': f"{r['precio_unitario']:.2f}", 'total': f"{r['total']:.2f}"})

# ---- set dorado: (pregunta, respuesta en Python, SQL, tipo) ---------------------
r2 = lambda x: round(x, 2)
tot_com, tot_cli, n_dia = defaultdict(float), defaultdict(float), Counter()
for f in filas:
    tot_com[f['comercio']] += f['total']; tot_cli[f['cliente']] += f['total']; n_dia[f['fecha']] += 1
total = sum(f['total'] for f in filas)
tarjeta = [f['total'] for f in filas if f['metodo'] in ('TDC', 'TDD')]
preguntas = [
    ('¿Cuántas transacciones hay en la tabla?', len(filas),
     'SELECT COUNT(*) FROM t', 'conteo'),
    ('¿Cuántos clientes distintos aparecen?', len({f['cliente'] for f in filas}),
     'SELECT COUNT(DISTINCT cliente) FROM t', 'conteo'),
    ('¿Cuál es el monto total vendido en marzo de 2026, en MXN?', r2(sum(f['total'] for f in filas if f['fecha'][:7] == '2026-03')),
     "SELECT ROUND(SUM(total), 2) FROM t WHERE strftime(fecha, '%Y-%m') = '2026-03'", 'MXN'),
    ('¿Qué comercio vendió el mayor monto total?', max(tot_com, key=tot_com.get),
     'SELECT comercio FROM t GROUP BY comercio ORDER BY SUM(total) DESC LIMIT 1', 'texto'),
    ('¿Cuál es el ticket promedio (total por transacción) de los pagos con tarjeta, crédito o débito, en MXN?', r2(sum(tarjeta) / len(tarjeta)),
     "SELECT ROUND(AVG(total), 2) FROM t WHERE metodo IN ('TDC', 'TDD')", 'MXN'),
    ('¿Cuántas transacciones se pagaron en efectivo?', sum(f['metodo'] == 'EFECTIVO' for f in filas),
     "SELECT COUNT(*) FROM t WHERE metodo = 'EFECTIVO'", 'conteo'),
    ('¿Qué porcentaje del monto total se pagó por SPEI? Redondea a un decimal.', round(100 * sum(f['total'] for f in filas if f['metodo'] == 'SPEI') / total, 1),
     "SELECT ROUND(100 * SUM(total) FILTER (WHERE metodo = 'SPEI') / SUM(total), 1) FROM t", '%'),
    ('¿Qué fecha tuvo más transacciones? Responde en formato AAAA-MM-DD.', None,
     'SELECT strftime(fecha, \'%Y-%m-%d\') FROM t GROUP BY fecha ORDER BY COUNT(*) DESC, fecha LIMIT 1', 'texto'),
    ('¿Cuántas transacciones tienen una cantidad mayor a 3?', sum(f['cantidad'] > 3 for f in filas),
     'SELECT COUNT(*) FROM t WHERE cantidad > 3', 'conteo'),
    ('¿Qué cliente gastó más en total? Responde con su ID.', max(tot_cli, key=tot_cli.get),
     'SELECT cliente FROM t GROUP BY cliente ORDER BY SUM(total) DESC LIMIT 1', 'texto'),
]
top = max(n_dia.values())
dias_top = sorted(d for d, n in n_dia.items() if n == top)
preguntas[7] = (preguntas[7][0], dias_top[0], preguntas[7][2], preguntas[7][3])

import duckdb
con = duckdb.connect()
con.execute(f"CREATE TABLE t AS SELECT * FROM read_csv('{HERE / 'transacciones.csv'}')")
with open(HERE / 'set_dorado.jsonl', 'w') as f:
    for i, (q, ans, sql, tipo) in enumerate(preguntas, 1):
        got = con.execute(sql).fetchone()[0]
        got = float(got) if isinstance(ans, float) else (int(got) if isinstance(ans, int) else str(got))
        assert got == ans, f'P{i}: Python {ans!r} ≠ SQL {got!r}'
        f.write(json.dumps({'id': f'P{i:02d}', 'pregunta': q, 'respuesta': ans, 'tipo': tipo, 'sql': sql}, ensure_ascii=False) + '\n')
print(f'{len(filas)} transacciones, {len(preguntas)} preguntas; Python y SQL coinciden en todas.')
if len(dias_top) > 1:
    print('aviso: empate en P08', dias_top)
