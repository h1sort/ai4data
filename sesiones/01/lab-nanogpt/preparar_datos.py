#!/usr/bin/env python3
"""Genera los dos datasets del lab de nanoGPT (sesión 1) en formato de caracteres.

Uso (desde la raíz del repo): uv run sesiones/01/lab-nanogpt/preparar_datos.py [ruta/a/nanoGPT]

Por defecto usa ../nanoGPT, es decir, nanoGPT clonado junto a este repo.

Escribe nanoGPT/data/sumas/ y nanoGPT/data/transacciones/ con train.bin, val.bin
y meta.pkl, igual que data/shakespeare_char de nanoGPT. Semilla fija: todos en el
salón entrenan con exactamente los mismos datos.

- sumas: "a+b=c" con a, b entre 0 y 99. El 20% de los pares NO se usa para entrenar
  (pares_ocultos.txt): sirven para ver si el modelo suma o si recuerda.
- transacciones: filas CSV de un comercio ficticio con reglas que sí se pueden
  verificar (cliente existe, comercio existe, fecha válida, total = cantidad × precio).
"""
import json, pickle, random, sys
from datetime import date, timedelta
from pathlib import Path
import numpy as np

SEED = 2026
RAIZ = Path(__file__).resolve().parents[3]
nano = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else RAIZ.parent / 'nanoGPT'
if not (nano / 'train.py').exists():
    sys.exit(f'No encuentro nanoGPT en {nano}. Clónalo junto a este repo: git clone https://github.com/karpathy/nanoGPT')


def guardar(nombre, texto_train, texto_val, extra=None):
    out = nano / 'data' / nombre
    out.mkdir(parents=True, exist_ok=True)
    chars = sorted(set(texto_train + texto_val))
    stoi = {c: i for i, c in enumerate(chars)}
    itos = {i: c for c, i in stoi.items()}
    enc = lambda s: np.array([stoi[c] for c in s], dtype=np.uint16)
    enc(texto_train).tofile(out / 'train.bin')
    enc(texto_val).tofile(out / 'val.bin')
    with open(out / 'meta.pkl', 'wb') as f:
        pickle.dump({'vocab_size': len(chars), 'itos': itos, 'stoi': stoi}, f)
    for k, v in (extra or {}).items():
        (out / k).write_text(v)
    print(f'{nombre}: {len(texto_train):,} caracteres de entrenamiento, vocabulario de {len(chars)} -> {out}')


# ---- sumas -------------------------------------------------------------------
rnd = random.Random(SEED)
pares = [(a, b) for a in range(100) for b in range(100)]
rnd.shuffle(pares)
corte = int(len(pares) * 0.8)
vistos, ocultos = pares[:corte], pares[corte:]
linea = lambda a, b: f'{a}+{b}={a + b}\n'
lista = list(vistos) * 3  # cada par visto aparece 3 veces
rnd.shuffle(lista)
train = ''.join(linea(a, b) for a, b in lista)
val = ''.join(linea(a, b) for a, b in vistos[:500])  # val = vistos: medimos memoria, no generalización
guardar('sumas', train, val, {
    'pares_vistos.txt': ''.join(f'{a} {b}\n' for a, b in vistos),
    'pares_ocultos.txt': ''.join(f'{a} {b}\n' for a, b in ocultos),
})

# ---- transacciones -------------------------------------------------------------
rnd = random.Random(SEED)
comercios = {  # comercio ficticio -> rango de precio unitario (MXN)
    'Abarrotes La Esperanza': (12, 180), 'Farmacia del Centro': (35, 900),
    'Papelería El Lápiz': (8, 240), 'Café Tres Volcanes': (38, 140),
    'Ferretería Don Beto': (15, 1600), 'Panadería La Espiga': (6, 95),
    'Librería Mar Abierto': (120, 780), 'Taller Mecánico Ruiz': (250, 4200),
    'Tortillería Lupita': (14, 60), 'Óptica Visión Clara': (300, 3800),
    'Lavandería Burbujas': (45, 320), 'Veterinaria Patitas': (150, 1900),
}
metodos = ['TDC', 'TDD', 'EFECTIVO', 'SPEI']
clientes = [f'CLI-{i:04d}' for i in range(1, 301)]
inicio = date(2026, 1, 1)
filas = []
for _ in range(14000):
    d = inicio + timedelta(days=rnd.randrange(181))  # ene–jun 2026
    c = rnd.choice(clientes)
    m = rnd.choice(list(comercios))
    lo, hi = comercios[m]
    precio = round(rnd.uniform(lo, hi) * 2) / 2
    cant = rnd.choices([1, 2, 3, 4, 5], weights=[50, 22, 12, 9, 7])[0]
    filas.append(f'{d.isoformat()},{c},{m},{rnd.choice(metodos)},{cant},{precio:.2f},{cant * precio:.2f}\n')
encabezado = 'fecha,cliente,comercio,metodo,cantidad,precio_unitario,total\n'
guardar('transacciones', ''.join(filas[:13000]), ''.join(filas[13000:]), {
    'catalogo.json': json.dumps({'clientes': clientes, 'comercios': list(comercios), 'metodos': metodos,
                                 'fechas': ['2026-01-01', '2026-06-30']}, ensure_ascii=False, indent=1),
    'muestra.csv': encabezado + ''.join(filas[:20]),
})
