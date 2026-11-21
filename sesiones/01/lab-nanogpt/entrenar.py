#!/usr/bin/env python3
"""Entrena el modelo de sumas o de transacciones con nanoGPT.

Uso (desde la raíz del repo): uv run sesiones/01/lab-nanogpt/entrenar.py sumas
                              uv run sesiones/01/lab-nanogpt/entrenar.py transacciones

Corre train.py de nanoGPT (clonado junto a este repo) con nuestra configuración y con el
Python del proyecto, así funciona igual en Windows, macOS y Linux.
"""
import argparse, subprocess, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument('modelo', choices=['sumas', 'transacciones'])
ap.add_argument('--nano', type=Path, default=AQUI.parents[3] / 'nanoGPT')
a, extra = ap.parse_known_args()  # extra: overrides de nanoGPT, p. ej. --max_iters=500
nano = a.nano.resolve()
if not (nano / 'data' / a.modelo / 'train.bin').exists():
    sys.exit(f'Faltan los datos en {nano / "data" / a.modelo}. Corre primero preparar_datos.py')
# train.py lee data/ y escribe out-*/ relativos a su carpeta: por eso cwd=nano.
sys.exit(subprocess.run([sys.executable, 'train.py', str(AQUI / f'config_{a.modelo}.py'), *extra], cwd=nano).returncode)
