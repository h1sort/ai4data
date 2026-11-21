#!/usr/bin/env python3
"""¿Tu laptop no alcanzó a entrenar? Copia los pesos ya entrenados a nanoGPT.

Uso (desde la raíz del repo): uv run sesiones/01/lab-nanogpt/usar_respaldo.py
Después corre los scripts de evaluación como si hubieras entrenado.
"""
import shutil
from pathlib import Path

AQUI = Path(__file__).resolve().parent
nano = AQUI.parents[3] / 'nanoGPT'
for m in ('sumas', 'transacciones'):
    destino = nano / f'out-{m}' / 'ckpt.pt'
    destino.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(AQUI / 'respaldo' / f'{m}.pt', destino)
    print('listo:', destino)
