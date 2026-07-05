# 2. Arquitectura Orientada al Analisis de Datos

Date: 2026-07-05

## Status

2026-07-05 proposed

## Context

El sistema propuesto coexiste con los sistemas críticos de control de emergencias y despacho que ya operan de forma independiente en cada entidad de respuesta (Bomberos, Cruz Roja, Comisión Nacional de Emergencias - CNE, y el Sistema 9-1-1). Estas instituciones requieren inmediatez absoluta en sus operaciones diarias.

Sin embargo, el objetivo de nuestra solución no es el despacho en tiempo real ni la gestión operativa inmediata de incidentes, sino actuar como un núcleo centralizador que reciba información de todas estas fuentes para facilitar la coordinación interinstitucional, la planeación a mediano/largo plazo y la optimización de la respuesta estatal ante emergencias.

## Decision

Se ha decidido diseñar el sistema bajo un enfoque puramente analítico y asíncrono (Business Intelligence / Data Analytics), estableciendo un desacoplamiento total de los sistemas operativos de despacho de cada institución.

La ingesta de datos se realizará mediante procesos programados o por lotes (ETL/ELT), aceptando que el sistema operará con una ventana de retraso tolerable (por ejemplo, actualizaciones horarias o diarias). El sistema no procesará telemetría ni despacho en tiempo real.

## Consequences

**Aspectos Positivos (Beneficios)**
- Cero Impacto en la Operación Crítica: Al no exigir sincronía ni respuestas en milisegundos, las consultas analíticas pesadas del sistema propuesto no afectarán el rendimiento ni la estabilidad de los sistemas de despacho locales de las instituciones (esenciales para salvar vidas).

- Flexibilidad en la Ingesta de Datos: Permite diseñar interfaces de integración más sencillas y robustas. Si una institución sufre una caída temporal en su sistema, los datos pendientes pueden enviarse en el siguiente lote sin romper el flujo de trabajo general.

- Foco en el Valor Estratégico: La arquitectura se optimizará para el modelado de datos, la generación de reportes consolidados, tableros de control (dashboards) y mapas de calor que ayuden a la CNE y demás entes a planificar recursos y detectar patrones de riesgo.

**Aspectos Negativos (Riesgos o Limitaciones)**
- Latencia en la Toma de Decisiones: El sistema no puede ser utilizado para coordinar tácticas en el segundo exacto en que ocurre un incidente mayor; su uso es estrictamente estratégico y posterior al evento inmediato.

- Complejidad en la Homogeneización de Datos: Cada entidad (9-1-1, Bomberos, etc.) maneja formatos, codificaciones y estructuras de datos nativas muy distintas. El motor de transformación del sistema deberá hacer un esfuerzo considerable para estandarizar los datos bajo un mismo modelo conceptual estatal.