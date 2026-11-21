#!/usr/bin/env python3
"""¿El modelo suma o recuerda? Evalúa el checkpoint de sumas en tres grupos.

Uso: python evaluar_sumas.py <ruta/a/nanoGPT> [n=500]

- vistos:  pares a+b que sí estuvieron en el entrenamiento
- ocultos: pares de 0–99 que nunca vio (mismo rango, otra combinación)
- 3 cifras: a, b entre 100 y 999 (fuera de todo lo que vio)

Decodificación greedy (siempre el carácter más probable): el modelo contesta lo
mismo cada vez, así que el error no es mala suerte del muestreo.
"""
import pickle, random, sys
from pathlib import Path
import torch

nano = Path(sys.argv[1] if len(sys.argv) > 1 else '../nanoGPT').resolve()
N = int(sys.argv[2]) if len(sys.argv) > 2 else 500
sys.path.insert(0, str(nano))
from model import GPT, GPTConfig  # noqa: E402

ck = torch.load(nano / 'out-sumas' / 'ckpt.pt', map_location='cpu', weights_only=False)
model = GPT(GPTConfig(**ck['model_args']))
model.load_state_dict({k.removeprefix('_orig_mod.'): v for k, v in ck['model'].items()})
model.eval()
meta = pickle.load(open(nano / 'data' / 'sumas' / 'meta.pkl', 'rb'))
stoi, itos = meta['stoi'], meta['itos']


@torch.no_grad()
def responde(a, b):
    x = torch.tensor([[stoi[c] for c in f'\n{a}+{b}=']])
    out = ''
    for _ in range(6):
        logits, _ = model(x[:, -model.config.block_size:])
        nxt = int(logits[0, -1].argmax())
        if itos[nxt] == '\n':
            break
        out += itos[nxt]
        x = torch.cat([x, torch.tensor([[nxt]])], 1)
    return out


def leer(nombre):
    return [tuple(map(int, l.split())) for l in (nano / 'data' / 'sumas' / nombre).read_text().splitlines()]


rnd = random.Random(7)
grupos = {
    'vistos': rnd.sample(leer('pares_vistos.txt'), N),
    'ocultos': rnd.sample(leer('pares_ocultos.txt'), N),
    '3 cifras': [(rnd.randrange(100, 1000), rnd.randrange(100, 1000)) for _ in range(N)],
}
for nombre, pares in grupos.items():
    ok = parece = 0
    errores = []
    for a, b in pares:
        r = responde(a, b)
        parece += r.isdigit()
        if r == str(a + b):
            ok += 1
        elif len(errores) < 4:
            errores.append(f'{a}+{b}={r}  (es {a + b})')
    print(f'{nombre:9} exactitud {ok / len(pares):6.1%}  responde con un número {parece / len(pares):6.1%}  n={len(pares)}')
    for e in errores:
        print('           ', e)
