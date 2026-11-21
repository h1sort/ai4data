# Experto en IA Agéntica para Datos

Programa en vivo de 12 sesiones con [Código Facilito](https://codigofacilito.com/programas/ia-datos), impartido por Carlos Haro. Sábados, 3 horas por sesión, 6 módulos y un proyecto final.

Producir el análisis se volvió barato. Saber si es verdad, no. En este programa construyes un sistema de IA sobre datos y demuestras con números que se puede confiar en él.

- **Temario completo:** [SYLLABUS.md](SYLLABUS.md)
- **Versión web:** [h1sort.com/ai4data](https://h1sort.com/ai4data/)
- **Curso introductorio gratuito (pre-requisito):** [h1sort/intro-ai4data-class](https://github.com/h1sort/intro-ai4data-class)

## Antes de la sesión 1 (hazlo en casa: descarga varios GB)

1. Instala **git** y **uv** ([docs.astral.sh/uv](https://docs.astral.sh/uv/getting-started/installation/)). uv instala Python 3.14 por ti.
2. Clona los dos repos **en la misma carpeta**:
   ```
   git clone https://github.com/h1sort/ai4data
   git clone https://github.com/karpathy/nanoGPT
   ```
3. Entra a `ai4data` y prepara el entorno (descarga PyTorch):
   ```
   cd ai4data
   uv sync
   ```
4. Instala [Ollama](https://ollama.com/download) y descarga el modelo local del curso: `ollama pull qwen3:1.7b` (1.4 GB, cuantizado a 4 bits; corre en casi cualquier laptop). Si tu máquina tiene muy poca memoria: `ollama pull qwen3:0.6b` (523 MB).
5. Copia `.env.example` a `.env`. Por defecto usa tu qwen3 local. Si prefieres no correr nada local, activa la opción de tu llave de OpenAI (`gpt-6-luna`) o de Anthropic (`claude-haiku-5-5`).
6. Prueba que todo funciona: `uv run sesiones/01/lab-tokens/tokens.py`

Todos los comandos del curso se corren desde la carpeta `ai4data` con `uv run`, en una sola línea: funcionan igual en Windows (PowerShell o cmd), macOS y Linux.

## Módulos

| | Módulo | Sesiones |
|---|---|---|
| 01 | Fundamentos de LLMs para Análisis de Datos | 1–2 |
| 02 | LLMs vía Chat y RAG para Datos | 3–4 |
| 03 | LLMs vía Copilotos y CLIs para Datos | 5–6 |
| 04 | LLMs vía APIs y Productos en Data Warehouses | 7–8 |
| 05 | Evaluaciones (Evals) para Sistemas de IA en Datos | 9–10 |
| 06 | Flujos Avanzados, Equipos | 11–12 |

## Material

| Sesión | Láminas | Labs |
|---|---|---|
| 01 · El LLM como instrumento de medición en datos | [h1sort.com/ai4data/01](https://h1sort.com/ai4data/01/) | [sesiones/01](sesiones/01/) |

- `caso/`: los datos del caso (comercio ficticio) y el set dorado, con cada respuesta verificada en Python y SQL.
- `herramientas/`: cliente mínimo para cualquier API compatible con OpenAI (Ollama, OpenAI, Anthropic) y el script que publica la copia web.
- `web/`: la fuente de [h1sort.com/ai4data](https://h1sort.com/ai4data/). La copia del sitio vive en h1sort-website; se actualiza con `herramientas/publicar.py`.

El material de las siguientes sesiones se irá publicando aquí.
