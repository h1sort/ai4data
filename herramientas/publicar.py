#!/usr/bin/env python3
"""Publica la copia web de este repo en h1sort-website.

Uso: uv run herramientas/publicar.py <ruta/a/h1sort-website>

- web/                       -> public/ai4data/       (temario)
- sesiones/NN/deck (sin notas) -> public/ai4data/NN/  (láminas de cada sesión)

Después, en h1sort-website: npm ci && npm run build, rama nueva, PR y merge.
"""
import shutil, subprocess, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sitio = Path(sys.argv[1]).resolve() / 'public' / 'ai4data'
sitio.mkdir(parents=True, exist_ok=True)
for f in (RAIZ / 'web').iterdir():
    shutil.copy2(f, sitio / f.name)
print('web/ ->', sitio)
for deck in sorted(RAIZ.glob('sesiones/*/deck')):
    n = deck.parent.name
    subprocess.run([sys.executable, str(deck / 'tools' / 'public-build.py'), str(sitio / n)], check=True)
    print(f'sesiones/{n}/deck ->', sitio / n)
