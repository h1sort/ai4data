# Lab · nanoGPT con sumas y transacciones

Sesión 01. Entrenamos un GPT diminuto ([nanoGPT](https://github.com/karpathy/nanoGPT), de Andrej Karpathy) con dos datasets generados para el curso, y medimos qué aprendió.

```bash
# en la misma carpeta
git clone https://github.com/h1sort/ai4data
git clone https://github.com/karpathy/nanoGPT
pip install torch numpy
L=$PWD/ai4data/sesiones/01/lab-nanogpt

python $L/preparar_datos.py nanoGPT          # datos con semilla fija
cd nanoGPT
python train.py $L/config_sumas.py           # ~4 min en una CPU de 2 núcleos
python $L/evaluar_sumas.py .
python train.py $L/config_transacciones.py   # ~9 min
python $L/evaluar_transacciones.py .
```

| Archivo | Qué hace |
|---|---|
| `preparar_datos.py` | Genera `data/sumas` (a+b con a, b ∈ 0–99; 20% de los pares escondidos) y `data/transacciones` (filas de un comercio ficticio con reglas verificables). |
| `config_*.py` | Modelo de 0.79M parámetros, 3,000 iteraciones, CPU. Ojo: `gradient_accumulation_steps = 1`; el valor por defecto de nanoGPT (40) es 40 veces más lento. |
| `evaluar_sumas.py` | Exactitud en pares vistos, escondidos y de 3 cifras, con decodificación greedy. |
| `evaluar_transacciones.py` | Genera filas y las revisa contra el catálogo: cliente, comercio, método, fecha y total = cantidad × precio. |
| `respaldo/` | Pesos ya entrenados (sin estado del optimizador), por si tu laptop es lenta. Cópialos a `nanoGPT/out-sumas/ckpt.pt` y `nanoGPT/out-transacciones/ckpt.pt`, corre `preparar_datos.py` y luego los scripts de evaluación. |

## Resultados de referencia (21 nov 2026, CPU de 2 núcleos)

| Sumas, n=500 por grupo | Exactitud | Contesta con un número |
|---|---|---|
| Vistas | 92.8% | 100% |
| Escondidas | 92.0% | 100% |
| 3 cifras | 0.0% | 100% |

Transacciones, 300 filas generadas: 74.0% pasan todas las reglas. Fallan sobre todo por comercios inventados (79.0% existe), totales mal multiplicados (85.0%) y fechas imposibles como `2026-02-30`.

Karpathy marca nanoGPT como viejo desde noviembre de 2025 y recomienda [nanochat](https://github.com/karpathy/nanochat). Aquí usamos nanoGPT porque es el más chico que entrena en clase, en CPU.
