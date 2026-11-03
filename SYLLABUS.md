# Experto en IA Agéntica para Datos — Temario (borrador)

12 sesiones en vivo · sábados · 3 horas · 6 módulos de 2 clases · un caso, un dataset, un proyecto final.

> Estado: **borrador v1** para revisión con Código Facilito. Los títulos de los módulos se conservan como están publicados; lo que cambia es el enfoque de cada clase. La única propuesta de cambio de título es en el Módulo 1 (ver nota al final).

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

## Módulo 1 · Fundamentos Teóricos de LLMs en Análisis de Datos

*No es "cómo funciona un transformer" (eso fue la clase 3 gratuita). Es lo que un profesional de datos necesita saber del modelo cuando lo que sale es un número.*

### Sesión 1 · El LLM como instrumento de medición
- Repaso de 10 min con enlace a la clase 3 gratuita.
- Tokens aplicados a datos: cómo se tokenizan números, fechas y tablas; por qué un LLM suma mal; cuántas filas caben realmente en una ventana de contexto y cuánto cuesta.
- No determinismo medido, no explicado: la misma pregunta 20 veces y cuántas respuestas distintas salen.
- Salidas estructuradas (JSON Schema) como contrato entre el modelo y el pipeline.
- Tres formas de responder una pregunta de datos: el modelo calcula, el modelo escribe SQL, o el modelo llama a una herramienta. Cuándo usar cada una.
- **Lab:** primera corrida contra el set dorado.
- **Entregable:** marcador v0 (exactitud, varianza, costo, latencia), que es la línea base del programa.

### Sesión 2 · Elegir modelo para datos: costo, contexto, exactitud y dónde corre
- Familias de modelos: frontera, pequeños, open-weights; razonamiento vs no razonamiento.
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
- **Lab:** clasificar y extraer campos de los tickets y reseñas a columnas, con un tope de gasto.
- **Entregable:** pipeline de enriquecimiento con reporte de costo.

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
4. Al menos un pipeline de enriquecimiento con costo controlado (M4).
5. Suite de evals en CI y juez calibrado (M5).
6. Capa semántica y monitoreo (M6).

**Calificación:** exactitud sobre el set oculto, varianza, costo por respuesta y la calidad del análisis de errores. Gana claridad sobre el porqué, no solo el número.

---

## Nota sobre la corrección del Módulo 1

Problemas que veo en el Módulo 1 publicado (por confirmar cuál señaló Código Facilito):

1. **Títulos duplicados.** El título del módulo ("Fundamentos Teóricos de LLMs en Análisis de Datos") y el de la clase 1 ("Fundamentos Teóricos de LLMs en Datos") son casi iguales.
2. **Vendor en un módulo de fundamentos.** "…para Datos, en Snowflake" ata una clase de fundamentos a un producto; ningún otro título del temario nombra un vendor.
3. **Traslape con el curso gratuito.** "Fundamentos teóricos de LLMs" es justo la primera hora de la clase 3 gratuita (transformer, entrenamiento, qué es un agente).

Propuesta de títulos:
- Módulo 1: **Fundamentos de LLMs para Análisis de Datos** (se quita "Teóricos": el módulo es práctico).
- Clase 1: **El LLM como instrumento de medición en datos**.
- Clase 2: **Elegir modelo para datos: costo, contexto y exactitud** (Snowflake se queda como laboratorio, no en el título).
