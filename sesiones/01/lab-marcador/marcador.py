#!/usr/bin/env python3
"""Marcador v0: el modelo contesta el set dorado leyendo la tabla completa en el prompt.

Uso: python marcador.py --precio-entrada 0.15 --precio-salida 0.60 [--k 3] [--esquema]
     (precios en USD por millón de tokens, de la página de tu proveedor)

Cada pregunta se hace --k veces. Escribe marcador_v0.json con los cuatro números:
exactitud, consenso (varianza), costo por respuesta y latencia por respuesta.
"""
import argparse, json, sys, time
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / 'herramientas'))
import llm  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument('--precio-entrada', type=float, required=True, help='USD por millón de tokens de entrada')
ap.add_argument('--precio-salida', type=float, required=True, help='USD por millón de tokens de salida')
ap.add_argument('--k', type=int, default=3, help='corridas por pregunta')
ap.add_argument('--esquema', action='store_true')
a = ap.parse_args()

tabla = (RAIZ / 'caso' / 'transacciones.csv').read_text()
dorado = [json.loads(l) for l in (RAIZ / 'caso' / 'set_dorado.jsonl').read_text().splitlines()]
sistema = ('Eres un analista de datos. Contesta solo con base en la tabla. '
           + ('' if a.esquema else 'Termina con la respuesta sola en la última línea, sin unidades.'))

filas, aciertos, consensos, costos, latencias = [], 0, [], [], []
print(f'modelo {llm.MODEL} · {len(dorado)} preguntas × {a.k} corridas')
for q in dorado:
    vals = []
    for _ in range(a.k):
        r = llm.chat([{'role': 'system', 'content': sistema},
                      {'role': 'user', 'content': f'Tabla de transacciones (CSV):\n{tabla}\n\n{q["pregunta"]}'}],
                     llm.ESQUEMA_RESPUESTA if a.esquema else None)
        v = llm.extraer_valor(r['texto'])
        ok = llm.coincide(v, q['respuesta'])
        vals.append(str(v)); aciertos += ok
        costos.append((r['entrada'] * a.precio_entrada + r['salida'] * a.precio_salida) / 1e6)
        latencias.append(r['segundos'])
        filas.append({'id': q['id'], 'valor': v, 'verdad': q['respuesta'], 'correcta': ok,
                      'tokens_entrada': r['entrada'], 'tokens_salida': r['salida'], 'segundos': round(r['segundos'], 2)})
    consensos.append(Counter(vals).most_common(1)[0][1] / a.k)
    print(f'  {q["id"]}  verdad {q["respuesta"]!s:22} modelo {", ".join(vals)}')

n = len(dorado) * a.k
marcador = {
    'version': 'v0', 'modelo': llm.MODEL, 'fecha': time.strftime('%Y-%m-%d'), 'metodo': 'tabla completa en el prompt',
    'exactitud': round(aciertos / n, 3), 'consenso': round(sum(consensos) / len(consensos), 3),
    'costo_usd_por_respuesta': round(sum(costos) / n, 5), 'latencia_s_por_respuesta': round(sum(latencias) / n, 2),
    'corridas': filas,
}
(Path(__file__).parent / 'marcador_v0.json').write_text(json.dumps(marcador, ensure_ascii=False, indent=1))
print(f"""
MARCADOR v0 · {llm.MODEL}
  exactitud   {marcador['exactitud']:.0%}
  consenso    {marcador['consenso']:.0%}
  costo       ${marcador['costo_usd_por_respuesta']:.4f} por respuesta
  latencia    {marcador['latencia_s_por_respuesta']:.1f} s por respuesta
Guardado en marcador_v0.json""")
