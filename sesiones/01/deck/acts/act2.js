// Acts 3–5 · Tokens, no determinismo y salidas estructuradas.
// Token splits: lab-tokens/tokens.mjs (gpt-tokenizer, o200k_base and cl100k_base agree on every example).
(() => {
  const tk = (parts) => parts.map((p) => `<span class="tk">${p}</span>`).join('');
  const EX = [
    ['1234567', ['123', '456', '7'], 'agrupa de izquierda a derecha, no por miles'],
    ['2026-11-21', ['202', '6', '-', '11', '-', '21'], 'el año queda partido'],
    ['$1,249.50', ['$', '1', ',', '249', '.', '50'], 'seis piezas para un monto'],
    ['CLI-0164', ['CLI', '-', '016', '4'], 'el ID tampoco es una unidad'],
  ];

  Deck.css(`
    #s-tokens-numeros .tn { list-style: none; padding: 0; margin: 10px 0 0; }
    #s-tokens-numeros .tn li { display: grid; grid-template-columns: 420px 1fr 520px; align-items: center; padding: 20px 0; border-top: 2px solid var(--hair); }
    #s-tokens-numeros .tn li:last-child { border-bottom: 2px solid var(--hair); }
    #s-tokens-numeros .src { font-family: var(--mono); font-size: 44px; }
    #s-tokens-numeros .d { font-size: 28px; color: var(--dim); }
    .tk { display: inline-block; font-family: var(--mono); font-size: 38px; border: 2px solid var(--faint); border-radius: 10px; padding: 2px 14px; margin: 4px 8px 4px 0; }
    .tk:nth-child(even) { border-color: var(--accent); color: var(--accent); }

    #s-tokens-fila .row { display: flex; flex-wrap: wrap; font-family: var(--mono); margin: 6px 0 44px; max-width: 1680px; }
    #s-tokens-fila .row .tk { font-size: 28px; padding: 0 8px; margin: 3px 4px 3px 0; }
    #s-tokens-fila .tf { display: grid; grid-template-columns: repeat(3, 1fr); gap: 48px; }
    #s-tokens-fila .tf > div { border-top: 3px solid var(--fg); padding-top: 20px; }
    #s-tokens-fila .tf .big { font-size: 104px; font-weight: 500; letter-spacing: -0.03em; line-height: 1; margin: 14px 0 10px; }
    #s-tokens-fila .tf .d { font-size: 28px; color: var(--dim); line-height: 1.3; }

    #s-tokens-costo .f { font-size: 72px; font-weight: 500; letter-spacing: -0.02em; line-height: 1.2; margin: 40px 0 50px; }
    #s-tokens-costo .f .op { color: var(--faint); font-weight: 400; margin: 0 22px; }
    #s-tokens-costo .live { display: grid; grid-template-columns: repeat(3, 1fr); gap: 40px; }
    #s-tokens-costo .live > div { border: var(--stroke) dashed var(--faint); border-radius: 18px; padding: 24px 30px; }
    #s-tokens-costo .live .k { font-family: var(--mono); font-size: 22px; letter-spacing: 0.18em; text-transform: uppercase; color: var(--dim); }
    #s-tokens-costo .live .v { font-size: 64px; font-weight: 500; margin-top: 10px; }

    #s-no-sumes .ns { display: grid; grid-template-columns: 1fr 1fr; gap: 64px; margin-top: 20px; }
    #s-no-sumes .ns > div { border-top: 3px solid var(--fg); padding-top: 22px; }
    #s-no-sumes .ns h3 { font-size: 46px; font-weight: 500; margin: 12px 0 20px; letter-spacing: -0.02em; }
    #s-no-sumes pre.code { font-size: 26px; }

    .lab2 { display: grid; grid-template-columns: 1.2fr 1fr; gap: 56px; }
    .lab2 pre.code { font-size: 24px; line-height: 1.55; }
    .lab2 pre.code .c { color: var(--faint); }
    .lab2 .r .t-small { color: var(--dim); }

    #s-veinte .vq { font-size: 58px; font-weight: 500; letter-spacing: -0.02em; line-height: 1.15; max-width: 1500px; margin: 26px 0 50px; }
    #s-veinte .vgrid { display: grid; grid-template-columns: repeat(10, 120px); gap: 18px; }
    #s-veinte .vgrid span { height: 86px; border: 2px dashed var(--faint); border-radius: 12px; display: flex; align-items: center; justify-content: center; font-family: var(--mono); font-size: 26px; color: var(--faint); }

    #s-medir-varianza .mv { display: grid; grid-template-columns: repeat(3, 1fr); gap: 44px; margin-top: 20px; }
    #s-medir-varianza .mv > div { border: var(--stroke) solid var(--faint); border-radius: 18px; padding: 30px 32px; }
    #s-medir-varianza .mv .k { font-family: var(--mono); font-size: 22px; letter-spacing: 0.18em; text-transform: uppercase; color: var(--accent); }
    #s-medir-varianza .mv h3 { font-size: 46px; font-weight: 500; margin: 16px 0 14px; }
    #s-medir-varianza .mv p { font-size: 29px; color: var(--dim); line-height: 1.35; margin: 0; }
    #s-medir-varianza .mv .f { font-family: var(--mono); font-size: 26px; color: var(--fg); margin-top: 18px; }

    #s-temperatura-cero .tc { display: grid; grid-template-columns: repeat(3, 1fr); gap: 48px; margin-top: 30px; }
    #s-temperatura-cero .tc > div { border-top: 3px solid var(--fg); padding-top: 20px; }
    #s-temperatura-cero .tc .big { font-size: 120px; font-weight: 500; letter-spacing: -0.03em; line-height: 1; margin: 14px 0 10px; }
    #s-temperatura-cero .tc .d { font-size: 29px; color: var(--dim); line-height: 1.3; }
    #s-temperatura-cero .why { margin-top: 56px; font-size: 36px; max-width: 1560px; line-height: 1.35; }

    #s-contrato .ct { display: grid; grid-template-columns: 1fr 1fr; gap: 64px; }
    #s-contrato pre.code { font-size: 24px; line-height: 1.5; }
    #s-contrato pre.code .k { color: var(--accent); }

    #s-forma-verdad .fv { display: grid; grid-template-columns: 1fr 1fr; gap: 64px; margin-top: 30px; }
    #s-forma-verdad .fv > div { border-top: 3px solid var(--fg); padding-top: 22px; }
    #s-forma-verdad .fv .k { font-size: 120px; font-weight: 500; line-height: 1; }
    #s-forma-verdad .fv h3 { font-size: 50px; font-weight: 500; margin: 18px 0 16px; }
    #s-forma-verdad .fv p { font-size: 31px; color: var(--dim); line-height: 1.35; margin: 0; }
  `);

  Deck.act(3, 'Tokens', [
    {
      id: 'tokens-numeros',
      title: 'Cómo ve un número',
      time: 360,
      particles: { shape: 'grid', opacity: 0.12 },
      html: `
        <div class="t-label">Antes de "pensar", el modelo parte el texto en tokens</div>
        <h2 class="t-title">Cómo ve un número un LLM</h2>
        <ul class="tn">
          ${EX.map(([s, parts, d], i) => `<li${i ? ` data-step="${i}"` : ''}><span class="src">${s}</span><span>${tk(parts)}</span><span class="d">${d}</span></li>`).join('')}
        </ul>
        <div class="cite foot">Tokenizadores o200k_base y cl100k_base (gpt-tokenizer). Mismos cortes en ambos.</div>`,
      notes: `
        <p>Nuestro modelito veía carácter por carácter. Los modelos de verdad no: antes de procesar, parten el texto en tokens. Esto es lo que ve un modelo con los tokenizadores de OpenAI, medido con el script del lab.</p>
        <p>Un millón doscientos treinta y cuatro mil quinientos sesenta y siete: 123, 456, 7. Agrupa de izquierda a derecha en bloques de tres, que no coinciden con los miles como los escribimos.</p>
        <p class="dir">[Clic por cada fila.]</p>
        <p>La fecha: el año 2026 queda partido en 202 y 6. Un monto con signo de pesos son seis piezas. Y el ID del cliente tampoco es una unidad: CLI, guion, 016 y 4. Para el modelo, todo esto es texto que se parece a otro texto. Ahora, una fila completa.</p>`,
    },
    {
      id: 'tokens-fila',
      title: 'Una fila ≈ 37 tokens',
      time: 300,
      particles: { shape: 'grid', opacity: 0.12 },
      html: `
        <div class="t-label">Una fila del caso · o200k_base</div>
        <h2 class="t-title" style="margin-bottom:28px">Cada fila cuesta ~37 tokens</h2>
        <div class="row">${tk(['TX', '-', '003', '04', ',', '202', '6', '-', '01', '-', '01', ',', 'CLI', '-', '004', '9', ',A', 'bar', 'ro', 'tes', '·La', '·Esper', 'anza', ',T', 'DD', ',', '1', ',', '43', '.', '00', ',', '43', '.', '00', '↵'])}</div>
        <div class="tf">
          <div data-step="1"><div class="t-label">Ventana de 200 mil</div><div class="big">~5,400</div><div class="d">filas, sin contar instrucciones ni respuesta</div></div>
          <div data-step="2"><div class="t-label">Ventana de 1 millón</div><div class="big">~26,800</div><div class="d">filas, en el mejor caso</div></div>
          <div data-step="3"><div class="t-label">1 millón de filas</div><div class="big accent">37 M</div><div class="d">tokens: no cabe en ninguna ventana</div></div>
        </div>`,
      notes: `
        <p>Esta es la primera fila del caso que vamos a usar hoy: treinta y seis tokens, y estos son los cortes reales. Fíjense en la coma: se pega a la A de Abarrotes y a la T de TDD. Medí las quinientas filas: de 34 a 40, 37 en promedio.</p>
        <p class="dir">[Clic.]</p>
        <p>Con una ventana de contexto de 200 mil tokens caben unas cinco mil cuatrocientas filas, sin contar las instrucciones ni la respuesta.</p>
        <p class="dir">[Clic.]</p>
        <p>Con una ventana de un millón, unas veintiséis mil ochocientas, en el mejor caso. Y ya vimos en el curso gratuito que mientras más llenas la ventana, peor atención.</p>
        <p class="dir">[Clic.]</p>
        <p>Una tabla de un millón de filas, que en un banco es una tabla chica, son 37 millones de tokens. No cabe. Y aunque cupiera, hay que pagarla.</p>`,
    },
    {
      id: 'tokens-costo',
      title: 'Lo que cuesta',
      time: 240,
      particles: { shape: 'one', opacity: 0.15 },
      html: `
        <div class="t-label">Costo de meter una tabla al contexto · en vivo</div>
        <div class="f">filas <span class="op">×</span> 37 <span class="op">×</span> precio por token <span class="op">×</span> preguntas</div>
        <div class="live">
          <div><div class="k">Filas</div><div class="v">100,000</div></div>
          <div data-step="1"><div class="k">Precio · millón de tokens de entrada</div><div class="v">$ ___</div></div>
          <div data-step="2"><div class="k">Por cada pregunta</div><div class="v accent">$ ___</div></div>
        </div>`,
      notes: `
        <p>La cuenta es simple: filas por 37 tokens por precio por token, y eso por cada pregunta que hagas, porque cada pregunta vuelve a mandar la tabla.</p>
        <p class="dir">[Clic. Abrir en vivo la página de precios del proveedor que más use la sala y llenar el precio de entrada por millón de tokens. No lo pongo en la lámina porque cambia cada mes.]</p>
        <p class="dir">[Clic. Calcular en voz alta: 100 mil filas son 3.7 millones de tokens; por el precio de entrada.]</p>
        <p>Y eso es por pregunta. Si el equipo hace cien preguntas al día, multipliquen. Entonces, si no le vamos a pasar la tabla y no sabe sumar, ¿qué hacemos?</p>`,
    },
    {
      id: 'no-sumes',
      title: 'El modelo no suma',
      time: 180,
      particles: { shape: 'two', opacity: 0.14 },
      html: `
        <div class="t-label">Regla práctica</div>
        <h2 class="t-title">No le pidas que sume. Pídele que escriba cómo sumar.</h2>
        <div class="ns">
          <div><div class="t-label faint">El modelo calcula</div><h3>92% en la tabla de sumas</h3><p class="t-small dim">Y paga por cada fila que lee.</p></div>
          <div data-step="1"><div class="t-label accent">El modelo escribe código</div><h3>La base de datos suma</h3>
<pre class="code">SELECT metodo, AVG(total)
FROM transacciones
GROUP BY metodo;</pre></div>
        </div>`,
      notes: `
        <p>La regla práctica que se van a llevar: no le pidan al modelo que sume. Pídanle que escriba cómo sumar.</p>
        <p>Si el modelo calcula, ya vimos lo que pasa: un modelo que se equivoca una de cada trece sumas y que paga por cada fila que lee.</p>
        <p class="dir">[Clic.]</p>
        <p>Si el modelo escribe la consulta, la base de datos hace la suma, que para eso existe, y el modelo solo lee el resultado. Las tres formas de contestar una pregunta de datos, y cuándo usar cada una, son el tema de la sesión dos. Ahora, cuatro minutos con sus propios datos.</p>`,
    },
    {
      id: 'lab-tokens',
      title: 'Lab · tokens',
      time: 240,
      label: 'Lab · 4 min',
      particles: { shape: 'swarm', opacity: 0.12 },
      html: `
        <div class="t-label">Lab · 4 minutos</div>
        <h2 class="t-title">Tokeniza tus propios datos</h2>
        <div class="lab2">
<pre class="code">cd ai4data/sesiones/01/lab-tokens
npm install
node tokens.mjs tu_archivo.csv

<span class="c"># o sin archivo: los ejemplos de la lámina</span>
node tokens.mjs</pre>
          <div class="r">
            <p class="t-small">Usa un CSV de tu trabajo, <strong>sin datos personales</strong>.</p>
            <p class="t-small">Anota en el chat: tokens por fila y cuántas filas caben en 200 mil.</p>
            <p class="t-small">¿Qué columna es la más cara?</p>
          </div>
        </div>`,
      notes: `
        <p>Cuatro minutos. Corran el script con un CSV de su trabajo, sin datos personales, o sin archivo para repetir los ejemplos. Pongan en el chat cuántos tokens les cuesta una fila y cuántas filas les caben en doscientos mil.</p>
        <p class="dir">[Leer dos o tres resultados del chat. Suele salir que las columnas de texto libre y los IDs largos son las más caras.]</p>
        <p>Ya sabemos cómo ve un número. Ahora, ¿contesta lo mismo dos veces?</p>`,
    },
  ]);

  Deck.act(4, 'No determinismo', [
    {
      id: 'veinte',
      title: 'La misma pregunta 20 veces',
      time: 300,
      particles: { shape: 'swarm', opacity: 0.2 },
      html: `
        <div class="t-label">Experimento</div>
        <h2 class="t-title" style="margin-bottom:0">La misma pregunta, 20 veces</h2>
        <p class="vq">"Con estas 50 transacciones, ¿cuál es el ticket promedio de los pagos con tarjeta?"</p>
        <div class="vgrid">${Array.from({ length: 20 }, (_, i) => `<span>${String(i + 1).padStart(2, '0')}</span>`).join('')}</div>`,
      notes: `
        <p>Segundo experimento. Una sola pregunta, veinte veces, mismo modelo, mismo contexto: cincuenta transacciones en el prompt y la pregunta "¿cuál es el ticket promedio de los pagos con tarjeta?"</p>
        <p>Antes de correrlo, noten que la pregunta tiene una trampa: ¿tarjeta es solo crédito, o crédito y débito? En los datos hay TDC y TDD. Esa ambigüedad la vamos a ver en las respuestas.</p>
        <p class="dir">[Correr el script en vivo con el modelo de la sala e ir llenando la cuadrícula en voz alta. Si no hay red, usar la corrida grabada del ensayo.]</p>
        <p class="dir">[Verdad por código en estas 50 filas: 1,606.24 si tarjeta es TDC y TDD; 985.36 si es solo TDC.]</p>`,
    },
    {
      id: 'medir-varianza',
      title: 'Cómo se mide',
      time: 300,
      particles: { shape: 'split', opacity: 0.15 },
      html: `
        <div class="t-label">Cómo se mide la varianza</div>
        <h2 class="t-title">Tres números por pregunta</h2>
        <div class="mv">
          <div><div class="k">01</div><h3>Distintas</h3><p>¿Cuántas respuestas diferentes dio en 20 corridas?</p><div class="f">ideal: 1</div></div>
          <div data-step="1"><div class="k">02</div><h3>Consenso</h3><p>¿Qué fracción coincide con la respuesta más común?</p><div class="f">ideal: 100%</div></div>
          <div data-step="2"><div class="k">03</div><h3>Exactitud</h3><p>¿Qué fracción coincide con la verdad, calculada con código?</p><div class="f">ideal: 100%</div></div>
        </div>`,
      notes: `
        <p>¿Cómo lo convertimos en número? Tres medidas por pregunta.</p>
        <p>Distintas: cuántas respuestas diferentes dio en veinte corridas. Lo ideal es una.</p>
        <p class="dir">[Clic.]</p>
        <p>Consenso: qué fracción coincide con la respuesta más común. Esta es la que va a su marcador como varianza.</p>
        <p class="dir">[Clic.]</p>
        <p>Y exactitud: cuántas coinciden con la verdad, que calculamos con código, no con otro modelo. Ojo: el consenso alto no implica exactitud. Un modelo puede contestar veinte veces lo mismo y estar veinte veces mal. Y ahora la pregunta obvia: ¿por qué varía si la temperatura es cero?</p>`,
    },
    {
      id: 'temperatura-cero',
      title: 'Temperatura 0',
      time: 240,
      particles: { shape: 'ring', opacity: 0.15 },
      html: `
        <div class="t-label">Thinking Machines Lab · septiembre 2025</div>
        <h2 class="t-title">Ni a temperatura 0 contesta siempre lo mismo</h2>
        <div class="tc">
          <div><div class="big">1,000</div><div class="d">corridas del mismo prompt</div></div>
          <div data-step="1"><div class="big accent">80</div><div class="d">respuestas distintas</div></div>
          <div data-step="2"><div class="big">78</div><div class="d">veces salió la más común</div></div>
        </div>
        <p class="why" data-step="3">La causa: el servidor agrupa tu petición con las de otros, y el resultado cambia con el tamaño del grupo. Lo puedes arreglar en tu servidor; en una API ajena, <em>se mide</em>.</p>
        <div class="cite foot">Thinking Machines Lab, "Defeating Nondeterminism in LLM Inference", sep 2025 · Qwen3-235B</div>`,
      notes: `
        <p>La respuesta corta es que la temperatura no es la única fuente de variación. Thinking Machines publicó un experimento en septiembre de 2025: mil veces el mismo prompt, a temperatura cero, en un modelo abierto grande.</p>
        <p class="dir">[Clic.]</p>
        <p>Salieron ochenta respuestas distintas.</p>
        <p class="dir">[Clic.]</p>
        <p>La más común apareció 78 veces de mil.</p>
        <p class="dir">[Clic.]</p>
        <p>La causa: el servidor junta tu petición con las de otros usuarios en un lote, y algunos cálculos dan resultados ligeramente distintos según el tamaño del lote, que depende de la carga del servidor. Ellos lo arreglaron y las mil respuestas salieron idénticas, pero eso es en su servidor. Cuando usan una API de terceros, no lo controlan: lo miden. Eso hacemos ahora.</p>`,
    },
    {
      id: 'lab-veinte',
      title: 'Lab · 20 corridas',
      time: 480,
      label: 'Lab · 8 min',
      particles: { shape: 'swarm', opacity: 0.12 },
      html: `
        <div class="t-label">Lab · 8 minutos</div>
        <h2 class="t-title">Corre tus 20</h2>
        <div class="lab2">
<pre class="code"><span class="c"># cualquier API compatible con OpenAI:
# OpenAI, OpenRouter u Ollama local</span>
export LLM_BASE_URL=http://localhost:11434/v1
export LLM_MODEL=qwen3:4b
export LLM_API_KEY=...   <span class="c"># si aplica</span>

cd ai4data/sesiones/01/lab-veinte
python veinte.py --n 20</pre>
          <div class="r">
            <p class="t-small">Anota en el chat: modelo, distintas, consenso y exactitud.</p>
            <p class="t-small">Corre otra vez con <span class="mono">--temperatura 0</span>. ¿Cambia?</p>
          </div>
        </div>`,
      notes: `
        <p>Ocho minutos. El script funciona con cualquier API compatible con OpenAI: OpenAI directo, OpenRouter, o un modelo local con Ollama si no quieren gastar. Corran veinte veces y pongan en el chat su modelo y sus tres números.</p>
        <p class="dir">[Al terminar, armar en voz alta una tabla con 4 o 5 modelos de la sala. Lo usual: modelos distintos, consensos distintos, y alguien con consenso alto y exactitud baja.]</p>
        <p>Ya medimos si contesta lo mismo. Ahora, que conteste en una forma que una máquina pueda leer.</p>`,
    },
  ]);

  Deck.act(5, 'Salidas estructuradas', [
    {
      id: 'contrato',
      title: 'El contrato',
      time: 360,
      particles: { shape: 'grid', opacity: 0.12 },
      html: `
        <div class="t-label">Salidas estructuradas</div>
        <h2 class="t-title">La respuesta con contrato</h2>
        <div class="ct">
          <div>
            <p class="t-body dim" style="margin-top:0">El modelo ya no escribe prosa: llena un esquema. Si no cumple, la API lo rechaza.</p>
            <ul class="bullets t-small" style="margin-top:36px">
              <li data-step="1">La <strong>respuesta</strong> viene en su campo, sin prosa alrededor.</li>
              <li data-step="2">La <strong>definición</strong> que usó queda escrita.</li>
              <li data-step="3">Tu pipeline lo lee sin expresiones regulares.</li>
            </ul>
          </div>
<pre class="code">{
  <span class="k">"valor"</span>:      { "type": ["number", "string"] },
  <span class="k">"unidad"</span>:     { "enum": ["MXN", "conteo",
                          "%", "texto"] },
  <span class="k">"definicion"</span>: { "type": "string" },
  <span class="k">"supuestos"</span>:  { "type": "array",
                  "items": { "type": "string" } }
}</pre>
        </div>
        <div class="cite foot">JSON Schema · json-schema.org · OpenAI, "Introducing Structured Outputs in the API", ago 2024</div>`,
      notes: `
        <p>Tercera herramienta del día: las salidas estructuradas. En lugar de dejar que el modelo conteste en prosa, le damos un esquema, en JSON Schema, y la API garantiza que la respuesta lo cumple.</p>
        <p class="dir">[Clic.]</p>
        <p>La respuesta viene en su propio campo, sin un párrafo alrededor. Es número o texto porque algunas preguntas piden un nombre, un ID o una fecha; la unidad dice cuál.</p>
        <p class="dir">[Clic.]</p>
        <p>La definición que usó queda escrita: si dijo que tarjeta es TDC más TDD, lo dice ahí, y podemos auditarlo.</p>
        <p class="dir">[Clic.]</p>
        <p>Y su pipeline lo lee directo, sin expresiones regulares para sacar el número de un párrafo. Pero cuidado con lo que esto garantiza.</p>`,
    },
    {
      id: 'forma-verdad',
      title: 'Forma no es verdad',
      time: 240,
      particles: { shape: 'two', opacity: 0.15 },
      html: `
        <div class="t-label">Lo que garantiza y lo que no</div>
        <h2 class="t-title">Forma no es verdad</h2>
        <div class="fv">
          <div><div class="k good">✓</div><h3>Garantiza la forma</h3><p>Siempre un número, siempre las columnas correctas, siempre parseable.</p></div>
          <div data-step="1"><div class="k bad">✗</div><h3>No garantiza la verdad</h3><p>Nuestro modelo de sumas ya contestaba siempre con un número. Las filas inventadas tenían siete columnas perfectas.</p></div>
        </div>`,
      notes: `
        <p>Las salidas estructuradas garantizan la forma: siempre un número, siempre parseable.</p>
        <p class="dir">[Clic.]</p>
        <p>No garantizan la verdad. Y ya lo vimos hoy: nuestro modelito de sumas tenía la salida más estructurada del mundo, siempre un número, y fallaba el cien por ciento de las sumas de tres cifras. Las filas inventadas tenían siete columnas perfectas. La forma es necesaria para medir; la verdad la medimos aparte. Ocho minutos para ponerle contrato a su pregunta.</p>`,
    },
    {
      id: 'lab-esquema',
      title: 'Lab · esquema',
      time: 480,
      label: 'Lab · 8 min',
      particles: { shape: 'swarm', opacity: 0.12 },
      html: `
        <div class="t-label">Lab · 8 minutos</div>
        <h2 class="t-title">La misma pregunta, con esquema</h2>
        <div class="lab2">
<pre class="code">cd ai4data/sesiones/01/lab-veinte
python veinte.py --n 20 --esquema</pre>
          <div class="r">
            <p class="t-small">¿Bajó el número de respuestas distintas?</p>
            <p class="t-small">¿Qué <span class="mono">definicion</span> usó para "tarjeta"? ¿Siempre la misma?</p>
            <p class="t-small">¿Subió la exactitud, o solo el consenso?</p>
          </div>
        </div>`,
      notes: `
        <p>Repitan las veinte corridas con la bandera de esquema. Tres preguntas: ¿bajaron las respuestas distintas? ¿Qué definición de tarjeta usó, y fue siempre la misma? ¿Subió la exactitud o solo el consenso?</p>
        <p class="dir">[Si un modelo local no soporta esquemas, el script lo dice y cae a modo JSON simple.]</p>
        <p>Con esto tenemos todas las piezas. Vamos a su marcador.</p>`,
    },
  ]);
})();
