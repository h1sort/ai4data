# Sesión 01 · El LLM como instrumento de medición en datos

Módulo 1 · Fundamentos de LLMs para Análisis de Datos.

- **Láminas:** [h1sort.com/ai4data/01](https://h1sort.com/ai4data/01/) · fuente en `deck/` (`uv run sesiones/01/deck/tools/serve.py` y abre http://127.0.0.1:8000/deck/; `P` abre la vista de presentador con notas y reloj).
- **Preparación previa:** ver el [README de la raíz](../../README.md). Todo se corre desde la raíz del repo con `uv run`.
- **Guion, tiempos y fuentes:** [PLAN.md](PLAN.md).

| Lab | Carpeta | Tiempo |
|---|---|---|
| Entrenar nanoGPT con sumas y transacciones | [lab-nanogpt/](lab-nanogpt/) | 25 min |
| Tokeniza tus propios datos | [lab-tokens/](lab-tokens/) | 4 min |
| La misma pregunta 20 veces (y con esquema) | [lab-veinte/](lab-veinte/) | 16 min |
| Marcador v0 contra el set dorado | [lab-marcador/](lab-marcador/) | 15 min |

`lab-veinte` y `lab-marcador` usan cualquier API compatible con OpenAI. Se configuran en `.env` (copia de `.env.ejemplo`): Inkling 2 Mini en OpenRouter, o un modelo local en Ollama.

**Entregable:** la salida de `evaluar_sumas.py`, tu `marcador_v0.json` y una frase en el README de tu fork: ¿qué pregunta falló más y por qué?
