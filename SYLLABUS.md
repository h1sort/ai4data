# Experto en IA Agéntica para Datos · Temario

12 sesiones en vivo · sábados · 3 horas · 6 módulos de 2 clases · un caso, un dataset, un proyecto final.

Versión web: [h1sort.com/ai4data](https://h1sort.com/ai4data/) · Inscripción: [Código Facilito](https://codigofacilito.com/programas/ia-datos)

---

## Principio rector: distancia con el curso introductorio

El curso gratuito (3 clases, sept 2026, repo `h1sort/intro-ai4data-class`) fue **mostrar y entender**. Este programa es **construir y medir**.

| | Curso introductorio | Este programa |
|---|---|---|
| Pregunta central | ¿Qué cambió en el rol de datos? | ¿Cómo construyo algo en lo que se pueda confiar, y cómo lo demuestro con números? |
| Datos | Encuestas en vivo, NYC Taxi, títulos de puesto | **Un caso nuevo y único** (abajo), con respuestas verificadas |
| Formato | Demo del profesor, el alumno mira | Laboratorio: cada sesión el alumno entrega algo que se usa en la siguiente |
| Conceptos | Se nombran (contexto, tools, evals, capa semántica) | Se implementan y se miden |
| Medición | "La respuesta se ve bien / está mal" | Exactitud, varianza, costo y latencia sobre un set de preguntas con respuesta conocida |

**Reglas para no repetir el curso gratuito:**
1. Ningún demo del curso gratuito se repite (ni la encuesta, ni NYC Taxi, ni el trap de propinas en efectivo, ni la historia de AI_CLASSIFY).
2. Lo que ya se explicó ahí se da por visto: se enlaza la grabación como **pre-requisito** y se repasa en máximo 10 minutos.
3. Cada sesión termina con un entregable que el alumno *construyó*, no con un concepto que *escuchó*.

### Pre-requisitos (grabaciones gratuitas)
- Clase 1: el rol de datos en 4 eras; contexto, tools y evals como palancas.
- Clase 2: OLTP vs OLAP, almacenamiento por filas vs columnas, ETL.
- Clase 3: qué es un LLM y cómo se entrena; qué es un agente; capa semántica y fecha de corte.

---

## El caso del programa

Una empresa ficticia (marketplace / pagos en LatAm) con datos sintéticos generados para el curso:

- **Tablas transaccionales:** clientes, pedidos, pagos, devoluciones, sucursales.
- **Texto libre:** tickets de soporte y reseñas (para clasificación y RAG).
- **Documentos internos:** un diccionario de métricas con definiciones *deliberadamente ambiguas o en conflicto* entre áreas (finanzas vs operaciones vs marketing), más políticas y manuales.
- **Set dorado:** ~100 preguntas de negocio con su respuesta verificada y su SQL de referencia. Una parte queda **oculta** para calificar el proyecto final.

Todo corre en local con DuckDB. En los módulos 4 y 6 se usa además un warehouse en la nube (Snowflake trial y/o Databricks Free Edition).

**Hilo conductor:** un *marcador* (scorecard) por alumno con cuatro números: exactitud sobre el set dorado, varianza entre corridas, costo por respuesta y latencia. Se crea en la sesión 1 y se actualiza en cada sesión. Al final, cada alumno puede mostrar cuánto mejoró su sistema y por qué.

---

## Módulo 1 · Fundamentos de LLMs para Análisis de Datos

*No es "cómo funciona un transformer" (eso fue la clase 3 gratuita). Es lo que un profesional de datos necesita saber del modelo cuando lo que sale es un número.*

### Sesión 1 · El LLM como instrumento de medición en datos
- Repaso de 10 min con enlace a la clase 3 gratuita.
- **Lab nanoGPT (45–60 min):** entrenar en CPU un modelo de caracteres mínimo (basado en nanoGPT de Andrej Karpathy) con datos generados para el curso:
  - cadenas de aritmética (`23+45=68`): acierta ~92% de las sumas, las que vio y las que no, falla todas las de tres cifras y nunca contesta "no sé";
  - filas de transacciones de un comercio ficticio: inventa filas que parecen reales y una de cada cuatro rompe alguna regla del negocio (fecha imposible, comercio inventado, total mal multiplicado).
  - Conclusión: el modelo aprendió *cómo se ven* los datos, no *qué es verdad*. Por eso el resto del programa trata de herramientas, SQL y evals.
  - Plan B: checkpoint pre-entrenado para quien tenga una laptop lenta.
- Tokens aplicados a datos: cómo se tokenizan números, fechas y tablas; cuántas filas caben realmente en una ventana de contexto y cuánto cuesta.
- No determinismo medido, no explicado: la misma pregunta 20 veces y cuántas respuestas distintas salen.
- Salidas estructuradas (JSON Schema) como contrato entre el modelo y el pipeline.
- **Lab:** primera corrida contra el set dorado.
- **Entregable:** mini-modelo entrenado + marcador v0 (exactitud, varianza, costo, latencia), que es la línea base del programa.

### Sesión 2 · Elegir modelo para datos: costo, contexto y exactitud
- Tres familias de modelos: frontera, pequeños/open-weights y **modelos de decisión (System One)**, cuyo primer ejemplo comercial es **Jev** de TypeSafe: responden preguntas tipadas (una etiqueta de una lista, un puntaje o una probabilidad), no generan texto.
- Regla práctica: si la pregunta es un juicio con categorías fijas, no necesitas un modelo generativo. Si es aritmética, conteo o fechas, ni uno ni otro: código.
- Tres formas de responder una pregunta de datos: el modelo calcula, el modelo escribe SQL o el modelo llama a una herramienta.
- Dónde corre el modelo: API pública, dentro del warehouse (Snowflake Cortex como laboratorio principal) o local. Implicaciones de privacidad y residencia de datos para industrias reguladas.
- Leer una tabla de precios: input, output, tokens de razonamiento, caché.
- Por qué el benchmark público no responde tu pregunta: comparar 3–4 modelos sobre el set dorado propio.
- **Lab:** mismas preguntas, varios modelos, en local y en Snowflake.
- **Entregable:** memo de selección de modelo con números (cuál, para qué tipo de pregunta y a qué costo).

## Módulo 2 · LLMs vía Chat y RAG para Datos

### Sesión 3 · LLMs vía Chat e Ingeniería de Prompts para Datos
- El prompt como artefacto versionado y probado, no como texto improvisado.
- Darle al modelo el esquema, el diccionario de datos y ejemplos (few-shot) para text-to-SQL desde el chat.
- Ambigüedad: cuando dos definiciones de "cliente activo" producen dos números, y el modelo debe preguntar en lugar de escoger.
- **Lab:** tres versiones de prompt, cada una medida en el marcador.
- **Entregable:** prompt v1 con su resultado documentado.

### Sesión 4 · Introducción a RAG con LLMs para Datos
- RAG recupera *definiciones y documentos*, no *datos*: por qué no se hace RAG sobre una tabla para sacar un total.
- Fragmentación (chunking) de diccionarios, manuales y tickets; embeddings; búsqueda híbrida.
- Medir la recuperación antes que la respuesta: ¿trajo el documento correcto?
- **Lab:** RAG sobre el diccionario de métricas y los tickets de soporte.
- **Entregable:** índice de recuperación + tasa de acierto de la recuperación.

## Módulo 3 · LLMs vía Copilotos y CLIs para Datos

### Sesión 5 · LLMs vía Copilotos en Entornos de Datos
- Copilotos en notebooks, editores SQL y proyectos de transformación (dbt o equivalente).
- Revisar un diff generado por IA en un modelo de datos: qué revisar, y qué tests automáticos lo atrapan.
- Cuándo el copiloto acelera y cuándo te hace más lento.
- **Lab:** construir los modelos analíticos del caso con un copiloto, con tests que deben pasar.
- **Entregable:** capa de modelos con tests en verde.

### Sesión 6 · LLMs vía CLIs y Agentes para Datos
- Ya no *usar* un agente (eso fue el curso gratuito): *configurarlo*.
- Jerarquía de contexto (AGENTS.md por directorio), skills y comandos para tareas de datos.
- Construir un servidor MCP propio para el warehouse: rol de solo lectura, límite de filas, enmascarado de PII, chequeo de frescura de datos.
- Permisos y hooks: qué puede ejecutar el agente y qué requiere aprobación.
- **Lab:** el agente del alumno contestando el set dorado solo con sus herramientas.
- **Entregable:** servidor MCP + configuración del agente, con el marcador actualizado.

## Módulo 4 · LLMs vía APIs y Productos en Data Warehouses

### Sesión 7 · LLMs vía APIs
- Llamar modelos desde Python dentro de un pipeline: salidas estructuradas, lotes (batch), concurrencia.
- Reintentos con presupuesto: límite de intentos, de tokens y de dinero por corrida.
- Caché y contabilidad de costos por pipeline.
- **LLM vs modelo de decisión:** la misma clasificación de tickets y reseñas con un LLM (salida estructurada) y con Jev. Se comparan exactitud, salidas inválidas o nulas, varianza entre corridas y costo por 1,000 filas. También se prueba lo que sus propios autores advierten: que las probabilidades cambian con el orden de las opciones y que el modelo es débil en aritmética, conteo y fechas.
- **Lab:** clasificar y extraer campos de los tickets y reseñas a columnas, con un tope de gasto.
- **Entregable:** pipeline de enriquecimiento con reporte de costo + la comparativa LLM vs Jev.

### Sesión 8 · Productos en Data Warehouses con LLMs
- Funciones de IA dentro del warehouse (Cortex AI SQL, `ai_query` de Databricks): cuándo convienen frente a tu propio pipeline.
- Text-to-SQL como producto (Cortex Analyst, Genie): configurarlo con un modelo semántico y medirlo contra el set dorado.
- Comparación honesta: producto del vendor vs lo que construiste en la sesión 6.
- **Lab:** el mismo set dorado contra el producto del warehouse.
- **Entregable:** comparativa producto vs propio (exactitud, costo, control).

## Módulo 5 · Evaluaciones (Evals) para Sistemas de IA en Datos

### Sesión 9 · Introducción a Evals para LLMs en Datos
- Del marcador informal a una suite de evals.
- Evaluar SQL por ejecución: comparar resultados, no el texto del query.
- Leer trazas y construir una taxonomía de errores (definición equivocada, join, filtro de fechas, datos viejos, alucinación).
- **Lab:** análisis de errores sobre las trazas de la sesión 6.
- **Entregable:** suite de evals + taxonomía de errores del sistema propio.

### Sesión 10 · Evals Avanzadas y Human–Model Eval para Datos
- LLM-as-judge para lo que no se compara por ejecución (explicaciones, resúmenes, clasificaciones).
- Calibrar el juez contra etiquetas humanas: acuerdo humano–modelo y cuándo no confiar en el juez.
- Prueba de consenso: varias interfaces o modelos, misma pregunta, contar respuestas distintas.
- Evals de regresión en CI: el cambio que baja la exactitud no se fusiona.
- **Lab:** etiquetado humano en grupo y calibración del juez.
- **Entregable:** juez calibrado + suite corriendo en CI.

## Módulo 6 · Flujos Avanzados, Equipos

### Sesión 11 · IA en Equipos de Datos y Warehouses Avanzados
- La capa semántica como código: métricas con dueño, versión y pruebas.
- Gobierno: control de acceso, linaje, auditoría de lo que hizo el agente.
- Operar en producción: SLAs de frescura, monitoreo de costo y de calidad, qué pasa cuando el modelo cambia de versión.
- Cómo se reorganiza un equipo de datos alrededor de verificar, no solo de producir.
- **Lab:** llevar el sistema propio al warehouse con capa semántica y monitoreo.
- **Entregable:** sistema listo para el proyecto final.

### Sesión 12 · Proyecto Final y Futuro de IA en Datos
- Presentaciones de proyectos.
- Calificación sobre la parte **oculta** del set dorado: nadie la vio, nadie la pudo ajustar.
- Futuro: qué cambia y qué no en el stack de datos, con predicciones que el grupo deja por escrito.

---

## Proyecto final

**Un analista agéntico verificable sobre el caso del programa.** Debe incluir:
1. Modelo elegido y justificado con números (M1).
2. Prompting y RAG sobre definiciones (M2).
3. Agente con herramientas propias y permisos (M3).
4. Al menos un pipeline de enriquecimiento con costo controlado, justificando por tarea si usa modelo de decisión, LLM o SQL (M4).
5. Suite de evals en CI y juez calibrado (M5).
6. Capa semántica y monitoreo (M6).

**Calificación:** exactitud sobre el set oculto, varianza, costo por respuesta y la calidad del análisis de errores. Gana claridad sobre el porqué, no solo el número.
