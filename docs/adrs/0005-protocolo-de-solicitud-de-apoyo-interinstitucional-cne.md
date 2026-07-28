# ADR-0005: Protocolo de Solicitud de Apoyo Interinstitucional del CNE

**Date:** 2026-07-27
**Status:** 2026-07-27 proposed
**Decisionmakers:** Firma Consultora Cenfosoft (G. Castro, D. Cárdenas, A. Cascante, R. Villareal)
**Supersedes:** —
**Relates to:** ADR-001 (Entorno Operativo On-Premise), ADR-0002 (Arquitectura Orientada al Análisis de Datos), ADR-0003 (Persistencia Políglota Distribuida), ADR-0004 (Control de Acceso Basado en Roles por Institución)
**RFP de referencia:** MGPSP-DGTIC-RFP-2026-007 (CivisGuard Analytics)

---

## Contexto

La **Comisión Nacional de Prevención de Riesgos y Atención de Emergencias (CNE)** es el ente rector nacional de la gestión de emergencias en Costa Rica (Ley 8488). Durante un evento de emergencia declarado, el CNE tiene la facultad legal de solicitar la movilización de recursos a las demás instituciones del Estado —Fuerza Pública, Bomberos, Cruz Roja, CCSS y Sistema 9-1-1— hacia un **área geográfica específica** definida por la naturaleza del evento.

Esta solicitud de apoyo no es un incidente convencional: es un acto de coordinación interinstitucional que debe:

- Originarse **exclusivamente** desde el rol `coordinador_cne` (ADR-0004).
- Especificar un **área geográfica** (polígono o radio de impacto) y el tipo de apoyo requerido.
- Propagarse de forma **confiable y auditable** a los sistemas de coordinación internos de cada institución destinataria.
- Garantizar que cada institución reciba la solicitud **exactamente una vez**, incluso ante fallos de conectividad parciales (RNF-05, ADR-001 on-premise).
- Quedar registrada de forma **inmutable** en la bitácora del sistema (RNF-04, ADR-0003).

El acoplamiento directo del CNE con los sistemas internos de cada institución crearía dependencias frágiles, incompatibles con la autonomía institucional establecida en ADR-0003 y con el estilo arquitectónico event-driven del SAD.

---

## Decision

Se adopta un **Protocolo de Solicitud de Apoyo Interinstitucional** basado en **publicación de eventos en el bus EDA (Apache Kafka)** con las siguientes reglas:

1. **Evento de dominio `SolicitudDeApoyoEmitida`.** Cuando el `coordinador_cne` emite una solicitud de apoyo, el microservicio de Coordinación CNE publica en Kafka un evento `SolicitudDeApoyoEmitida` con el siguiente esquema mínimo:

   ```json
   {
     "solicitud_id": "uuid",
     "emitida_por": "usuario_id (coordinador_cne)",
     "institucion_origen": "CNE",
     "instituciones_destino": ["BOMBEROS", "FUERZA_PUBLICA", "CRUZ_ROJA"],
     "area_geografica": { "tipo": "polígono", "coordenadas": ["..."] },
     "tipo_apoyo": "evacuacion|rescate|atencion_medica|...",
     "nivel_urgencia": "inmediata|alta|media",
     "timestamp": "ISO-8601",
     "incidente_asociado_id": "uuid (opcional)"
   }
   ```

2. **Topics particionados por institución destino.** El evento se publica en un topic Kafka particionado por `institucion_destino`, de modo que el Adaptador de Integración de cada institución consuma únicamente las solicitudes dirigidas a ella, sin acoplamiento entre instituciones.

3. **Adaptadores de integración por institución.** Cada institución cuenta con un microservicio **Adaptador de Integración** que:
   - Suscribe al topic de su partición.
   - Transforma el evento `SolicitudDeApoyoEmitida` al formato propietario del sistema de coordinación interno de la institución (si aplica).
   - Confirma la recepción mediante un evento de respuesta `SolicitudDeApoyoAcusada`.
   - Garantiza procesamiento **idempotente** (at-least-once delivery de Kafka + deduplicación por `solicitud_id`).

4. **Trazabilidad completa.** Cada evento —emisión, acuse, ejecución parcial, cierre— se registra en la bitácora inmutable (ADR-0003, Event Sourcing), con `solicitud_id` como correlador, permitiendo reconstruir el ciclo completo de la solicitud de apoyo en cualquier momento.

5. **Autorización delegada al ADR-0004.** Solo los usuarios con rol `coordinador_cne` pueden invocar la operación de emisión. El API Gateway valida el JWT antes de que la solicitud llegue al microservicio de Coordinación CNE.

6. **Operación offline-resiliente.** Si la conectividad de una institución destino está degradada (ADR-001, RNF-05), Kafka retiene el mensaje en el topic hasta que el Adaptador de esa institución reconecte y lo consuma, sin pérdida ni duplicación.

---

## Alternativas consideradas

### Alternativa A — Llamada directa REST del CNE a cada sistema institucional

El microservicio del CNE llama sincrónicamente la API de cada institución al emitir una solicitud.

**Razones del descarte:**
- **Acoplamiento temporal:** si el sistema de una institución está caído, la solicitud de apoyo falla para todas (efecto en cascada). Incompatible con RNF-01 y RNF-05.
- **Conocimiento implícito de los sistemas internos de cada institución:** viola la autonomía institucional de ADR-0003.
- **Sin garantía de entrega:** ante una caída parcial no hay mecanismo de reintento confiable sin lógica adicional compleja.
- **Escalabilidad lineal:** agregar una nueva institución requiere modificar el microservicio del CNE.

### Alternativa B — Notificación vía base de datos compartida (*Shared Database*)

El CNE escribe la solicitud en una tabla central y cada institución la lee desde su propio proceso.

**Razones del descarte:**
- Anti-patrón *Shared Database* explícitamente descartado en ADR-0003.
- Introduce acoplamiento estructural entre instituciones.
- No provee semántica de entrega garantizada ni particionamiento por institución.

### Alternativa C — Publicación de eventos en bus EDA por partición institucional (ELEGIDA)

Evento `SolicitudDeApoyoEmitida` en Kafka, topics particionados por institución destino, Adaptadores de Integración idempotentes, trazabilidad en Event Store. Satisface simultáneamente RNF-01, RNF-03, RNF-04, RNF-05, ADR-0003 y ADR-0004, y mantiene la autonomía institucional.

---

## Consequences

**Positivas:**
- El CNE está **desacoplado** de los sistemas internos de cada institución; agregar una nueva institución solo requiere desplegar un nuevo Adaptador de Integración sin modificar el microservicio del CNE.
- La solicitud de apoyo llega **exactamente a quien corresponde** gracias al particionamiento por `institucion_destino`, sin que instituciones no destinatarias puedan leerla (refuerza ADR-0004).
- Resiliencia ante conectividad degradada garantizada por la retención de mensajes en Kafka.
- Trazabilidad completa y auditable del ciclo de vida de cada solicitud de apoyo.

**Negativas / riesgos:**
- La consistencia del estado de la solicitud es **eventual**: el CNE no recibe una confirmación síncrona de que todas las instituciones ejecutaron la movilización. Se requiere un mecanismo de seguimiento de estado (saga de larga duración o *process manager*).
- Los Adaptadores de Integración deben implementarse y mantenerse por institución; si el sistema interno de una institución cambia su API, el adaptador debe actualizarse.
- La idempotencia en los adaptadores debe probarse rigurosamente para evitar duplicación de solicitudes ante reinicios del consumidor Kafka.
