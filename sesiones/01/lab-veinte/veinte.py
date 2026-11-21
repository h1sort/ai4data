#!/usr/bin/env python3
"""La misma pregunta N veces: ¿cuántas respuestas distintas da el modelo?

Uso (desde la raíz del repo): uv run sesiones/01/lab-veinte/veinte.py [--n 20] [--temperatura 0] [--esquema] [--filas 50]

Mete las primeras --filas transacciones del caso en el prompt y pregunta el ticket
promedio de los pagos con tarjeta. La pregunta es ambigua a propósito (¿tarjeta es
solo TDC, o TDC y TDD?). La verdad se calcula con código para las dos lecturas.
"""
import argparse, csv, json, sys
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / 'herramientas'))
import llm  # noqa: E402

vistos_avisos = set()


def avisar(r):
    for a in r.get('avisos', []):
        if a not in vistos_avisos:
            vistos_avisos.add(a); print(f'  [aviso] {a}')


ap = argparse.ArgumentParser()
ap.add_argument('--n', type=int, default=20)
ap.add_argument('--temperatura', type=float, default=None)
ap.add_argument('--esquema', action='store_true')
ap.add_argument('--filas', type=int, default=50)
a = ap.parse_args()

texto = (RAIZ / 'caso' / 'transacciones.csv').read_text().splitlines()
tabla = '\n'.join(texto[:a.filas + 1])
filas = list(csv.DictReader(texto[:a.filas + 1]))
prom = lambda ms: round(sum(float(f['total']) for f in filas if f['metodo'] in ms) / max(1, sum(f['metodo'] in ms for f in filas)), 2)
verdad = {'TDC y TDD': prom(('TDC', 'TDD')), 'solo TDC': prom(('TDC',))}

pregunta = '¿Cuál es el ticket promedio (total por transacción) de los pagos con tarjeta? Responde en MXN.'
mensajes = [{'role': 'system', 'content': 'Eres un analista de datos. Contesta solo con base en la tabla.' +
             ('' if a.esquema else ' Termina con la respuesta numérica sola en la última línea.')},
            {'role': 'user', 'content': f'Tabla de transacciones (CSV):\n{tabla}\n\n{pregunta}'}]

print(f'modelo {llm.MODEL} · {a.n} corridas · {a.filas} filas · temperatura {a.temperatura if a.temperatura is not None else "por defecto"}'
      f'{" · con esquema" if a.esquema else ""}')
resp, defs, tok, seg = [], Counter(), 0, 0.0
for i in range(a.n):
    r = llm.chat(mensajes, llm.ESQUEMA_RESPUESTA if a.esquema else None, a.temperatura)
    avisar(r)
    v = llm.extraer_valor(r['texto'])
    try:
        v = round(float(v), 2)
    except (TypeError, ValueError):
        pass
    resp.append(v); tok += r['entrada'] + r['salida']; seg += r['segundos']
    if a.esquema:
        try:
            defs[json.loads(r['texto'])['definicion'][:70]] += 1
        except (ValueError, KeyError):
            pass
    print(f'  {i + 1:2d}  {v}')

c = Counter(resp)
moda, veces = c.most_common(1)[0]
print(f'\nverdad: {verdad}')
print(f'distintas   {len(c)} de {a.n}')
print(f'consenso    {veces / a.n:.0%}  (la más común: {moda})')
for k, t in verdad.items():
    print(f'exactitud   {sum(llm.coincide(v, t) for v in resp) / a.n:.0%}  si "tarjeta" = {k}')
print(f'tokens      {tok / a.n:,.0f} por corrida · {seg / a.n:.1f} s por corrida')
if defs:
    print('definiciones que usó:'); [print(f'  {n:2d} × {d}') for d, n in defs.most_common(5)]
