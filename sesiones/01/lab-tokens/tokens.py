#!/usr/bin/env python3
"""¿Cuántos tokens cuesta tu tabla? Con los tokenizadores de OpenAI (o200k_base y cl100k_base).

Uso (desde la raíz del repo): uv run sesiones/01/lab-tokens/tokens.py [archivo.csv]

Sin archivo: los ejemplos de la lámina y el CSV del caso. La primera vez, tiktoken
descarga los tokenizadores (~4 MB) y los guarda en caché.
"""
import sys
from pathlib import Path
import tiktoken

RAIZ = Path(__file__).resolve().parents[3]
EJEMPLOS = ['7', '42', '999', '1000', '1234567', '3.14159', '1,234,567.89', '$1,249.50',
            '2026-11-21', '21/11/2026', 'CLI-0164', '23+45=68']
archivo = Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / 'caso' / 'transacciones.csv'
lineas = archivo.read_text(encoding='utf-8').strip().splitlines()

for nombre in ('o200k_base', 'cl100k_base'):
    enc = tiktoken.get_encoding(nombre)
    print(f'\n== {nombre}')
    if len(sys.argv) == 1:
        for s in EJEMPLOS:
            ids = enc.encode(s)
            print(f'{s!r:16} {len(ids):2}  ' + ' | '.join(enc.decode([i]) for i in ids))
    n = [len(enc.encode(l + '\n')) for l in lineas[1:]]
    prom = sum(n) / len(n)
    print(f'\n{archivo.name}: encabezado {len(enc.encode(lineas[0] + chr(10)))} tokens · {len(n)} filas · '
          f'{prom:.1f} tokens por fila (min {min(n)}, max {max(n)})')
    print(f'  caben ~{int(200_000 / prom):,} filas en 200 mil tokens · ~{int(1_000_000 / prom):,} en 1 millón')
    cols = lineas[0].split(',')
    por = [0] * len(cols)
    for l in lineas[1:201]:
        for i, v in enumerate(l.split(',')[:len(cols)]):
            por[i] += len(enc.encode(v))
    print(f'  columna más cara (primeras 200 filas): {cols[por.index(max(por))]}')
