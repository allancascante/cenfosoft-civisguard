# ADR-003: Arquitectura de Persistencia Políglota Distribuida (Database-per-Service)

**Date:** 2026-07-19
**Status:** 2026-07-19 proposed
**Decisionmakers:** Firma Consultora Cenfosoft (G. Castro, D. Cárdenas, A. Cascante, R. Villareal)
**Supersedes:** —
**Relates to:** ADR-001 (Entorno Operativo On-Premise), ADR-0002 (Arquitectura Orientada al Análisis de Datos)
**RFP de referencia:** MGPSP-DGTIC-RFP-2026-007 (CivisGuard Analytics)

---

## Contexto

El sistema **CivisGuard Analytics** debe operar, conforme al **ADR-001**, sobre infraestructura **on-premise** del Ministerio de Gobernación, Policía y Seguridad Pública, con acceso restringido exclusivamente por VPN y descartando cualquier proveedor de nube pública o híbrida externa. El **ADR-0002** definió un enfoque **analítico/asíncrono** (ETL/ELT) desacoplado de los sistemas de despacho en tiempo real de cada institución, mientras que la "Estrategia de solución" del Documento Base estableció un **Estilo Arquitectónico Macro: Event-Driven Híbrido sobre Kubernetes**, combinando:

1. Un **pipeline ETL orientado a eventos** (ingesta de incidentes, mapa de calor, analítica territorial, bitácora), con workers *stateless* que escalan automáticamente según el tamaño de la cola.
2. **Microservicios de coordinación operativa** (despacho de recursos, protocolos de emergencia del CNE, sincronización *offline* de unidades de campo), cada uno con su propio ciclo de despliegue y comunicación vía el bus de eventos.

El RFP MGPSP-DGTIC-RFP-2026-007 impone restricciones que **condicionan directamente** la estrategia de persistencia:

| Restricción (RFP / Ley) | Implicación directa sobre la persistencia |
|---|---|
| **RNF-01** Disponibilidad 24/7/365; indisponibilidad no planificada ≤ 2 min | Requiere redundancia de almacenes, *failover* automático y RPO/RTO agresivos por servicio. |
| **RNF-02** Despacho crítico ≤ 90 s; mapa de calor visible ≤ 20 s; picos de 250 incidentes/min | La capa operacional (despacho) exige escrituras ACID de baja latencia; la capa analítica exige lecturas agregadas sub-segundo → perfiles de carga opuestos que un único almacén no optimiza simultáneamente. |
| **RNF-03** Visibilidad diferenciada por institución y perfil | Requiere aislamiento de datos por *tenant* institucional y control de acceso a nivel de fila (RLS) o particionamiento físico por institución. |
| **RNF-04** Bitácora operativa inmutable, irrefutable; retención ≥ 5 años (Contraloría) | Exige un almacén *append-only* / WORM con integridad verificable, fuera del alcance de un CRUD convencional. |
| **RNF-05** Operación en conectividad degradada; sincronización posterior sin pérdida ni duplicación | Requiere almacenamiento local en unidades de campo (*offline-first*) con resolución de conflictos al reconectar (idempotencia / CRDT / *outbox*). |
| **RNF-06** Autonomía institucional + vista nacional consolidada + Protocolo de Emergencia Nacional del CNE | Cada institución debe poder configurar su propio sub-modelo sin acoplarse al esquema de las demás. |
| **Ley 9986** — prohibición de dependencia tecnológica de un único proveedor comercial | Toda tecnología de persistencia debe ser *open source* con soporte multi-vendor/community. |
| **Ley 8968** — principios de finalidad, proporcionalidad y seguridad | Datos personales cifrados, minimización por institución, trazabilidad de acceso. |
| **Normativa Contraloría** — retención histórica ≥ 5 años | Estrategia de *archival* y exportación inmutable de largo plazo. |

El Documento Base ya declaró, entre sus principios de diseño, **"persistencia políglota distribuida"** y **"patrones tácticos de Domain-Driven Design (DDD)"**; el presente ADR formaliza y justifica técnicamente esa declaración inicial.

---

## Decisión

Se adopta una **arquitectura de persistencia políglota distribuida** bajo el principio **database-per-service** (Newman, 2021; Fowler, 2015; Richardson, 2019), con las siguientes reglas obligatorias:

1. **Propiedad exclusiva del dato.** Cada microservicio —alineado a un *Bounded Context* de DDD (Evans, 2003; Vernon, 2013)— es propietario **exclusivo** de su(s) almacén(es) de datos. Ningún microservicio accede por JDBC/ODBC/SQL directo al almacén de otro; la integración entre servicios se realiza **únicamente** mediante eventos publicados en el bus EDA (Apache Kafka) y APIs contractuales (REST/gRPC sobre el bus).

2. **Políglota por contexto.** La tecnología de cada almacén se selecciona según el perfil de carga del *Bounded Context* que sirve (OLTP transaccional, OLAP analítico, geoespacial, documental *append-only*, clave-valor cache, *event store*, almacenamiento de objetos), no por uniformidad organizacional.

3. **Open source y sustituibilidad.** Todas las tecnologías de persistencia elegidas son *open source* con comunidad activa y soporte multi-vendor, para cumplir la **Ley 9986**. Se excluyen motores propietarios con *lock-in* irrescindible.

4. **Consistencia eventual por defecto, fuerte dentro del agregado.** Las transacciones distribuidas entre microservicios se resuelven con el patrón **Saga** (orchestration/choreography) y **Outbox Pattern**; la consistencia fuerte (ACID) se garantiza **únicamente dentro del agregado DDD** y de su almacén propietario. La bitácora (RNF-04) usa **Event Sourcing** para garantizar inmutabilidad e irrefutabilidad.

5. **Aislamiento institucional.** Los almacenes que sirven a múltiples instituciones implementan **Row-Level Security (RLS)** y/o particionamiento por `institucion_id`.

6. **Offline-First en el borde.** Las unidades de campo operan contra un almacén local embebido (SQLite) que se sincroniza con el microservicio correspondiente mediante eventos idempotentes y resolución de conflictos basada en marcas de tiempo vectoriales / CRDT.

---

## Alternativas consideradas

### Alternativa A — Base de datos compartida monolítica (*Single Shared Database*)

Un único motor relacional centralizado, con un esquema único compartido por todos los módulos.

**Razones del descarte:**
- **Acoplamiento estructural:** cualquier cambio de esquema solicitado por una institución (RNF-06) impacta el esquema compartido y a las demás instituciones. Anti-patrón *Shared Database* (Newman, 2021; Fowler, 2015).
- **Punto único de fallo:** la RNF-01 exige indisponibilidad ≤ 2 min; un único almacén es el peor caso de *blast radius* (Kleppmann, 2017).
- **Mezcla de perfiles de carga opuestos:** las escrituras OLTP de despacho (RNF-02) compiten con las consultas OLAP agregadas del mapa de calor, degradando ambos (Kleppmann, 2017; Richardson, 2019).
- **Violación de la RNF-03:** la visibilidad diferenciada se vuelve frágil al depender exclusivamente de RLS sobre un esquema único.
- **Escalabilidad vertical limitada** por la restricción on-premise del ADR-001 (sin elasticidad de nube).

### Alternativa B — *Database-per-service* con tecnología uniforme (sin políglota)

Cada microservicio posee su propia base de datos, pero **todas** utilizan el mismo motor relacional (p. ej., PostgreSQL).

**Razones del descarte:**
- **Suboptimización por contexto:** la bitácora inmutable (RNF-04) se modela de forma antinatural en un CRUD relacional, cuando un *event store* o un almacén *append-only* resuelve el requisito por construcción.
- **OLAP sobre OLTP:** la analítica territorial y el mapa de calor (RNF-02, ≤20 s) exigen escaneos columnares de millones de incidentes; un motor OLTP requiere vistas materializadas e índices redundantes, multiplicando el coste de infraestructura on-premise.
- **Geoespacial de alto volumen:** el mapa de calor y la reincidencia por zona se benefician de extensiones geoespaciales nativas (PostGIS) y caches (Redis GEO), no de un único motor uniforme.
- **No aprovecha el *event store* nativo del bus EDA** ya decidido (Kafka).

### Alternativa C — **Persistencia políglota distribuida (ELEGIDA)**

*Database-per-service* + tecnología especializada por *Bounded Context*, integración exclusivamente por eventos/APIs, consistencia eventual entre servicios y fuerte dentro del agregado, todo *open source*. Ver *Consequences* y la Sección 4 del SAD para el mapeo almacén→*bounded context*→tecnología→modelo de consistencia. Esta alternativa **maximiza** el cumplimiento simultáneo de las seis RNF y las siete restricciones legales del RFP.

---

## Consequences

### Aspectos positivos (beneficios)

- **RNF-01 (Disponibilidad):** el fallo de un almacén afecta sólo a su *bounded context* (*blast radius* acotado); cada almacén se replica con su propio mecanismo de *failover* (streaming replication en PostgreSQL, réplicas en Kafka, Sentinel en Redis, erasure coding en MinIO), posibilitando RPO/RTO por servicio alineados a ≤ 2 min.
- **RNF-02 (Velocidad):** la separación OLTP (PostgreSQL) / OLAP columnar (ClickHouse) / cache geoespacial (Redis GEO) permite optimizar cada ruta: escritura ACID < 50 ms para despacho, lectura agregada < 200 ms para mapa de calor, propagación del cache < 20 s vía CDC (Kafka Connect).
- **RNF-03 (Visibilidad diferenciada):** el aislamiento físico por *bounded context* + RLS por `institucion_id` + particionamiento garantiza que Bomberos no pueda acceder al esquema policial ni la CCSS al táctico, por construcción.
- **RNF-04 (Bitácora inmutable):** el *event store* (Kafka, retención ≥ 5 años) + proyección *append-only* implementan la inmutabilidad e irrefutabilidad por diseño.
- **RNF-05 (Offline-First):** SQLite embebido + sincronización idempotente por eventos permite operar sin conectividad y reconciliar sin duplicación.
- **RNF-06 (Autonomía + vista consolidada):** cada institución configura su sub-modelo sin acoplamiento; la vista consolidada se construye en el DW (ClickHouse) a partir de eventos publicados.
- **Ley 9986:** todas las tecnologías (PostgreSQL, ClickHouse, MongoDB, Redis/Valkey, Kafka, MinIO, PostGIS, SQLite) son *open source* sin *lock-in*.
- **Escalabilidad independiente** sobre Kubernetes, coherente con el estilo Event-Driven Híbrido.

### Aspectos negativos (riesgos y trade-offs)

- **Complejidad operacional:** seis tecnologías de persistencia aumentan la curva de aprendizaje. **Mitigación:** stack observabilidad unificado (Prometheus + Grafana), *backup* unificado, runbooks por almacén, DBA polígota o 2 especializados.
- **Consistencia eventual entre servicios:** las transacciones que cruzan *bounded contexts* no son ACID globales. **Mitigación:** patrón **Saga** (orquestada para despacho, coreografiada para analítica) + **Outbox Pattern** + idempotencia.
- **Costos de infraestructura on-premise superiores** a una solución uniforme. **Mitigación:** justificado por el cumplimiento de RNF-01 (riesgo de vida) y RNF-04 (riesgo legal); el coste del *blast radius* de una BD compartida supera el coste marginal.
- **Gobernanza de datos:** requiere *schema registry* versionado. **Mitigación:** Apicurio/Confluent Schema Registry con *backward compatibility* obligatoria.
- **Latencia de la vista consolidada:** ventana de latencia entre el evento operativo y su disponibilidad en el DW. **Mitigación:** coherente con el ADR-0002; el cache Redis absorbe la latencia del mapa de calor (< 20 s vía CDC).

---

## Cumplimiento normativo

| Normativa | Cumplimiento por diseño |
|---|---|
| **Ley 9986** | Stack 100 % open source: PostgreSQL (PostgreSQL License), ClickHouse (Apache 2.0), Redis/Valkey (BSD), Apache Kafka (Apache 2.0), MinIO (AGPLv3), PostGIS (GPL), SQLite (public domain). Ningún componente presenta *lock-in* comercial. |
| **Ley 8968** | Cifrado en reposo por almacén (LUKS + TDE); minimización por institución vía RLS; trazabilidad de acceso en la bitácora inmutable. |
| **Normativa Contraloría** | Event store Kafka con retención ≥ 5 años + proyección *append-only* + *archival* a MinIO (Object Lock WORM) para exportación inmutable. |
| **Leyes 8488 / 8228 / 7410 / CCSS** | Aislamiento por *bounded context* impide el cruce de información entre instituciones salvo el marco legal explícito; el CNE accede a recursos consolidados pero no a datos internos. |

---

## Referencias (APA 7ª ed.)

- Evans, E. (2003). *Domain-Driven Design: Tackling Complexity in the Heart of Software*. Addison-Wesley.
- Fowler, M. (2015, 25 de marzo). *Microservices: A definition of this new architectural term*. https://martinfowler.com/articles/microservices.html
- Kleppmann, M. (2017). *Designing Data-Intensive Applications*. O'Reilly Media.
- Newman, S. (2021). *Building Microservices* (2.ª ed.). O'Reilly Media.
- Richardson, C. (2019). *Microservices Patterns*. Manning Publications.
- Vernon, V. (2013). *Implementing Domain-Driven Design*. Addison-Wesley.
- Asamblea Legislativa de Costa Rica. (2018). *Ley N.° 9986, Ley de la Contratación Pública*. La Gaceta N.° 97.
- Asamblea Legislativa de Costa Rica. (2011). *Ley N.° 8968, Ley de Protección de la Persona frente al Tratamiento de sus Datos Personales*. La Gaceta N.° 103.
- Hruschka, P., & Starke, G. (2024). *arc42 — Template for architecture documentation and communication* (versión 8.2). https://arc42.org

