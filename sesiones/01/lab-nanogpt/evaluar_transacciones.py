#!/usr/bin/env python3
"""¿Las filas que inventa el modelo serían aceptadas por un sistema real?

Uso: python evaluar_transacciones.py <ruta/a/nanoGPT> [n=300]

Genera n filas con el checkpoint de transacciones (temperatura 0.8, como
sample.py) y revisa cada una contra el catálogo y las reglas del negocio:
7 columnas, cliente y comercio existen, fecha válida dentro del periodo,
cantidad 1–5, y total = cantidad × precio_unitario.
"""
import csv, io, json, pickle, sys
from datetime import date
from pathlib import Path
import torch

nano = Path(sys.argv[1] if len(sys.argv) > 1 else '../nanoGPT').resolve()
N = int(sys.argv[2]) if len(sys.argv) > 2 else 300
sys.path.insert(0, str(nano))
from model import GPT, GPTConfig  # noqa: E402

torch.manual_seed(1337)
ck = torch.load(nano / 'out-transacciones' / 'ckpt.pt', map_location='cpu', weights_only=False)
model = GPT(GPTConfig(**ck['model_args']))
model.load_state_dict({k.removeprefix('_orig_mod.'): v for k, v in ck['model'].items()})
model.eval()
d = nano / 'data' / 'transacciones'
meta = pickle.load(open(d / 'meta.pkl', 'rb'))
stoi, itos = meta['stoi'], meta['itos']
cat = json.loads((d / 'catalogo.json').read_text())
clientes, comercios, metodos = set(cat['clientes']), set(cat['comercios']), set(cat['metodos'])
ini, fin = (date.fromisoformat(x) for x in cat['fechas'])


@torch.no_grad()
def filas(n):
    out, x = [], torch.tensor([[stoi['\n']]])
    buf = ''
    while len(out) < n:
        x = model.generate(x, 200, temperature=0.8, top_k=200)
        texto = ''.join(itos[int(i)] for i in x[0].tolist())
        x = x[:, -1:]
        buf += texto[1:]
        *completas, buf = buf.split('\n')
        out += [f for f in completas if f]
    return out[:n]


def revisar(f):
    p = next(csv.reader(io.StringIO(f)))
    if len(p) != 7:
        return {'forma': False}
    fecha, cli, com, met, cant, precio, total = p
    r = {'forma': True, 'cliente existe': cli in clientes, 'comercio existe': com in comercios,
         'método válido': met in metodos}
    try:
        r['fecha válida'] = ini <= date.fromisoformat(fecha) <= fin
    except ValueError:
        r['fecha válida'] = False
    try:
        r['total = cantidad × precio'] = abs(int(cant) * float(precio) - float(total)) < 0.005
    except ValueError:
        r['total = cantidad × precio'] = False
    return r


gen = filas(N)
res = [revisar(f) for f in gen]
reglas = ['forma', 'cliente existe', 'comercio existe', 'método válido', 'fecha válida', 'total = cantidad × precio']
print(f'{N} filas generadas')
for k in reglas:
    print(f'  {k:28} {sum(r.get(k, False) for r in res) / N:6.1%}')
todas = sum(all(r.get(k, False) for k in reglas) for r in res)
print(f'  {"pasa TODAS las reglas":28} {todas / N:6.1%}')
print('\nEjemplos que se ven bien y no lo están:')
malas = [(f, r) for f, r in zip(gen, res) if r.get('forma') and not all(r.get(k, False) for k in reglas)]
for f, r in malas[:8]:
    print(' ', f, '  <-', ', '.join(k for k in reglas if not r.get(k, False)))
print('\nUn ejemplo por regla:')
for k in reglas[1:]:
    eg = next((f for f, r in zip(gen, res) if r.get('forma') and not r.get(k, False)), None)
    if eg:
        print(f'  {k:28} {eg}')
print('\nEjemplos que pasan todo:')
for f, r in [(f, r) for f, r in zip(gen, res) if all(r.get(k, False) for k in reglas)][:3]:
    print(' ', f)
