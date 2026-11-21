# Sesión 01 · El LLM como instrumento de medición en datos

Programa **Experto en IA Agéntica para Datos** (Código Facilito) · Módulo 1 · 3 horas en vivo, sábado. Imparte Carlos Haro.

Deck en `deck/` (motor de h1sort/udlap, que viene de cide y datapub). Labs en `lab-nanogpt/` y `lab-tokens/`.

## 1. La idea

El curso gratuito explicó qué es un LLM. Esta sesión lo **pone a prueba como instrumento**: si lo que sale es un número, ¿cuánto se puede confiar en él y cómo se mide? Tres experimentos, todos con resultados reales:

1. **nanoGPT:** entrenamos un modelo diminuto con sumas y con filas de transacciones. Suma bien el 92% de las veces dentro de lo que vio, 0% fuera, y siempre contesta con un número. Inventa filas que tienen la forma correcta y no son verdad.
2. **Tokens:** cómo se parte un número, una fecha o una fila antes de que el modelo la vea, y cuánto cuesta meter una tabla al contexto.
3. **No determinismo:** la misma pregunta 20 veces, contando respuestas distintas.

Todo desemboca en el **marcador v0** de cada alumno (exactitud, varianza, costo, latencia), que se actualiza el resto del programa.

**Frase de cierre:** *El modelo aprendió cómo se ven los datos. Saber si son verdad es trabajo nuestro, y hoy empezamos a medirlo.*

## 2. Guion (≈192 min: ver recortes abajo)

| # | Acto | id | Contenido | min |
|---|---|---|---|---|
| 1 | Apertura | `title` | Título de la sesión | 1 |
| 2 | | `quien` | who_is_this_dude + QRs (repo con ícono de GitHub, láminas) | 2 |
| 3 | | `programa` | Curso gratuito vs programa: construir y medir | 3 |
| 4 | | `marcador` | Los cuatro números del marcador | 3 |
| 5 | | `hoy` | Mapa de la sesión | 2 |
| 6 | Repaso | `repaso` | Tres cosas que ya sabemos (clase 3 gratuita) | 5 |
| 7 | | `pregunta` | ¿Y si el siguiente token es un número? | 2 |
| 8 | | `instrumento` | Termómetro vs LLM: exactitud, precisión, rango, costo. Explica el título | 3 |
| 9 | nanoGPT | `nanogpt` | Qué es nanoGPT, por qué este y no nanochat | 3 |
| 10 | | `experimento` | Modelo 1 (sumas) y modelo 2 (transacciones) | 3 |
| 11 | | `apuesta` | La sala apuesta: vistas, escondidas, 3 cifras | 3 |
| 12 | | `lab-nanogpt` | Lab con cronómetro: los dos modelos, entrenar e inferencia (25 min) | 28 |
| 13 | | `perdida` | La curva de pérdida | 3 |
| 14 | | `sumas` | Modelo 1: 92.8% · 92.0% · 0.0% y siempre un número | 6 |
| 15 | | `filas` | Modelo 2: entrenar → inferencia → revisar con código | 6 |
| 16 | | `leccion` | Aprendió cómo se ven los datos, no qué es verdad | 3 |
| 17 | Pausa | `pausa` | 10 minutos con cronómetro | 10 |
| 18 | Tokens | `tokens-numeros` | Cómo se parte un número, una fecha, un monto | 6 |
| 19 | | `tokens-fila` | Una fila del caso ≈ 37 tokens; cuántas caben | 5 |
| 20 | | `ddia` | 200 mil tokens ≈ 1 DDIA · 1 millón ≈ 5 · tu tabla ≈ 180 | 2 |
| 21 | | `tokens-costo` | Filas × tokens × precio (precio en vivo) | 4 |
| 22 | | `no-sumes` | El modelo no suma: escribe código | 3 |
| 23 | | `lab-tokens` | Lab: tokeniza tus propios datos (4 min) | 4 |
| 24 | Modelos de otros y no determinismo | `modelos-de-otros` | Tu ckpt de 0.79M vs Inkling 2 Mini (26.4B, pesos abiertos) | 3 |
| 25 | | `donde-corre` | Remoto (OpenRouter) o local (Ollama): .env | 4 |
| 26 | | `veinte` | La misma pregunta 20 veces, con el comando en la lámina | 5 |
| 27 | | `medir-varianza` | Distintas, consenso, exactitud | 5 |
| 28 | | `temperatura-cero` | 1,000 corridas a temperatura 0 → 80 respuestas | 4 |
| 29 | | `por-que-varia` | Muestreo, lote compartido, razonamiento; y en local | 3 |
| 30 | | `lab-veinte` | Lab: tus 20, y a temperatura 0 (8 min) | 8 |
| 31 | Salidas estructuradas | `contrato` | JSON Schema como contrato | 6 |
| 32 | | `forma-verdad` | Forma ✓, verdad ✗ | 4 |
| 33 | | `lab-esquema` | Lab: la respuesta con esquema (8 min) | 8 |
| 34 | Marcador v0 | `set-dorado` | Qué es el set dorado | 5 |
| 35 | | `lab-marcador` | Lab: primera corrida → marcador v0 (15 min) | 15 |
| 36 | | `plantilla` | Tu marcador v0 | 4 |
| 37 | Cierre | `entregable` | Lo que entregas hoy | 2 |
| 38 | | `siguiente` | Sesión 2: elegir modelo (y modelos de decisión) | 2 |
| 39 | | `gracias` | Cierre y QRs | 1 |
| 40 | | `fuentes` | Fuentes | — |

**Recortes para quedar en 180:** el lab de tokens se vuelve tarea (−4), `repaso` a 3 min (−2), el lab de esquema lo hace el profesor en vivo con el comando de la lámina (−5), `temperatura-cero` a 2 min (−2). Nunca cortar `apuesta`, `sumas`, `filas` ni `lab-marcador`.

**Cronómetros:** las láminas de lab y la pausa traen un cronómetro (clic en los dígitos para iniciar o pausar; +1 min, +30 s, ↺). Sigue corriendo aunque cambies de lámina.

**Todos los comandos** se corren desde la raíz del repo con `uv run`, en una sola línea: funcionan igual en PowerShell, cmd, macOS y Linux.

## 3. Fuentes (todo número en lámina necesita una)

- **nanoGPT**: Andrej Karpathy, https://github.com/karpathy/nanoGPT (MIT). `model.py` y `train.py` ~300 líneas cada uno. Desde nov 2025 el README lo marca como viejo y recomienda nanochat (https://github.com/karpathy/nanochat); aquí se usa nanoGPT porque es el más chico que entrena en clase en CPU.
- **Resultados del lab** (corrida propia, 21 nov 2026, CPU de 2 núcleos, PyTorch 2.15, semillas fijas, scripts en `lab-nanogpt/`):
  - Sumas: modelo de 0.79M parámetros, 3,000 iteraciones, 4 min 19 s. Pérdida 2.66 → 1.06 (train) / 1.07 (val).
  - `evaluar_sumas.py`, n=500 por grupo, greedy: vistos 92.8%, ocultos 92.0%, 3 cifras 0.0%; responde con un número 100% en los tres. Errores típicos: el acarreo (16+70=76).
  - Transacciones: mismo tamaño, 3,000 iteraciones, 8 min 41 s. Pérdida 4.02 → 0.40. Ver §3.1.
- **Tokenización**: medición propia con `tiktoken` (OpenAI), codificaciones o200k_base y cl100k_base, script `lab-tokens/tokens.py`. Las dos dan los mismos cortes en todos los ejemplos de la lámina. Fila del caso (`caso/transacciones.csv`, o200k_base): 36.7 tokens en promedio (34–40), encabezado 20; la tabla completa de 500 filas, 18,347 tokens. La primera fila (TX-00304) son 36 tokens; la lámina muestra sus cortes reales.
- **Filas que caben**: `tokens.py`: ~5,456 filas en 200 mil (lámina: ~5,450) y ~27,282 en 1 millón (~27,300); un millón de filas ≈ 37 millones de tokens. Sin contar instrucciones ni respuesta.
- **DDIA**: Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly, marzo 2017, 616 páginas (ficha de O'Reilly; el sitio del autor dice 614). Tokens por libro: **estimación**, no medición: con la regla de ~3 páginas por cada mil tokens (Redis, "context window"), ~205 mil tokens → 200 mil ≈ 1 DDIA, 1 millón ≈ 5, 37 millones ≈ 180.
- **Inkling 2 Mini**: Thinking Machines Lab, "Introducing Inkling 2 Mini" (20 nov 2026), https://thinkingmachines.ai/news/inkling-2-mini/ : 26.4B parámetros totales, 3.4B activos, ~20 GB, pesos abiertos (Apache 2.0, ficha en Hugging Face `thinkingmachines/Inkling-2-Mini`), en Ollama para Macs con 32 GB o más. En OpenRouter como `thinkingmachines/inkling-2-mini`; el precio no va en lámina (las fuentes no coinciden: $0.08/$0.35 vs $0.10/$0.40 por millón): se copia en vivo de la página del modelo. La página del modelo no dice nada sobre determinismo al servirlo.
- **Modelos locales**: Ollama, `qwen3:1.7b` (1.4 GB), `qwen3:4b` (2.5 GB), `inkling-2-mini` (~20 GB), según ollama.com/library.
- **No determinismo a temperatura 0**: Horace He y Thinking Machines Lab, "Defeating Nondeterminism in LLM Inference" (10 sep 2025). https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/
- **Salidas estructuradas**: OpenAI, "Introducing Structured Outputs in the API" (6 ago 2024), https://openai.com/index/introducing-structured-outputs-in-the-api/ ; JSON Schema, https://json-schema.org
- **Modelos de decisión (adelanto de la sesión 2)**: Jev de TypeSafe; ver `SYLLABUS.md`.
- **Precios por token**: no van en lámina; se consultan en vivo en la página del proveedor que use la sala.

### 3.1 Transacciones
`evaluar_transacciones.py`, 300 filas, temperatura 0.8, semilla 1337. Porcentajes sobre las 300 filas (una fila mal formada falla todas las reglas):
forma 87.7% · cliente existe 87.7% · método existe 87.0% · fecha existe 85.7% · total = cantidad × precio 85.0% · comercio existe 79.0% · **pasa todas 74.0%**.
Ejemplos reales en la lámina: `2026-02-30` (fecha), `Café Tres Volco Ruiz … 4,1790.50,6162.00` (total: 4 × 1,790.50 = 7,162; y comercio), `Ferretería Lupita` (comercio inventado), `TDDD` (método).

### 3.2 Lab de 20 corridas
Primeras 50 filas del caso. Verdad por código: ticket promedio con tarjeta = **1,606.24** si tarjeta es TDC y TDD, **985.36** si solo TDC. La pregunta es ambigua a propósito.

## 4. Pendientes antes de la clase

- [x] **Caso v0 y set dorado** (`caso/`): 500 transacciones y 10 preguntas, cada respuesta verificada en Python y SQL. Crece en los siguientes módulos (más tablas, preguntas escondidas para el proyecto final).
- [x] **Scripts de `lab-veinte/` y `lab-marcador/`** sobre `herramientas/llm.py` (API compatible con OpenAI: OpenAI, OpenRouter, Ollama). Probados contra un servidor simulado; **falta una corrida real** con un modelo, y grabarla como respaldo para `veinte`.
- [x] **Checkpoint de respaldo**: `lab-nanogpt/respaldo/` (solo pesos, ~3 MB cada uno) + `usar_respaldo.py`.
- [x] **Todo con uv y Python 3.14**, comandos de una línea desde la raíz del repo (sin `$PWD`): probado en Linux; falta probar en una máquina Windows real.
- [ ] **Corrida real con Inkling 2 Mini** (OpenRouter) de `veinte` y `marcador`, y grabar la de `veinte` como respaldo.
- [ ] **Mandar a los alumnos la preparación previa** (README de la raíz): uv, clonar, `uv sync`, `.env`, y Ollama + modelo si van a usar local.
- [ ] Ensayar una vez con cronómetro.
