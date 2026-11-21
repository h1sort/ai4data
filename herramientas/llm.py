"""Cliente mínimo para cualquier API compatible con OpenAI (Ollama local, OpenAI, Anthropic…).

Solo biblioteca estándar. Se configura con un archivo .env en la raíz del repo
(copia .env.example a .env y edítalo). Las variables de entorno, si existen, ganan:
  LLM_BASE_URL  http://localhost:11434/v1 (Ollama) · https://api.openai.com/v1 · https://api.anthropic.com/v1
  LLM_MODEL     qwen3:1.7b · gpt-6-luna · claude-haiku-5-5 · …
  LLM_API_KEY   la llave del proveedor (Ollama no la necesita)
"""
import json, os, re, time, urllib.error, urllib.request
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
BASE = os.environ.get('LLM_BASE_URL', 'http://localhost:11434/v1').rstrip('/')
MODEL = os.environ.get('LLM_MODEL', 'qwen3:1.7b')
KEY = os.environ.get('LLM_API_KEY', '')


def chat(mensajes, esquema=None, temperatura=None, max_tokens=4000):
    """Devuelve dict(texto, entrada, salida, segundos, avisos). `esquema`: JSON Schema de la respuesta.

    Cada proveedor acepta parámetros un poco distintos. Si uno los rechaza (error 400),
    se reintenta sin lo que rechazó y se deja un aviso, en lugar de tronar a mitad del lab:
    - temperatura: Claude 4.7 en adelante solo acepta 1; algunos modelos de razonamiento, ninguna.
    - max_tokens: algunos modelos de OpenAI piden max_completion_tokens.
    - json_schema: si no lo acepta, prueba json_object y luego texto libre.
    max_tokens es alto porque los modelos que razonan gastan tokens antes de contestar.
    """
    body = {'model': MODEL, 'messages': mensajes, 'max_tokens': max_tokens}
    if temperatura is not None:
        body['temperature'] = temperatura
    if esquema:
        body['response_format'] = {'type': 'json_schema',
                                   'json_schema': {'name': 'respuesta', 'strict': True, 'schema': esquema}}
    avisos, t0 = [], time.time()
    for _ in range(5):
        try:
            r = _post(body)
            break
        except urllib.error.HTTPError as e:
            if e.code != 400:
                raise
            msg = e.read().decode(errors='replace').lower()
            if 'temperature' in body and 'temperature' in msg:
                body.pop('temperature'); avisos.append(f'{MODEL} no acepta esa temperatura: uso la suya por defecto')
            elif 'max_tokens' in body and 'max_tokens' in msg:
                body['max_completion_tokens'] = body.pop('max_tokens')
            elif body.get('response_format', {}).get('type') == 'json_schema':
                body['response_format'] = {'type': 'json_object'}; avisos.append(f'{MODEL} no aceptó json_schema; pruebo json_object')
            elif 'response_format' in body:
                body.pop('response_format'); avisos.append(f'{MODEL} no aceptó formato JSON; pido texto libre')
            else:
                raise urllib.error.HTTPError(e.url, e.code, msg[:300], e.headers, None) from None
    else:
        raise RuntimeError('demasiados reintentos')
    u = r.get('usage') or {}
    texto = r['choices'][0]['message'].get('content') or ''
    texto = re.sub(r'<think>.*?</think>', '', texto, flags=re.S).strip()  # qwen3 en Ollama puede incluir su razonamiento
    return {'texto': texto, 'entrada': u.get('prompt_tokens', 0), 'salida': u.get('completion_tokens', 0),
            'segundos': time.time() - t0, 'avisos': avisos}


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
