# Sección 4 — Topología de Datos y Persistencia

**Proyecto:** CivisGuard Analytics — Sistema Nacional de Coordinación de Emergencias e Incidentes Institucionales
**RFP:** MGPSP-DGTIC-RFP-2026-007
**Marco de documentación:** arc42 (Hruschka & Starke, 2024), Sección 4
**ADRs asociados:** ADR-001 (On-Premise), ADR-0002 (Analítico/Asíncrono), **ADR-003 (Persistencia políglota distribuida)**
**Fecha:** 2026-07-19
**Elaborado por:** Firma Consultora Cenfosoft

---

## 4.1 Introducción y alineación con las decisiones previas

Esta sección formaliza la **Topología de Datos y Persistencia** de CivisGuard Analytics, alineándose con tres decisiones arquitectónicas previas:

1. **ADR-001 — Entorno Operativo On-Premise.** Todos los almacenes se despliegan dentro del perímetro del Ministerio de Gobernación, en servidores físicos propios, accesibles exclusivamente por VPN. No se usa ningún servicio gestionado de nube pública.
2. **ADR-0002 — Arquitectura Orientada al Análisis de Datos.** El sistema tiene una **doble naturaleza**: (a) un núcleo **analítico/asíncrono** (ETL/ELT, BI, mapas de calor) con ventana de latencia tolerable, y (b) **microservicios de coordinación operativa** (despacho, protocolos del CNE, sincronización *offline*) con exigencias de baja latencia. La topología debe **servir a ambas naturalezas sin que una degradue a la otra**.
3. **ADR-003 — Persistencia políglota distribuida.** Cada microservicio, alineado a un *Bounded Context* de DDD, es propietario exclusivo de su(s) almacén(es) y selecciona la tecnología óptima. La integración es **exclusivamente por eventos** (Kafka) y APIs contractuales.

> **Coherencia con el RFP.** La topología resuelve la tensión entre el RFP (despacho ≤ 90 s, mapa de calor ≤ 20 s) y el ADR-0002 (analítico/asíncrono) mediante el modelo **híbrido** del Documento Base: la capa operacional usa almacenes OLTP de baja latencia, y la capa analítica usa almacenes OLAP/cache alimentados por eventos.

---

## 4.2 Justificación: políglota distribuida vs. base de datos compartida

La decisión detallada se documenta en el **ADR-003** y se contrasta visualmente en el anexo **`matriz-comparativa-persistencia.md`**. Síntesis:

- **No se usa una base de datos compartida** porque (a) acoplaría los esquemas de las seis instituciones (violando RNF-06), (b) mezclaría perfiles OLTP/OLAP (violando RNF-02), (c) crearía un punto único de fallo con *blast radius* máximo (violando RNF-01), (d) modelaría antinaturalmente la bitácora inmutable (violando RNF-04) y (e) expondría todos los datos personales en un único esquema (aumentando el riesgo bajo Ley 8968).

- **Se usa una arquitectura de persistencia políglota distribuida** porque (a) aísla cada *bounded context* con su tecnología óptima, (b) permite consistencia fuerte dentro del agregado y eventual entre servicios (Sagas), (c) implementa la bitácora inmutable por diseño mediante *Event Sourcing*, (d) cumple la Ley 9986 con un *stack* 100 % *open source*, y (e) absorbe la naturaleza híbrida analítica/operativa del ADR-0002.

La matriz comparativa demuestra que esta opción **no incumple ningún criterio** del RFP y **satisface óptimamente 15 de 20 criterios**, frente a 9 incumplimientos de la BD compartida.

---

## 4.3 Topología por *Bounded Context*

CivisGuard Analytics se descompone en **nueve *Bounded Contexts***, cada uno propietario de su(s) almacén(es). La descomposición se deriva del análisis del dominio del RFP (Procesos 1–3, glosario, RNF-03 y RNF-06) y del *Ubiquitous Language* institucional.

### 4.3.1 Mapeo *Bounded Context* → Almacén → Tecnología → Modelo de consistencia

| # | *Bounded Context* | Responsabilidad | Tecnología (open source) | Consistencia | Patrón principal |
|:--:|---|---|---|:--:|---|
| **BC1** | **Incidentes** | Registro, clasificación, ciclo de vida, prioridad | **PostgreSQL 16** (particionado por `institucion_origen_id`) | Fuerte (ACID) | Repository, Aggregate `Incidente` |
| **BC2** | **Despacho y Recursos** | Asignación, tracking, SLA, ubicación de recursos | **PostgreSQL 16** + **Redis 7** (cache GEO, TTL 5 s) | Fuerte (ACID); eventual en cache | CQRS (escritura PG, lectura Redis) |
| **BC3** | **Bitácora y Auditoría** | Registro inmutable e irrefutable (RNF-04), retención ≥ 5 años | **Apache Kafka 3.7** (event store) + proyección *append-only* en **PostgreSQL** | Eventual (proyección); Kafka es verdad canónica | **Event Sourcing** + *Outbox* |
| **BC4** | **Analítica y BI** | Mapa de calor, reincidencia, reportes consolidados | **ClickHouse 24** (OLAP columnar) vía Kafka Connect (CDC) | Eventual (latencia s–min, coherente con ADR-0002) | CQRS (lado lectura) |
| **BC5** | **Geoespacial** | Mapa de calor operacional (≤ 20 s), zonas de riesgo | **PostGIS 3.4** + **Redis GEO** (cache incidentes activos) | Fuerte en PostGIS; eventual en cache | Repository geoespacial; índices GiST |
| **BC6** | **Identidad y Acceso** | Usuarios, roles, RBAC por institución, MFA | **Keycloak 24** (LDAP integrado) + **PostgreSQL** | Fuerte | RBAC + ABAC |
| **BC7** | **Sincronización Offline** | Almacenamiento local en campo, reconciliación (RNF-05) | **SQLite 3** (embebido) + **Kafka** (cola eventos pendientes) | Eventual con CRDT | *Offline-First*; *Outbox* idempotente |
| **BC8** | **Mensajería y Eventos** | Bus EDA — *source of truth*, *pub/sub* | **Apache Kafka 3.7** + **Apicurio Schema Registry** | Eventual; orden por partición | *Pub/Sub*; CDC (Debezium) |
| **BC9** | **Archivos y Evidencia** | Multimedia, exportaciones Contraloría, *archival* WORM | **MinIO** (Object Lock WORM) + **PostgreSQL** (metadatos) | Fuerte metadatos; inmutable objetos | Repository de objetos; versionado |

### 4.3.2 Justificación de cada selección tecnológica

**PostgreSQL 16** (BC1, BC2, BC3-proyección, BC5, BC6, BC9). Motor ACID *open source* (PostgreSQL License, BSD-like) con **RLS nativa**, particionamiento declarativo, PostGIS y replicación *streaming*. Se elige por: (a) Ley 9986 (sin *lock-in*); (b) RLS para RNF-03; (c) ACID para RNF-02; (d) replicación para RNF-01. Referencias: Kleppmann (2017), Richardson (2019).

**Apache Kafka 3.7** (BC3 event store, BC7, BC8). *Event streaming* *open source* (Apache 2.0). Se elige por: (a) *source of truth* del *Event Sourcing* (RNF-04, inmutabilidad por diseño); (b) retención ≥ 5 años (Contraloría); (c) escalado con particiones para 250 incidentes/min (RNF-02); (d) orden por `incidente_id`; (e) CDC con Debezium para alimentar ClickHouse y Redis. Referencias: Kleppmann (2017), Richardson (2019).

**ClickHouse 24** (BC4). OLAP columnar *open source* (Apache 2.0). Se elige por: (a) escaneo columnar sub-segundo sobre millones de incidentes (RNF-02, ≤ 20 s); (b) compresión que reduce coste on-premise; (c) alimentación por Kafka Connect; (d) Ley 9986 (sustituible por DuckDB/Druid).

**Redis 7 / Valkey** (BC2, BC5). Cache en memoria (RSALv2/SSPL; alternativa **Valkey** BSD). Se elige por: (a) latencia sub-ms para cache de recursos y mapa de calor (RNF-02); (b) estructuras GEO nativas; (c) Sentinel para *failover* (RNF-01). Se prefiere **Valkey** para cumplimiento estricto Ley 9986.

**PostGIS 3.4** (BC5). Extensión geoespacial de PostgreSQL (GPL). Índices GiST para zonas de riesgo y reincidencia territorial (Proceso 3 del RFP). Open source.

**Keycloak 24** (BC6). IAM *open source* (Apache 2.0). RBAC + ABAC por institución (RNF-03, RNF-06), LDAP/AD del Ministerio, MFA, sesiones para 1.200–2.000 usuarios concurrentes.

**SQLite 3** (BC7). BD embebida *public domain*. Operación local sin conectividad (RNF-05), sincronización idempotente, resolución de conflictos CRDT.

**MinIO** (BC9). Object storage S3-compatible (AGPLv3). *Object Lock* WORM para evidencia y exportaciones inmutables (RNF-04, Contraloría ≥ 5 años). API S3 estándar (sustituible por Ceph).

**Apicurio Schema Registry** (BC8). Registro de esquemas (Apache 2.0). Gobernanza de *event schemas* con compatibilidad *backward* obligatoria.

---

## 4.4 Modelos de consistencia por almacén

| *Bounded Context* | Modelo | Justificación |
|---|:--:|---|
| BC1 Incidentes | **Fuerte (ACID)** | El ciclo de vida exige transiciones consistentes; una pérdida implica un caso sin responsable (RNF-02). |
| BC2 Despacho | **Fuerte** en asignación; **eventual** en cache | La asignación no admite duplicación; el cache tolera 5 s (revalidado por CDC). |
| BC3 Bitácora | **Eventual** (proyección); Kafka es **canónica** | RNF-04 garantiza inmutabilidad por Kafka; la proyección es reconstruible. |
| BC4 Analítica | **Eventual** | Coherente con ADR-0002; latencia tolerable para planificación. |
| BC5 Geoespacial | **Fuerte** PostGIS; **eventual** Redis | Zonas = datos maestros; incidentes activos se actualizan por CDC ≤ 20 s. |
| BC6 IAM | **Fuerte** | La revocación de acceso debe ser inmediata (RNF-03). |
| BC7 Offline | **Eventual** con CRDT | Por naturaleza offline; reconciliación idempotente. |
| BC8 Bus | **Eventual**; orden por partición | Asíncrono; orden por `incidente_id` garantiza secuencia. |
| BC9 Archivos | **Fuerte** metadatos; **inmutable** objetos | Metadatos consultables; objetos son evidencia WORM. |

### 4.4.1 Transacciones distribuidas: patrón Saga

Las operaciones que cruzan *bounded contexts* **no** usan 2PC/XA. Se resuelven con **Saga** (Richardson, 2019):

- **Saga orquestada** para el flujo crítico **Despacho de Recurso** (Proceso 2): el *orchestrator* coordina (1) reservar recurso en BC2, (2) registrar entrada en bitácora BC3, (3) publicar `RecursoDespachadoEvent`, (4) notificar instituciones. Cada paso tiene **acción compensatoria**.
- **Saga coreografiada** para flujos analíticos (Proceso 3): `IncidenteRegistradoEvent` dispara, en paralelo, actualización del cache (BC5), proyección al DW (BC4) y evaluación de alertas.

### 4.4.2 Patrón CQRS

- **BC2 Despacho**: escrituras en PostgreSQL; lecturas (recursos cercanos) en Redis GEO, actualizado por CDC.
- **BC4 Analítica**: escrituras (ingesta) en Kafka; lecturas (mapa de calor, reportes) en ClickHouse, proyectado por Kafka Connect.
- **BC3 Bitácora**: escritura (append) en Kafka; lectura (consulta histórica) en la proyección PostgreSQL.

### 4.4.3 *Event Sourcing* (bitácora inmutable)

Cada acción sobre un incidente (`IncidenteRegistrado`, `IncidenteClasificado`, `RecursoDespachado`, `CasoEscalado`, `CasoCerrado`) se persiste como **evento inmutable** en Kafka (tópico `bitacora.incidentes`, retención ≥ 5 años). La proyección PostgreSQL es un *read model* reconstruible. La inmutabilidad se garantiza por: (a) eventos Kafka *append-only* por construcción; (b) la proyección se crea con rol sin UPDATE/DELETE; (c) acceso administrativo segregado por RBAC y auditado.

### 4.4.4 *Outbox Pattern*

Cada microservicio que origina eventos escribe en su BD una tabla `outbox` dentro de la **misma transacción** del cambio de estado; Debezium CDC lee `outbox` y publica en Kafka. Esto garantiza la atomicidad entre el cambio y la publicación (Richardson, 2019).

---

## 4.5 Seguridad y multi-tenancy (RNF-03, Ley 8968)

### 4.5.1 Aislamiento por institución

Doble barrera: (1) **particionamiento físico por `institucion_id`** en PostgreSQL y Kafka; (2) **RLS** en PostgreSQL con políticas que restringen filas según el `institucion_id` del JWT (Keycloak):

```sql
CREATE POLICY aislamiento_institucional ON incidentes
FOR SELECT
USING (institucion_origen_id = current_setting('app.institucion_id')::int
       OR has_role(current_user, 'cne_supervisor', 'member'));
```

El rol `cne_supervisor` tiene visibilidad consolidada para Protocolos de Emergencia Nacional (RNF-06), **sin** acceso a datos internos (RNF-03).

### 4.5.2 Cifrado

- **En tránsito:** TLS 1.3 en todas las conexiones; acceso al perímetro sólo por VPN (ADR-001).
- **En reposo:** LUKS a nivel volumen; pgcrypto para columnas sensibles; SSE en MinIO.

### 4.5.3 Auditoría de acceso a datos personales (Ley 8968)

Todo acceso a datos personales se registra como `DatoPersonalAccedido` en la bitácora (BC3), con identidad, institución, marca de tiempo y justificación.

---

## 4.6 Estrategia *Offline-First* (RNF-05)

1. **Operación local.** El funcionario registra/actualiza incidentes en SQLite local sin conectividad.
2. **Outbox local.** Cada cambio se escribe en `outbox` local con `evento_id` UUID (idempotencia).
3. **Reconexión.** El cliente envía eventos pendientes; el microservicio los aplica **idempotentemente** (deduplicación por `evento_id`).
4. **Resolución de conflictos.** Marcas de tiempo vectoriales; *merge* automático para campos no conflictivos; para conflictivos, prevalece la versión más reciente y se registra la divergencia en la bitácora.

---

## 4.7 Retención y cumplimiento normativo

| Almacén | Retención | Cumplimiento |
|---|---|---|
| Kafka `bitacora.incidentes` | **≥ 5 años** | Contraloría; RNF-04 |
| Proyección PG `bitacora_eventos` | **≥ 5 años** (particionado mensual) | Idem |
| MinIO (evidencia, exportaciones) | **≥ 5 años** Object Lock WORM | Inmutabilidad Contraloría |
| PostgreSQL operacional | **3 años caliente** + *archival* MinIO | Equilibrio consulta/coste |
| ClickHouse | **5 años** (particionado mensual, TTL) | Analítica histórica |
| Redis | **Volátil** (TTL 5 s–24 h) | Cache; no es fuente de verdad |
| SQLite local | **30 días** + purga tras sync | Minimización Ley 8968 |

### 4.7.1 Exportación para la Contraloría

Se genera desde el event store Kafka (o proyección PG) en CSV/JSON/PDF firmado, se empaqueta en MinIO con Object Lock WORM y se entrega por VPN + firma digital. Inmutable y verificable (hash SHA-256).

---

## 4.8 Estrategia de respaldo y recuperación (RNF-01)

| Almacén | RPO | RTO | Mecanismo |
|---|:--:|:--:|---|
| PostgreSQL (BC1, BC2, BC5, BC6, BC9) | 0 s | < 30 s | *Streaming replication* síncrona + Patroni; WAL archiving a MinIO |
| Kafka (BC3, BC8) | 0 s | < 60 s | Factor replicación 3, `min.insync.replicas=2`; KRaft |
| ClickHouse (BC4) | < 5 min | < 2 min | ReplicatedMergeTree; reconstruible desde Kafka |
| Redis (BC2, BC5) | < 5 s | < 30 s | Sentinel + AOF; reponible desde PostgreSQL |
| MinIO (BC9) | 0 s | < 2 min | Erasure coding + replicación entre *sites* |
| Keycloak (BC6) | 0 s | < 60 s | Replicación PostgreSQL subyacente |

El **RTO agregado** ≤ 2 min porque: (a) almacenes críticos (PG, Kafka) *failover* < 60 s; (b) almacenes reconstruibles desde Kafka (ClickHouse, Redis) aceptan < 2 min; (c) el *blast radius* acotado de la políglota permite que un fallo local no caiga todo el sistema.

---

## 4.9 Tabla resumen de tecnologías (cumplimiento Ley 9986)

| Tecnología | Licencia | Sustituible por | Cumple |
|---|---|---|:--:|
| PostgreSQL 16 | PostgreSQL License (BSD-like) | — | ✓ |
| Apache Kafka 3.7 | Apache 2.0 | RedPanda, Pulsar | ✓ |
| ClickHouse 24 | Apache 2.0 | DuckDB, Druid | ✓ |
| Redis 7 / Valkey | RSALv2/SSPL · BSD (Valkey) | Valkey (LF), KeyDB | ✓ |
| PostGIS 3.4 | GPL | — (extensión PG) | ✓ |
| Keycloak 24 | Apache 2.0 | Authentik, ORY Kratos | ✓ |
| SQLite 3 | Public Domain | — | ✓ |
| MinIO | AGPLv3 | Ceph, Rook | ✓ |
| Apicurio | Apache 2.0 | Confluent Schema Registry | ✓ |

---

## 4.10 Diagramas asociados

- **Diagrama de Topología de Datos (Mermaid):** `docs/c4-models/topologia-datos.md`
- **Diagrama editable (draw.io):** `docs/c4-models/topologia-datos.drawio`
- **Matriz comparativa (anexo visual):** `docs/src-sad/matriz-comparativa-persistencia.md`

---

## 4.11 Referencias (APA 7ª ed.)

- Evans, E. (2003). *Domain-Driven Design: Tackling Complexity in the Heart of Software*. Addison-Wesley.
- Fowler, M. (2015, 25 de marzo). *Microservices: A definition of this new architectural term*. https://martinfowler.com/articles/microservices.html
- Hruschka, P., & Starke, G. (2024). *arc42 — Template for architecture documentation and communication* (versión 8.2). https://arc42.org
- Kleppmann, M. (2017). *Designing Data-Intensive Applications*. O'Reilly Media.
- Newman, S. (2021). *Building Microservices* (2.ª ed.). O'Reilly Media.
- Richardson, C. (2019). *Microservices Patterns*. Manning Publications.
- Vernon, V. (2013). *Implementing Domain-Driven Design*. Addison-Wesley.
- Asamblea Legislativa de Costa Rica. (2011). *Ley N.° 8968, Ley de Protección de la Persona frente al Tratamiento de sus Datos Personales*. La Gaceta N.° 103.
- Asamblea Legislativa de Costa Rica. (2018). *Ley N.° 9986, Ley de la Contratación Pública*. La Gaceta N.° 97.
- Brown, S. (2024). *The C4 model for visualising software architecture*. https://c4model.com

