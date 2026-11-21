"""Cliente mínimo para cualquier API compatible con OpenAI (OpenRouter, OpenAI, Ollama local…).

Solo biblioteca estándar. Se configura con un archivo .env en la raíz del repo
(copia .env.ejemplo a .env y edítalo). Las variables de entorno, si existen, ganan:
  LLM_BASE_URL  https://openrouter.ai/api/v1 · http://localhost:11434/v1 (Ollama) · …
  LLM_MODEL     thinkingmachines/inkling-2-mini · qwen3:4b · …
  LLM_API_KEY   la llave del proveedor (Ollama no la necesita)
"""
import json, os, time, urllib.error, urllib.request
from pathlib import Path


def _leer_env():
    f = Path(__file__).resolve().parents[1] / '.env'
    if f.exists():
        for linea in f.read_text(encoding='utf-8').splitlines():
            linea = linea.strip()
            if linea and not linea.startswith('#') and '=' in linea:
                k, v = linea.split('=', 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


_leer_env()
BASE = os.environ.get('LLM_BASE_URL', 'https://openrouter.ai/api/v1').rstrip('/')
MODEL = os.environ.get('LLM_MODEL', 'thinkingmachines/inkling-2-mini')
KEY = os.environ.get('LLM_API_KEY', '')


def chat(mensajes, esquema=None, temperatura=None, max_tokens=800):
    """Devuelve dict(texto, entrada, salida, segundos). `esquema`: JSON Schema de la respuesta."""
    body = {'model': MODEL, 'messages': mensajes, 'max_tokens': max_tokens}
    if temperatura is not None:
        body['temperature'] = temperatura
    if esquema:
        body['response_format'] = {'type': 'json_schema',
                                   'json_schema': {'name': 'respuesta', 'strict': True, 'schema': esquema}}
    t0 = time.time()
    try:
        r = _post(body)
    except urllib.error.HTTPError as e:
        if not esquema or e.code != 400:
            raise
        # Algunos modelos no aceptan json_schema: cae a JSON simple y lo dice.
        print(f'  [aviso] {MODEL} no aceptó json_schema; uso response_format json_object')
        body['response_format'] = {'type': 'json_object'}
        r = _post(body)
    u = r.get('usage') or {}
    return {'texto': r['choices'][0]['message']['content'] or '', 'entrada': u.get('prompt_tokens', 0),
            'salida': u.get('completion_tokens', 0), 'segundos': time.time() - t0}


def _post(body):
    req = urllib.request.Request(f'{BASE}/chat/completions', data=json.dumps(body).encode(),
                                 headers={'Content-Type': 'application/json',
                                          **({'Authorization': f'Bearer {KEY}'} if KEY else {})})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.loads(r.read())


ESQUEMA_RESPUESTA = {
    'type': 'object',
    'properties': {
        'valor': {'type': ['number', 'string'], 'description': 'La respuesta: un número, o un texto si se pide un nombre, ID o fecha'},
        'unidad': {'type': 'string', 'enum': ['MXN', 'conteo', '%', 'texto']},
        'definicion': {'type': 'string', 'description': 'Cómo interpretaste la pregunta'},
        'supuestos': {'type': 'array', 'items': {'type': 'string'}},
    },
    'required': ['valor', 'unidad', 'definicion', 'supuestos'],
    'additionalProperties': False,
}


def extraer_valor(texto):
    """Saca la respuesta de un JSON con 'valor', o la última cifra/línea si es prosa."""
    import re
    try:
        return json.loads(texto)['valor']
    except (ValueError, KeyError, TypeError):
        pass
    nums = re.findall(r'-?\d[\d,]*\.?\d*', texto.replace('$', ''))
    return nums[-1].replace(',', '') if nums else texto.strip().splitlines()[-1] if texto.strip() else ''


def coincide(valor, verdad, tol=0.005):
    """Números: error relativo ≤ 0.5%. Textos: igualdad sin mayúsculas ni espacios extra."""
    try:
        v, t = float(str(valor).replace(',', '').replace('%', '').replace('$', '')), float(verdad)
        return abs(v - t) <= tol * max(1.0, abs(t))
    except (TypeError, ValueError):
        return str(valor).strip().lower() == str(verdad).strip().lower()
