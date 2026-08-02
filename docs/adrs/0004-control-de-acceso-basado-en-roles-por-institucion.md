# ADR-0004: Control de Acceso Basado en Roles por Institución (RBAC Institucional)

**Date:** 2026-07-27
**Status:** 2026-07-27 proposed
**Decisionmakers:** Firma Consultora Cenfosoft (G. Castro, D. Cárdenas, A. Cascante, R. Villareal)
**Supersedes:** —
**Relates to:** ADR-001 (Entorno Operativo On-Premise), ADR-0002 (Arquitectura Orientada al Análisis de Datos), ADR-0003 (Persistencia Políglota Distribuida)
**RFP de referencia:** MGPSP-DGTIC-RFP-2026-007 (CivisGuard Analytics)

---

## Contexto

**CivisGuard Analytics** integra seis instituciones del Estado costarricense —Sistema 9-1-1, Fuerza Pública, CCSS, Cruz Roja, Bomberos y CNE— cada una con operadores propios que deben poder reportar y consultar incidentes dentro de su ámbito institucional **sin acceder a los incidentes de otras instituciones**.

El RFP MGPSP-DGTIC-RFP-2026-007 y el marco legal vigente imponen restricciones que condicionan directamente el modelo de seguridad:

| Restricción | Implicación sobre control de acceso |
|---|---|
| **RNF-03** Visibilidad diferenciada por institución y perfil | Un operador de Bomberos no puede ver incidentes de Fuerza Pública ni viceversa. |
| **Ley 8968** — principio de finalidad y proporcionalidad | Los datos personales de un incidente solo pueden ser procesados por quien tiene competencia legal sobre ese incidente. |
| **Ley 8228** — Ley General de Policía | La información operativa de la Fuerza Pública es de acceso restringido a personal autorizado. |
| **ADR-0003** — Aislamiento institucional con RLS | El almacén ya prevé Row-Level Security por `institucion_id`; el modelo de autenticación/autorización debe alimentar ese filtro de forma confiable. |

La arquitectura event-driven definida en el SAD establece microservicios independientes por dominio; sin un modelo de autorización centralizado y portable entre servicios, cada microservicio debería reimplementar su propia lógica de seguridad, generando fragmentación e inconsistencias.

---

## Decision

Se adopta un modelo de **Control de Acceso Basado en Roles (RBAC)** con **alcance institucional obligatorio**, bajo las siguientes reglas:

1. **Identidad federada con claim de institución.** Cada usuario autenticado recibe un *JSON Web Token* (JWT) firmado que incluye obligatoriamente los claims `institucion_id` y `rol`. El servicio de autenticación (Identity Provider) es la única fuente de verdad sobre la identidad.

2. **Roles por institución.** Los roles se definen en el contexto de una institución; no existen roles globales salvo los del CNE (ver ADR-0005). Los roles base son:

   | Rol | Capacidades |
   |---|---|
   | `operador_institucional` | Reportar incidentes y consultar incidentes **de su propia institución**. |
   | `supervisor_institucional` | Todo lo anterior + visualizar estadísticas agregadas de su institución. |
   | `coordinador_cne` | Ver incidentes de **todas** las instituciones en modo lectura + emitir solicitudes de apoyo (ver ADR-0005). |
   | `admin_plataforma` | Gestión de usuarios y configuración; sin acceso a datos operativos de incidentes. |

3. **Enforcement en el gateway y en la capa de datos.** La autorización se aplica en dos capas:
   - **API Gateway:** valida el JWT y rechaza tokens inválidos o expirados antes de que la solicitud llegue a cualquier microservicio.
   - **Microservicio / base de datos:** aplica **Row-Level Security (RLS)** usando el `institucion_id` extraído del JWT, alineado con ADR-0003, de modo que incluso una brecha en el gateway no expone datos de otras instituciones.

4. **Principio de mínimo privilegio.** Un usuario solo puede acceder a las operaciones y datos estrictamente necesarios para su rol. El reporte de un incidente solo incluye los datos del ámbito de la institución que lo origina.

5. **Auditoría de accesos.** Todo intento de acceso —exitoso o rechazado— se registra en la bitácora inmutable definida en ADR-0003, incluyendo `usuario_id`, `institucion_id`, `recurso`, `operacion` y `timestamp`. Retención mínima de 5 años conforme a la normativa de la Contraloría.

6. **Tecnología open source.** El Identity Provider debe ser *open source* (p. ej. Keycloak) para cumplir la restricción de independencia tecnológica de la **Ley 9986**.

---

## Alternativas consideradas

### Alternativa A — Control de acceso ad-hoc por microservicio

Cada microservicio implementa su propia lógica de autorización sin un modelo centralizado.

**Razones del descarte:**
- Duplicación de lógica de seguridad en cada servicio; alta probabilidad de inconsistencias entre implementaciones.
- Imposible auditar de forma centralizada (viola RNF-03 y Ley 8968).
- El RLS de ADR-0003 no tiene un claim confiable y portable de donde extraer `institucion_id`.

### Alternativa B — ACL (Access Control List) por recurso

Listas de control de acceso por cada incidente o recurso individual.

**Razones del descarte:**
- No escala para el volumen de incidentes del sistema (250 incidentes/min, RNF-02); gestionar ACL individuales es operacionalmente inviable.
- No responde al modelo mental del dominio, donde el acceso se determina por la pertenencia institucional, no por el recurso individual.

### Alternativa C — RBAC con alcance institucional (ELEGIDA)

Roles definidos por institución, JWT con claims verificables, enforcement en dos capas (gateway + RLS), auditoría centralizada, Identity Provider open source. Satisface simultáneamente RNF-03, Ley 8968, Ley 8228, ADR-0003 y el principio de mínimo privilegio.

---

## Consequences

**Positivas:**
- Separación clara entre autenticación (quién eres) y autorización (qué puedes hacer y sobre qué institución).
- El RLS de ADR-0003 opera con un `institucion_id` confiable proveniente del JWT, sin lógica adicional en cada microservicio.
- Auditoría centralizada y verificable para efectos legales y de Contraloría.
- Modelo extensible: agregar una nueva institución implica crear sus usuarios y asignarles el rol correspondiente, sin cambios de código.

**Negativas / riesgos:**
- El Identity Provider se convierte en un componente crítico; requiere alta disponibilidad y estrategia de *failover* alineada con RNF-01.
- La gestión de roles y permisos debe operarse con disciplina; una asignación incorrecta de `coordinador_cne` a un usuario no autorizado comprometería la visibilidad interinstitucional.
