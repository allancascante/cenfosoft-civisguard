# Apéndice — Declaración de Uso de Inteligencia Artificial Generativa

**Proyecto:** CivisGuard Analytics — Sistema Nacional de Coordinación de Emergencias e Incidentes Institucionales
**RFP:** MGPSP-DGTIC-RFP-2026-007
**Curso:** PSWE-04 — Diseño de Sistemas de Software — Maestría en Ingeniería de Software — CENFOTEC — Q02 2026
**Equipo Consultor (Cenfosoft):** Gustavo Castro · David Cárdenas · Allan Cascante · Randy Villareal
**Fecha:** 2026-07-19

---

## A.1 Marco ético de referencia

Si se usa alguna herramienta de Inteligencia Artificial para realizar este trabajo, el equipo consultor Cenfosoft se guía por las recomendaciones de **Cheng, Calhoun y Reedy (2025)**, en su artículo *"Artificial intelligence-assisted academic writing: recommendations for ethical use"* publicado en *Advances in Simulation*, 10:22, DOI https://doi.org/10.1186/s41077-025-00350-6.

De manera específica, el equipo adopta:

1. **Los tres criterios de Mann et al. (2024)** que Cheng et al. (2025) endosan: *(1)* verificación y garantía humana (*human vetting and guaranteeing*); *(2)* contribución humana sustancial (*substantial human contribution*); y *(3)* reconocimiento y transparencia (*acknowledgement and transparency*).
2. **Las cuatro preguntas del *Author Checklist* (Fig. 3 de Cheng et al., 2025)** que el equipo aplica al uso de IA en este SAD:
   - ¿He usado la IA de forma que las ideas, interpretaciones y análisis críticos primarios sean **propios**?
   - ¿He usado la IA de forma que los humanos **mantengan competencia** en las habilidades nucleares de investigación y escritura?
   - ¿He **verificado** que todo el contenido (y referencias) sea exacto, confiable y libre de sesgo?
   - ¿He **divulgado exactamente** cómo se usaron las herramientas de IA y en qué partes del manuscrito?
3. **Los tres *tiers* éticos (Fig. 2 de Cheng et al., 2025)** como criterio para clasificar cada uso de IA:
   - **Tier 1 (éticamente más aceptable):** reestructurar texto preexistente, gramática/ortografía, legibilidad, traducción.
   - **Tier 2 (éticamente contingente):** generar *outline*, resumir, mejorar claridad, *brainstorming* — su uso ético depende de los pasos que el autor tome con el contenido generado.
   - **Tier 3 (éticamente sospechoso):** redacción *de novo* sin contenido original en el *prompt*, interpretación de datos, revisión de literatura, verificación de plagio — se evita salvo supervisión humana crítica exhaustiva.

---

## A.2 Declaración de uso real de IA en este trabajo

El equipo Cenfosoft declara de forma **transparente y honesta** el uso de herramientas de Inteligencia Artificial Generativa (modelos LLM, ChatGPT/Chatly) en la elaboración del presente Documento de Arquitectura de Software (SAD), en cumplimiento del principio de *acknowledgement and transparency* (Cheng et al., 2025; Mann et al., 2024).

### A.2.1 Alcance del uso de IA

La IA se utilizó **exclusivamente** para los siguientes fines, todos dentro de los **Tier 1** y **Tier 2** de Cheng et al. (2025):

1. **Especificación de formatos y usos.** La IA asistió en la estructura formal de los ADRs (formato estándar *Context–Decision–Consequences*), de la sección arc42 #4 (Topología de Datos y Persistencia) y de la matriz comparativa, aplicando las plantillas de la industria (arc42, C4, ADR de Nygard).
2. **Comparaciones basadas en documentos previamente analizados por el equipo.** La IA asistió en la **comparación de competencias entre marcos** (p. ej., PostgreSQL vs. ClickHouse para OLAP; Kafka vs. BD relacional para *event store*; Redis vs. cache embebido) y en la **validación de convalidaciones entre marcos** (p. ej., que *database-per-service* es compatible con el Event-Driven Híbrido decidido en el Documento Base). En todos los casos, los documentos fuente (RFP, Documento Base, ADR-001/0002) fueron **leídos, comprendidos y analizados por el equipo humano previamente**; la IA sólo agrupó y formateó las comparaciones a partir del material que el equipo suministró.
3. **Revisión de los apuntes del equipo.** Basado en la estructura del trabajo del Documento Base, la IA se usó para **revisión de los apuntes** (ortografía, gramática, legibilidad, coherencia de referencias APA) — uso claramente dentro del **Tier 1** de Cheng et al. (2025).
4. **Agrupamiento y formato de los datos obtenidos.** La IA ayudó al equipo a **agrupar y dar formato** a los datos obtenidos del análisis (p. ej., organización de la tabla de mapeo *Bounded Context → Almacén → Tecnología → Modelo de consistencia*; organización de la matriz comparativa 20-criterios). El **análisis de los datos lo realizó el equipo humano**; la IA no interpretó datos ni generó conclusiones sustantivas.

### A.2.2 Lo que la IA **NO** hizo (contribución humana sustancial)

Conforme al segundo principio de Mann et al. (2024) —*substantial human contribution*— y a la pregunta *(1)* del *Author Checklist* de Cheng et al. (2025), el equipo declara que las siguientes tareas fueron **realizadas exclusivamente por los autores humanos**:

- **Análisis del dominio y descomposición en *Bounded Contexts*.** El equipo identificó los nueve *Bounded Contexts* a partir de la lectura del RFP (Procesos 1–3, glosario, RNF-03/RNF-06) y del *Ubiquitous Language* institucional.
- **Selección de la estrategia de persistencia (políglota distribuida vs. compartida).** La decisión técnica, su justificación y el análisis de *trade-offs* son **del equipo**. La IA sólo formateó la justificación previamente elaborada por los autores.
- **Mapeo de tecnologías por *Bounded Context*.** El equipo eligió PostgreSQL, Kafka, ClickHouse, Redis, PostGIS, Keycloak, SQLite, MinIO y Apicurio con base en su experiencia profesional (12+ años del arquitecto principal en sector bancario) y en la literatura citada. La IA no propuso tecnologías por sí sola; validó que las elecciones del equipo eran coherentes con la literatura (Kleppmann, 2017; Richardson, 2019; Newman, 2021).
- **Análisis del cumplimiento legal (Leyes 8968, 7410, 8488, 8228, 9986, Contraloría).** El equipo realizó el mapeo norma→requisito→tecnología; la IA sólo organizó la tabla.
- **Defensa de *trade-offs*.** Los argumentos de la matriz comparativa son del equipo.
- **Verificación de referencias.** El equipo verificó manualmente que cada referencia APA corresponde a una fuente real (no alucinada), conforme a la advertencia de Cheng et al. (2025) sobre referencias fabricadas por LLMs (Athaluri et al., 2023; Bhattacharyya et al., 2023).

### A.2.3 Verificación humana y control de alucinaciones

Conforme a la pregunta *(3)* del *Author Checklist* de Cheng et al. (2025) —exactitud, confiabilidad y ausencia de sesgo—, el equipo aplicó los siguientes **filtros críticos** a toda salida de IA:

1. **Filtro de fuentes.** Toda afirmación técnica sustantiva se respalda con una referencia APA verificada por el equipo (Evans, 2003; Fowler, 2015; Kleppmann, 2017; Newman, 2021; Richardson, 2019; Vernon, 2013; Cheng et al., 2025; Mann et al., 2024; leyes costarricenses consultadas en La Gaceta). Las afirmaciones no referenciadas se eliminaron o se marcaron como opinión del equipo.
2. **Filtro de coherencia con el Documento Base.** Toda salida de IA se contrastó con el ADR-001 (On-Premise), el ADR-0002 (Analítico/Asíncrono) y la "Estrategia de solución" del Documento Base (Event-Driven Híbrido sobre Kubernetes). Cualquier divergencia se corrigió.
3. **Filtro de cumplimiento del RFP.** Cada sección se validó contra las seis RNF y las siete restricciones legales del RFP MGPSP-DGTIC-RFP-2026-007.
4. **Filtro de idoneidad legal (Ley 9986).** El equipo verificó manualmente que cada tecnología propuesta es *open source* y sustituible, descartando opciones con *lock-in*.
5. **Filtro anti-alucinación de referencias.** Cada cita se verificó contra la fuente original (DOI, ISBN, La Gaceta); no se aceptaron referencias generadas por la IA sin verificación cruzada, conforme a la advertencia explícita de Cheng et al. (2025) sobre la "notoria falta de confiabilidad" de los LLM al citar referencias.

### A.2.4 Competencia humana mantenida

Conforme a la pregunta *(2)* del *Author Checklist* de Cheng et al. (2025) —mantener competencia humana en habilidades nucleares—, el equipo declara que:

- Los autores realizaron el **análisis arquitectónico, el razonamiento de *trade-offs* y la defensa técnica** sin delegar el pensamiento crítico a la IA.
- La IA se usó como **asistente de productividad** (formato, agrupamiento, comparación de marcos a partir de material ya analizado), no como sustituto del juicio arquitectónico.
- El equipo mantiene y refuerza su competencia en arquitectura de software, DDD, microservicios y persistencia políglota mediante la revisión manual y la validación crítica de cada salida de IA.

---

## A.3 Apéndice de prompts: indicaciones dadas a la IA y filtros críticos aplicados

Conforme a la indicación del curso: *"Si usa alguna herramienta de Inteligencia Artificial, debe incluir en un apéndice todas las indicaciones (prompts) que Ud. dio y los filtros críticos aplicados por Ud."*, se documentan a continuación los **cinco prompts principales** entregados a la IA y los **filtros críticos** que el equipo aplicó a cada salida. Cada prompt se clasifica según el *tier* ético de Cheng et al. (2025).

### Prompt 1 — Formato de ADR-003 (Tier 1: estructura/formato)

> **Prompt dado:**
> *"Actúa como arquitecto de software senior. Genera la estructura formal de un Architecture Decision Record (ADR) en formato estándar (Context–Decision–Alternatives Considered–Consequences–References APA), para documentar la decisión de usar persistencia políglota distribuida (database-per-service) en CivisGuard Analytics. La decisión debe alinearse con el ADR-001 (On-Premise) y el ADR-0002 (Analítico/Asíncrono) ya existentes, y cumplir las RNF-01 a RNF-06 del RFP MGPSP-DGTIC-RFP-2026-007. Considera al menos tres alternativas: BD compartida monolítica, BD por servicio uniforme, y políglota distribuida. Usa referencias APA verificables (Newman 2021, Fowler 2015, Richardson 2019, Kleppmann 2017, Evans 2003, Vernon 2013)."*

**Filtros críticos aplicados por el equipo:**
- Verificación de que las tres alternativas cubren el espacio de decisión (descartadas + elegida).
- Verificación de que cada consecuencia positiva/negativa se respalda en una RNF o ley específica.
- Verificación manual de cada referencia APA contra la fuente real (no alucinada).
- Reescritura humana del texto de justificación para reflejar el análisis propio del equipo.

### Prompt 2 — Comparación de tecnologías por Bounded Context (Tier 2: comparación entre marcos)

> **Prompt dado:**
> *"Tengo nueve Bounded Contexts para CivisGuard Analytics (Incidentes, Despacho y Recursos, Bitácora y Auditoría, Analítica y BI, Geoespacial, IAM, Sync Offline, Mensajería y Eventos, Archivos y Evidencia). Para cada uno, compárame las opciones de tecnología de persistencia open source más adecuadas al perfil de carga, justificando brevemente. Considera: PostgreSQL 16, Apache Kafka 3.7, ClickHouse 24, Redis/Valkey, PostGIS 3.4, Keycloak 24, SQLite 3, MinIO, Apicurio. La comparación debe cumplir la Ley 9986 (open source, sin lock-in) y las RNF-01 (disponibilidad), RNF-02 (despacho ≤90s, mapa de calor ≤20s), RNF-04 (bitácora inmutable ≥5 años) y RNF-05 (offline-first). Entrega una tabla Bounded Context → Tecnología → Modelo de consistencia → Patrón."*

**Filtros críticos aplicados por el equipo:**
- Validación de que la elección de cada tecnología corresponde al perfil de carga real del BC (no a preferencia de la IA).
- Validación de que Redis se reemplaza por Valkey para cumplimiento estricto de la Ley 9986 (ajuste del equipo).
- Validación de que la bitácora usa Event Sourcing (Kafka) y no un CRUD relacional (decisión del equipo).
- Revisión de que los modelos de consistencia (fuerte/eventual) son correctos por BC.
- Verificación de las licencias open source de cada tecnología.

### Prompt 3 — Matriz comparativa de estrategias de persistencia (Tier 2: agrupamiento/comparación)

> **Prompt dado:**
> *"Construye una matriz comparativa de 20 criterios (derivados de las RNF-01 a RNF-06 del RFP, de las Leyes 8968, 7410, 8488, 8228, 9986 y de la normativa de la Contraloría, más atributos de calidad: acoplamiento, escalabilidad, evolución tecnológica, alineación con ADR-0002 y con el estilo Event-Driven Híbrido) que contraste las tres alternativas de persistencia: A) BD compartida monolítica, B) BD por servicio uniforme, C) Políglota distribuida. Usa símbolos ✓✓/✓/△/✗ para idoneidad. Incluye una columna de 'Hecho/justificación' con referencia APA por fila. Termina con una conclusión que justifique la opción C."*

**Filtros críticos aplicados por el equipo:**
- Verificación de que los 20 criterios cubren todo el espectro del RFP y leyes (no sólo atributos técnicos).
- Revisión crítica de cada celda de la matriz: el equipo ajustó varias calificaciones (p. ej., el coste de infraestructura on-premise se calificó △ para C, no ✗, porque el trade-off se asume y mitiga).
- Validación de que la conclusión se deriva de los hechos de la matriz, no de una afirmación gratuita.
- Verificación de cada referencia APA.

### Prompt 4 — Revisión de apuntes, gramática y formato APA (Tier 1: revisión/legibilidad)

> **Prompt dado:**
> *"Revisa el siguiente texto del SAD (Sección 4 Topología de Datos y Persistencia) en busca de errores de gramática, ortografía, coherencia de referencias en estilo APA 7ª edición, y legibilidad técnica. No cambies el contenido sustantivo ni las decisiones técnicas; sólo corrige formato, gramática y consistencia de citas. Indica los cambios sugeridos con un diff."*

**Filtros críticos aplicados por el equipo:**
- Verificación de que la IA no alteró el contenido sustantivo ni las decisiones técnicas (Tier 1 estricto).
- Aceptación manual sólo de los cambios de formato/gramática; rechazo de cualquier modificación sustantiva.
- Re-verificación de cada referencia APA contra la fuente original.

### Prompt 5 — Generación del diagrama Mermaid de topología de datos (Tier 2: ilustración a partir de contenido del equipo)

> **Prompt dado:**
> *"Genera un diagrama Mermaid (flowchart TB) de la topología de datos de CivisGuard Analytics, con las siguientes capas: (1) Clientes (Web, Móvil Offline, Sistemas externos), (2) API Gateway + Keycloak, (3) Microservicios por Bounded Context (BC1 Incidentes … BC9 Archivos), (4) Bus EDA Apache Kafka como source of truth, (5) Capa de persistencia políglota (PostgreSQL para BC1/2/3/5/6/9, ClickHouse para BC4, Redis para BC2/5 cache, MinIO para BC9 objetos, SQLite para BC7 offline). Usa colores distintivos por tipo de nodo. Usa flechas sólidas para síncrono, flechas asíncronas para eventos Kafka, flechas CDC para Debezium/Kafka Connect. Incluye una leyenda con tipos de nodo y tipos de flujo, y una tabla de tecnologías con licencia open source."*

**Filtros críticos aplicados por el equipo:**
- Validación de que el diagrama refleja fielmente la topología decidida por el equipo (no una topología inventada por la IA).
- Verificación de que los flujos síncrono/asíncrono/CDC están tipados correctamente.
- Verificación de que la leyenda incluye tecnologías explícitas y licencias open source (cumplimiento Ley 9986).
- Revisión manual de la coherencia entre el diagrama Mermaid y la sección arc42 #4 del SAD.
- Generación complementaria del archivo `.drawio` editable por el equipo, para cumplimiento de la convención del Documento Base (draw.io como herramienta de edición C4).

---

## A.4 Resumen de clasificación por tier ético (Cheng et al., 2025)

| # | Uso de IA | Tier ético (Cheng et al., 2025) | ¿Requiere supervisión humana crítica? |
|:--:|---|:--:|:--:|
| 1 | Formato de ADR-003 | Tier 1 (estructura/formato) | Sí — verificación de referencias |
| 2 | Comparación de tecnologías por BC | Tier 2 (comparación entre marcos) | Sí — validación de elecciones técnicas |
| 3 | Matriz comparativa 20 criterios | Tier 2 (agrupamiento/comparación) | Sí — revisión crítica de cada celda |
| 4 | Revisión de apuntes, gramática, APA | Tier 1 (revisión/legibilidad) | Sí — rechazo de cambios sustantivos |
| 5 | Diagrama Mermaid de topología | Tier 2 (ilustración a partir de contenido del equipo) | Sí — validación de fidelidad al diseño |

**Conclusión de la clasificación:** ningún uso de IA se ubica en el **Tier 3** (éticamente sospechoso: redacción *de novo*, interpretación de datos, revisión de literatura). El equipo **no** usó la IA para interpretar datos, generar conclusiones sustantivas, ni redactar secciones completas sin contenido original en el *prompt*. La interpretación de datos y el análisis arquitectónico fueron realizados por el equipo humano, conforme a la pregunta *(1)* del *Author Checklist* de Cheng et al. (2025).

---

## A.5 Declaración final

El equipo Cenfosoft declara que el uso de IA en este trabajo fue **asistencial, transparente y acotado a tareas de formato, comparación entre marcos, agrupamiento de datos y revisión de legibilidad**, siempre dentro de los *tiers* éticamente aceptables de Cheng et al. (2025), con verificación humana de cada salida y con preservación de la competencia y el juicio arquitectónico del equipo. La IA **no** generó ideas primarias, **no** interpretó datos, **no** tomó decisiones técnicas por sí sola y **no** sustituyó el análisis crítico de los autores. Todas las referencias citadas fueron verificadas contra fuentes reales para prevenir alucinaciones, conforme a la advertencia explícita de Cheng et al. (2025) y de Athaluri et al. (2023).

---

## A.6 Referencias (APA 7ª ed.)

- Athaluri, S. A., Manthena, S. V., Kesapragada, V., Yarlagadda, V., Dave, T., & Duddumpudi, R. T. S. (2023). Exploring the boundaries of reality: Investigating the phenomenon of artificial intelligence hallucination in scientific writing through ChatGPT references. *Cureus*, *15*(4), e37432. https://doi.org/10.7759/cureus.37432
- Bhattacharyya, M., Miller, V. M., Bhattacharyya, D., & Miller, L. E. (2023). High rates of fabricated and inaccurate references in ChatGPT-generated medical content. *Cureus*, *15*(5), e39238. https://doi.org/10.7759/cureus.39238
- Cheng, A., Calhoun, A., & Reedy, G. (2025). Artificial intelligence-assisted academic writing: Recommendations for ethical use. *Advances in Simulation*, *10*(22). https://doi.org/10.1186/s41077-025-00350-6
- Mann, S. P., Vazirani, A. A., Mateo, A., Earp, B. D., Minssen, T., Cohen, I. G., et al. (2024). Guidelines for ethical use and acknowledgement of large language models in academic writing. *Nature Machine Intelligence*, *6*, 1272–1274. https://doi.org/10.1038/s42256-024-00910-x
- Evans, E. (2003). *Domain-Driven Design: Tackling Complexity in the Heart of Software*. Addison-Wesley.
- Fowler, M. (2015, 25 de marzo). *Microservices: A definition of this new architectural term*. https://martinfowler.com/articles/microservices.html
- Kleppmann, M. (2017). *Designing Data-Intensive Applications*. O'Reilly Media.
- Newman, S. (2021). *Building Microservices* (2.ª ed.). O'Reilly Media.
- Richardson, C. (2019). *Microservices Patterns*. Manning Publications.
- Vernon, V. (2013). *Implementing Domain-Driven Design*. Addison-Wesley.
- Asamblea Legislativa de Costa Rica. (2011). *Ley N.° 8968, Ley de Protección de la Persona frente al Tratamiento de sus Datos Personales*. La Gaceta N.° 103.
- Asamblea Legislativa de Costa Rica. (2018). *Ley N.° 9986, Ley de la Contratación Pública*. La Gaceta N.° 97.

