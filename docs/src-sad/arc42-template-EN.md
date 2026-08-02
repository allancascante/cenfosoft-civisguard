---
date: July 2025
title: "![arc42](images/arc42-logo.png) Template"
---

# 

**About arc42**

arc42, the template for documentation of software and system
architecture.

Template Version 9.0-EN. (based upon AsciiDoc version), July 2025

Created, maintained and © by Dr. Peter Hruschka, Dr. Gernot Starke and
contributors. See <https://arc42.org>.

# Introduction and Goals

## Requirements Overview

**CivisGuard Analytics** is a national mission-critical platform for coordinating, monitoring, and analyzing inter-institutional incidents in Costa Rica. Its purpose is to provide a shared view of the territory, coordinate resource dispatch, preserve complete case traceability, and transform operational data into preventive intelligence.

The solution serves the following institutions:

1. 9-1-1 Emergency System.
2. Public Force.
3. Costa Rican Social Security Fund (CCSS).
4. Costa Rican Red Cross.
5. Costa Rican Fire Department.
6. National Commission for Risk Prevention and Emergency Response (CNE).

CivisGuard is not a public reporting channel and does not replace existing institutional systems. It integrates with them to consolidate information, coordinate responsibilities, and produce differentiated operational and analytical views.

The main business processes are:

- incident reception, registration, and classification;
- coordinated dispatch and inter-institutional tracking;
- resource availability and status updates;
- activation of national emergency protocols by the CNE;
- field-unit operation under degraded connectivity;
- territorial monitoring, heat maps, and recurrence analysis;
- generation, consultation, and export of audit logs.

The target scale defined by the RFP is:

| Dimension | Target |
|---|---|
| Concurrent users | Between 1,200 and 2,000 institutional users during peak hours. |
| Initial volume | Approximately 30,000 incidents per month in the Greater Metropolitan Area. |
| Nationwide projection | Up to 80,000 incidents per month. |
| Ingestion peak | Up to 250 incidents per minute. |
| Coverage | Initial phase in the Greater Metropolitan Area, followed by nationwide expansion. |
| Availability | Continuous 24/7/365 operation. |

### Document consistency note

The RFP and the C4 Level 1, 2, and 3 models include operational registration, coordination, and near-real-time dispatch capabilities. ADR-0002, however, describes a purely analytical batch-oriented solution that does not participate in dispatch.

To keep this SAD consistent with the contractual scope and current diagrams, ADR-0002 is interpreted only as the decision applicable to **analytical ingestion from legacy institutional systems**. CivisGuard's operational plane retains the Incident, Dispatch, CNE Protocol, and Offline Synchronization services. This interpretation must be formalized by updating or superseding ADR-0002.

## Quality Goals

| Priority | Quality goal | Main criterion |
|---:|---|---|
| 1 | Availability and fault tolerance | Maintain 24/7/365 operation and limit unplanned downtime to no more than two consecutive minutes. |
| 2 | Operational performance | Allow at least one resource to be dispatched for a critical incident within 90 seconds. |
| 3 | Integrity and auditability | Record every relevant action in an immutable, verifiable log that remains queryable for at least five years. |
| 4 | Security and institutional segregation | Ensure that every institution and profile accesses only the information required for its responsibilities. |
| 5 | Connectivity resilience | Allow offline operation and later synchronization without data loss or duplicate records. |
| 6 | Scalability and evolvability | Support the defined peaks, nationwide expansion, and independent deployments without stopping the entire platform. |

## Stakeholders

| Role/Name | Contact or representation | Expectations |
|---|---|---|
| MGPSP / DGTIC | Issuing institution and requesting area | Architecture governance, operational continuity, legal compliance, consolidated national visibility, and cost control. |
| 9-1-1 Emergency System | Operators and integration owners | Immediate incident registration and classification, dispatch within the SLA, and simple operation under pressure. |
| Public Force | Supervisors, officers, and technical teams | Coordination, traceability, protection of tactical information, and operational autonomy. |
| CCSS | Supervisors, response personnel, and technical teams | Resource coordination, minimum necessary access, and protection of personal data. |
| Costa Rican Red Cross | Supervisors and field units | Resource availability, mobile operation, and reliable synchronization. |
| Costa Rican Fire Department | Supervisors and operational units | Safe coordination, functional autonomy, and response to fires and hazardous-material incidents. |
| CNE | National emergency coordinator | Consolidated resource visibility and the ability to activate national protocols without manual confirmation by each institution. |
| Territorial analyst | MGPSP and institutional analysts | Heat maps, historical reports, metrics, and recurrence detection. |
| Comptroller auditor | Office of the Comptroller General | Complete, exportable, verifiable logs available for at least five years. |
| Access administrator | Security/IAM team | Centralized identity, role, attribute, and institutional segregation management. |
| MGPSP infrastructure team | On-premise operations | Reproducible deployment, monitoring, backup, recovery, patching, and sufficient capacity. |
| Cenfosoft consulting team | Gustavo Castro, David Cárdenas, Allan Cascante, and Randy Villareal | Design, justify, document, and defend the proposed architecture. |

# Architecture Constraints

| Constraint | Description and architectural impact |
|---|---|
| On-premise infrastructure only | ADR-001 excludes public and hybrid cloud. Every component is hosted and processed on physical infrastructure controlled by the MGPSP. |
| VPN-only access | Institutional and operational access must use an authorized VPN connection. Business endpoints are not exposed directly to the internet. |
| Vendor independence | Law 9986 prohibits irrescindable technological dependency. Open-source technologies, open formats, OCI containers, and reproducible infrastructure are prioritized. |
| 24/7/365 operation | Maintenance windows must not compromise critical operations. Maximum unplanned downtime is two consecutive minutes. |
| Critical dispatch | A critical incident must not remain without at least one dispatched resource for more than 90 seconds after registration and classification. |
| Territorial update | The heat map must reflect an active incident no later than 20 seconds after registration. |
| Institutional segregation | Information must be filtered by role, institution, jurisdiction, incident participation, and sensitivity. |
| Immutable audit log | Incident actions cannot be modified or deleted and must remain historically queryable for at least five years. |
| Offline-first operation | Field units must record and update information under limited connectivity and synchronize later without loss or duplication. |
| Data sovereignty and protection | Personal data processing must comply with Law 8968 and the principles of purpose limitation, proportionality, security, and minimum access. |
| Institutional competencies | The solution must respect the General Police Law, the National Emergency System Law, Fire Department autonomy, and the competencies of participating institutions. |
| Limited physical capacity | Scaling is constrained by available on-premise hardware; capacity must be planned for peaks and nationwide growth. |

# Context and Scope

## Business Context

![C4 Level 1 — System Context](../c4-models/SystemContext-C4%20Nivel%201.drawio.png)

CivisGuard is positioned at the center of inter-institutional coordination. It receives incidents, exchanges availability and dispatch information with institutional systems, provides interfaces for authorized users, and exports logs for oversight.

### Actors and external systems

| Actor or system | Relationship with CivisGuard |
|---|---|
| 9-1-1 operator | Registers, classifies, and requests incident dispatch. |
| Institutional supervisor | Monitors active incidents, manages resources, and coordinates their institution's participation. |
| Territorial analyst | Consults heat maps, reports, and recurrence metrics. |
| Field officer or unit | Updates statuses, records field information, and operates offline when necessary. |
| CNE coordinator | Activates and manages national emergency protocols. |
| Comptroller auditor | Consults and exports historical logs for oversight. |
| Access administrator | Manages identities, roles, attributes, and institutional permissions. |
| 9-1-1 System | Primary source of incidents reported by citizens. |
| Institutional systems | Provide resource availability, confirmations, and operational statuses. |
| Comptroller system | Receives audit-log and evidence exports. |

> **Pending diagram correction:** the C4 Level 1 diagram contains a duplicated “Field Officer or Unit” label where one figure actually represents the “National Emergency Coordinator.” This document uses the correct role, and the `.drawio` source should be corrected.

### Scope boundaries

In scope:

- inter-institutional coordination;
- incident registration and lifecycle;
- resource dispatch and tracking;
- differentiated visibility;
- heat maps and territorial analytics;
- audit logging and export;
- offline synchronization;
- identity and access management.

Out of scope:

- direct reception of citizen reports;
- replacement of each institution's internal dispatch system;
- management of public telecommunications infrastructure;
- public or hybrid cloud deployment;
- automation of decisions that legally require human intervention.

## Technical Context

### External interfaces

| Interface | Direction | Channel or protocol | Information exchanged | Considerations |
|---|---|---|---|---|
| Web users | User → CivisGuard | HTTPS/REST over VPN; JWT | Commands, queries, reports, and administration | Centralized authentication, RBAC/ABAC, rate limiting, and auditing. |
| Mobile application | Bidirectional | HTTPS/REST over VPN and deferred synchronization | Field events, statuses, and confirmations | Local SQLite, idempotency, deduplication, and conflict resolution. |
| 9-1-1 System | 9-1-1 → CivisGuard | REST API, webhook, or contractual integration | Registered and classified incidents | Schema validation, mutual authentication, and idempotency keys. |
| Institutional systems | Bidirectional | REST/gRPC for operations; batch ETL/ELT for analytics | Availability, reservations, confirmations, and historical datasets | Timeouts, manual fallback, versioned contracts, and segregation. |
| Comptroller system | CivisGuard → Comptroller | API or signed file | Logs and historical exports | Integrity, traceability, authorization, and agreed formats. |
| Event bus | Services and workers ↔ Kafka | Kafka protocol | Domain and integration events | At-least-once delivery, versioned schemas, and partitioning by incident. |
| Internal persistence | Service → owned store | JDBC/SQL, S3 API, or native protocol | Bounded-context data | Database-per-service; direct queries across service databases are prohibited. |

### Input/output channel mapping

| Input or output | Producer | Consumer | Channel |
|---|---|---|---|
| `IncidenteRegistrado` | Incident Service | Dispatch, Heat Map, Audit, and Analytics | Kafka |
| `RecursoDespachado` / `RecursosDespachados` | Dispatch Service | Audit, analytics, and interested systems | Kafka |
| `ProtocoloEmergenciaNacional` | CNE Protocol Service | Operational services and workers | Logically high-priority Kafka flow |
| `EventoCampo` | Offline Synchronization Service | Domain services and audit | Kafka |
| Availability query | Dispatch Service | Cache and institutional systems | Redis/Valkey and REST |
| Audit export | Audit service/worker | Comptroller system | API or signed file |
| Historical data | Institutional systems | Analytical pipeline | Batch ETL/ELT |

# Solution Strategy

## Macro Architectural Style: Hybrid Event-Driven Architecture on On-Premise Kubernetes

The solution combines a synchronous operational plane for critical commands with an asynchronous event-based plane for integration, projections, auditing, and analytics.

The architecture runs exclusively on an MGPSP on-premise Kubernetes cluster and is accessed through VPN.

## Operational plane

The Incident, Dispatch, CNE Protocol, and Offline Synchronization services contain the main business logic. They expose contractual APIs through the API Gateway and maintain strong consistency within their own aggregates and databases.

Operations requiring an immediate response use REST or gRPC:

- register and classify incidents;
- query resource availability;
- initiate and confirm dispatches;
- activate national protocols;
- synchronize offline operations.

Transactions spanning institutions or bounded contexts are coordinated through Sagas and compensating actions.

## Asynchronous and analytical plane

Confirmed events are published to Apache Kafka. Stateless workers consume them to:

- maintain the heat map;
- build the append-only audit log;
- populate the data warehouse;
- update caches and projections;
- generate territorial intelligence.

Historical ingestion from legacy institutional systems may use scheduled ETL/ELT. This batch path corresponds to the analytical scope of ADR-0002 and does not replace the internal operational flow.

## Distributed polyglot persistence

Database-per-service is applied, and each bounded context selects the appropriate store:

- PostgreSQL for OLTP, ACID rules, and RLS;
- ClickHouse for OLAP and territorial aggregations;
- PostGIS for geospatial queries;
- Redis/Valkey for availability and geospatial caches;
- SQLite for offline operation;
- MinIO with Object Lock for evidence and WORM archival;
- Kafka as the EDA bus and durable event log;
- Keycloak for identities, roles, and attributes.

## Kubernetes as the orchestration platform

Kubernetes provides:

- isolation and independent deployment by service;
- automatic restart and rescheduling of containers;
- rolling updates;
- horizontal scaling;
- network policies;
- reproducible administration through manifests and infrastructure as code.

KEDA scales workers according to Kafka lag or queue depth. Scaling is limited by physical on-premise capacity and must therefore be accompanied by capacity planning.

## Security by design

The API Gateway is the single entry point and delegates authentication to Keycloak. Authorization combines RBAC and ABAC by institution, role, jurisdiction, sensitivity, and incident participation. Data is encrypted in transit and at rest, and every sensitive action produces an audit entry.

# Building Block View

## Whitebox Overall System

![C4 Level 2 — Containers](../c4-models/SystemContext-C4%20Nivel%202.drawio.png)

### Motivation

The container decomposition separates user channels, operational logic, asynchronous processing, and persistence. This limits failure blast radius, allows each workload to scale independently, and prevents analytical queries from affecting registration and dispatch operations.

### Contained building blocks

| Building block | Technology | Responsibility |
|---|---|---|
| Institutional Web App | React / TypeScript | Portal for operators, supervisors, and analysts. |
| Field Mobile App | React Native + SQLite | Field-unit operation with offline-first support. |
| API Gateway | Kong or Tyk/Nginx | Single entry point, TLS, authentication, authorization, rate limiting, and routing. |
| IAM | Keycloak | Identities, MFA, LDAP, RBAC/ABAC, and institution-specific JWTs. |
| Incident Service | Node.js / Express | Incident registration, classification, and lifecycle. |
| Dispatch Service | Java / Spring Boot | Availability, reservations, dispatch Saga, confirmation, and compensation. |
| CNE Protocol Service | Node.js / Express | Activation and distribution of national protocols. |
| Offline Synchronization Service | Go | Reception, deduplication, validation, and reconciliation of field events. |
| Event Bus | Apache Kafka 3.7 | EDA integration, durable retention, and event distribution. |
| Heat Map Worker | Python / KEDA | Territorial projection updates within 20 seconds. |
| Audit Worker | Python / KEDA | Append-only persistence and export preparation. |
| Analytics Worker | Python / KEDA | Data-warehouse loading and recurrence metrics. |
| Operational persistence | PostgreSQL 16 | ACID incident, dispatch, IAM, and metadata data. |
| Analytical store | ClickHouse 24 | Reports, heat maps, and historical data. |
| Geospatial layer | PostGIS 3.4 + Redis GEO | Risk zones, nearby resources, and active incidents. |
| Evidence archive | MinIO | Objects, evidence, and WORM exports. |

### Important interfaces

- HTTPS/REST between clients and the API Gateway.
- REST/gRPC between the Gateway and services.
- Kafka for domain and integration events.
- JDBC/SQL only between a service and its owned database.
- S3 API for MinIO.
- Redis/Valkey for availability and geospatial caches.
- Contractual REST APIs with institutional systems.
- ETL/ELT for historical datasets sent to the analytical plane.

### Institutional Web App

**Purpose:** provide differentiated operational and analytical views for operators, supervisors, and analysts.

**Interfaces:** HTTPS to the API Gateway; updates through queries or authorized notification channels.

**Quality characteristics:** institutional accessibility, profile segregation, responsive interaction, and no reliance on client-side authorization alone.

### Field Mobile App

**Purpose:** allow field registration and updates of incidents and resources.

**Interfaces:** API Gateway and Offline Synchronization Service.

**Quality characteristics:** local SQLite storage for up to 30 days, durable queue, retries, idempotency, and intermittent-connectivity support.

### API Gateway and IAM

**Purpose:** centralize authentication, authorization, TLS, consumption limits, ingress observability, and routing.

**Interfaces:** HTTPS/REST, internal gRPC, Keycloak/LDAP, and JWT.

**Quality characteristics:** high availability, consistent policies, traceability, and no bypass to internal services.

### Incident Service

**Purpose:** register, classify, and manage the incident lifecycle.

**Interfaces:** REST through the Gateway, owned PostgreSQL, Transactional Outbox, and Kafka.

**Fulfilled requirements:** immediate registration, traceability, institutional segregation, and generation of `IncidenteRegistrado`.

### Dispatch Service

**Purpose:** coordinate the selection, reservation, and confirmation of resources across institutions.

**Interfaces:** REST, Redis/Valkey, institutional systems, PostgreSQL, and Kafka.

**Quality characteristics:** confirmation within 90 seconds, manual fallback, orchestrated Saga, and idempotency.

### CNE Protocol Service

**Purpose:** validate and distribute national emergency protocols.

**Interfaces:** REST and Kafka.

**Quality characteristics:** propagation without institution-by-institution manual confirmation, strict access control, and rule versioning.

### Offline Synchronization Service

**Purpose:** reconcile operations accumulated by field units.

**Interfaces:** Mobile App, owned PostgreSQL/store, and Kafka.

**Quality characteristics:** deduplication, logical ordering, version validation, and explicit conflict resolution.

### Projection workers

**Purpose:** build derived views without blocking the operational plane.

**Interfaces:** Kafka, ClickHouse, append-only PostgreSQL, PostGIS, Redis/Valkey, and MinIO.

**Quality characteristics:** KEDA scaling, replay, checkpoints, and idempotency.

## Level 2 — Persistence and data topology

Source file: [`Topologia-datos.drawio`](../c4-models/Topologia-datos.drawio)

The topology is organized into layers:

1. web, mobile, and external-system clients;
2. API Gateway and IAM over VPN;
3. bounded-context-aligned microservices;
4. Apache Kafka EDA bus;
5. distributed polyglot persistence.

### Bounded contexts and stores

| Bounded Context | Primary store | Consistency model |
|---|---|---|
| BC1 Incidents | PostgreSQL partitioned by `institucion_id` | ACID within the aggregate; events toward other contexts. |
| BC2 Dispatch and Resources | PostgreSQL + Redis GEO | Local ACID; Saga for inter-institutional coordination. |
| BC3 Audit and Oversight | Kafka + append-only PostgreSQL + MinIO WORM | Immutability, verification, and queryable projection. |
| BC4 Analytics and BI | ClickHouse | Eventual consistency and OLAP workloads. |
| BC5 Geospatial | PostGIS + Redis GEO | Low-latency projections and a persistent geospatial source. |
| BC6 IAM | Keycloak + PostgreSQL store | Strong consistency for identities and permissions. |
| BC7 Offline Synchronization | Local SQLite + synchronization service | Eventual convergence, idempotency, and conflict resolution. |
| BC9 Files and Evidence | Metadata PostgreSQL + MinIO | Metadata integrity and WORM retention. |

## Level 3 — Dispatch Service

![C4 Level 3 — Dispatch Service Components](../c4-models/SystemContext-C4%20Nivel%203.drawio.png)

The Dispatch Service is divided through CQRS into a query side and a command side.

### Query side

| Component | Responsibility |
|---|---|
| Availability Query Handler | Receives availability queries and checks the cache first. |
| Resource Availability Fetcher | Queries institutional systems when sufficiently fresh information is unavailable. |
| Availability Cache | Maintains the latest known resource state by institution. |
| Fallback Alert Publisher | Notifies an operator or supervisor when an institution does not respond and a manual decision is required. |

> The data topology defines a 5-second TTL for the BC2 resource cache, while C4 Level 3 states 30 seconds. For critical dispatch, this SAD adopts a target of **TTL ≤ 5 seconds**, and the component diagram must be updated to remove the discrepancy.

### Command side

| Component | Responsibility |
|---|---|
| Dispatch Command Handler | Validates the command and starts the coordination Saga. |
| Dispatch Saga Orchestrator | Requests reservations, waits for confirmations, and decides whether to confirm or compensate. |
| Dispatch Confirmation Handler | Confirms the global dispatch, persists the result, and publishes `RecursosDespachados`. |
| Compensation Handler | Releases reservations and reports failure when a timeout or rejection occurs. |
| Dispatch Repository | The only component allowed to write to the dispatch database. |

### Dispatch Service external dependencies

- API Gateway for authenticated commands and queries.
- Institutional systems for availability, reservation, and confirmation.
- Redis/Valkey for availability reads.
- PostgreSQL for dispatch state.
- Kafka for confirmed events.
- Operator or supervisor for manual fallback.

# Runtime View

## Scenario 1: Incident registration and heat-map update

1. The operator registers and classifies an incident through the Web App.
2. The API Gateway validates the token, institution, role, and consumption limits.
3. The Incident Service validates business rules and persists the incident and an outbox entry in one local transaction.
4. A publisher sends `IncidenteRegistrado` to Kafka.
5. The Heat Map Worker consumes the event and updates the geospatial projection.
6. The Audit Worker appends the event to the audit record.
7. The Analytics Worker updates data-warehouse projections.
8. Authorized views display the incident within 20 seconds.

Notable aspects:

- incident confirmation does not depend on ClickHouse;
- consumers are idempotent;
- an analytical failure does not prevent registration;
- events are partitioned by `incidentId` to preserve case ordering.

## Scenario 2: Coordinated dispatch of a critical incident

1. The operator queries available resources.
2. Availability Query Handler queries Redis/Valkey.
3. For missing or expired data, Resource Availability Fetcher queries institutional systems.
4. When an institution does not respond, Fallback Alert Publisher requests a manual decision.
5. The operator submits the dispatch command.
6. Dispatch Command Handler starts the Saga.
7. Dispatch Saga Orchestrator requests reservations from the relevant institutions.
8. Dispatch Confirmation Handler receives confirmations.
9. When the conditions are satisfied within 90 seconds, the dispatch is persisted and `RecursosDespachados` is published.
10. On timeout or rejection, Compensation Handler releases reservations and notifies the operator.

Notable aspects:

- there is no global ACID transaction;
- consistency is achieved through Saga coordination, compensation, and idempotency;
- Dispatch Repository is the only writer to its database;
- the failure of one institution must not block the others indefinitely.

## Scenario 3: Offline operation and synchronization

1. A field unit loses connectivity.
2. The Mobile App stores operations in SQLite with unique identifiers, versions, and local order.
3. The application continues to provide local confirmations and maintains a durable queue.
4. After VPN connectivity is restored, pending operations are sent to the Offline Synchronization Service.
5. The service deduplicates, validates versions, and applies conflict rules.
6. Accepted operations are published as `EventoCampo`.
7. Conflicts that cannot be resolved automatically are referred to a supervisor.

Notable aspects:

- last-write-wins is not used for critical transitions;
- server-confirmed operations are removed from the local queue;
- local storage retains up to 30 days under the current topology.

## Scenario 4: National Emergency Protocol activation

1. An authenticated CNE Coordinator activates a protocol.
2. The CNE Protocol Service validates permissions, validity, and version.
3. It persists the activation and publishes `ProtocoloEmergenciaNacional`.
4. Operational services update their rules and priorities.
5. Workers and views reflect the emergency state.
6. The audit log records who activated the protocol and the justification.

Notable aspects:

- institution-by-institution manual confirmation is not required;
- consumers must be able to receive the event again without duplicating effects;
- protocol versioning supports audit and controlled rollback.

## Scenario 5: Batch analytical ingestion from legacy systems

1. An institution generates a historical dataset according to the agreed contract.
2. The file or batch is transferred through a secure channel.
3. The pipeline validates schema, integrity, institution, and period.
4. Data is normalized and loaded into the analytical plane.
5. Metrics, reports, and historical maps are produced.
6. Errors are isolated for reprocessing without affecting operational systems.

This scenario implements the analytical scope of ADR-0002 without removing CivisGuard's operational capabilities.

## Scenario 6: Audit-log export to the Comptroller

1. An authorized auditor requests an incident range.
2. The service validates permissions, purpose, and institutional filters.
3. Append-only projections and archived objects are queried.
4. An export is generated with integrity and traceability metadata.
5. The file is temporarily stored in MinIO and delivered through an API or agreed channel.
6. The request and download are recorded in the audit log.

# Deployment View

## Infrastructure Level 1

Reference file: [`Topologia-datos.drawio`](../c4-models/Topologia-datos.drawio)

### Motivation

Deployment must preserve data sovereignty, comply with the on-premise decision, and sustain continuous operation. Kubernetes decouples software from specific hardware and allows the environment to be rebuilt within institutional infrastructure.

### Quality and performance features

- VPN-only access;
- no public business endpoints;
- redundancy of critical components;
- Kafka replication factor 3 and `min.insync.replicas=2`;
- worker scaling with KEDA;
- separation of OLTP, OLAP, geospatial, and object workloads;
- WORM storage for exports and evidence;
- centralized monitoring;
- tested backup and recovery;
- physical capacity sized for 2,000 users and 250 incidents per minute.

### Mapping of building blocks to infrastructure

| Infrastructure | Deployed building blocks |
|---|---|
| Institutional VPN perimeter | Access by users, units, and external systems. |
| Load balancers / Kubernetes ingress | API Gateway and TLS termination. |
| On-premise Kubernetes cluster | Microservices, workers, Web App, connectors, and integration components. |
| IAM platform | Keycloak, LDAP/MFA, and identity storage. |
| Kafka cluster | Topics, KRaft, Schema Registry, and CDC connectors. |
| PostgreSQL/PostGIS cluster | Service-owned databases, RLS, and geospatial data. |
| ClickHouse cluster | Data warehouse and OLAP queries. |
| Redis/Valkey | Availability and geospatial caches. |
| MinIO | Objects, evidence, exports, and WORM retention. |
| Mobile devices | React Native App and local SQLite. |
| Observability platform | Prometheus, Grafana, centralized logs, and alerts. |

## Infrastructure Level 2

### Perimeter, VPN, and access

All access traverses the institutional VPN. The API Gateway is the only entry point to services. Kubernetes network policies prevent clients from directly reaching databases or microservices.

Main risks:

- the VPN can become a bottleneck or single point of failure;
- remote units depend on channel availability;
- redundant VPN concentrators and capacity monitoring are required.

### On-premise Kubernetes cluster

The cluster runs services as independent replicas distributed across physical nodes. It should be configured with:

- a highly available control plane;
- multiple worker nodes;
- anti-affinity for critical replicas;
- PodDisruptionBudgets;
- rolling updates;
- quotas and limits;
- redundant persistent storage;
- NetworkPolicies.

### Apache Kafka and contracts

Kafka uses KRaft, replication factor 3, and at least two in-sync replicas. Apicurio Schema Registry manages event compatibility. Kafka Connect and Debezium build projections and CDC flows where applicable.

Operational retention and legal retention must not be confused: Kafka retains history required by the event strategy, while MinIO WORM and append-only projections provide long-term archival and export.

### Polyglot persistence

Each store must be deployed with backup and recovery appropriate to its criticality. Store-specific RPO/RTO targets still need to be formalized.

- PostgreSQL/PostGIS: replication, failover, and consistent backups.
- ClickHouse: replicas and partitions for historical queries.
- Redis/Valkey: high availability; never the only persistent source.
- MinIO: Object Lock, versioning, and replication/erasure coding.
- SQLite: device encryption, local retention, and deletion after confirmation.

### Observability and operations

Prometheus and Grafana consolidate metrics. Logs and traces must include `correlationId`, `incidentId`, institution, and service while avoiding unnecessary personal data.

Minimum indicators:

- availability and error rate;
- p95/p99 latency;
- dispatch time;
- consumer lag;
- queue depth;
- projection age;
- synchronization failures;
- offline conflicts;
- denied access;
- replica and backup status.

# Cross-cutting Concepts

## Identity, authentication, and authorization

Keycloak centralizes identities and integrates LDAP/MFA. Authorization combines:

- role-based RBAC;
- ABAC by institution, jurisdiction, sensitivity, purpose, and participation;
- RLS or partitioning by `institucion_id`;
- backend enforcement;
- auditing of sensitive and denied access.

## Data ownership and classification

Each bounded context exclusively owns its data. Services do not directly read other services' tables. Information included in events and logs is minimized, and unnecessary copies of personal or tactical information are avoided.

## Contracts and evolution

REST, gRPC, and Kafka contracts are versioned. Events must retain backward compatibility through optional fields, defaults, and deprecation processes.

## Consistency, Saga, and idempotency

Strong consistency is limited to an aggregate and its owned store. Cross-service operations use:

- an orchestrated Saga for dispatch;
- events for propagation;
- Transactional Outbox;
- idempotency keys;
- processed-event tracking;
- uniqueness constraints;
- compensating actions.

## Auditing and integrity

The audit log is append-only and includes identity, institution, action, justification, UTC timestamp, correlation, version, and integrity hash. Hash chaining, periodic signing, and WORM storage are used.

The audit log retains audit metadata and controlled references. Personal incident information and tactical information are not indiscriminately duplicated in the immutable record.

## Resilience and failure handling

Services use timeouts, retries with backoff, circuit breakers, bulkheads, and manual fallback when automation cannot proceed safely. Retries must never produce a second business effect.

## Offline operation

Local operations are durable, identifiable, and synchronizable. Critical transitions are validated against aggregate versions. Unresolvable conflicts are presented to a supervisor.

## Time, ordering, and identifiers

- UTC for audit timestamps.
- Monotonic clocks for durations and timeouts.
- Globally unique incident and event identifiers.
- Partitioning by `incidentId` to preserve ordering within a case.
- Device clocks are not the sole authority for critical decisions.

## Observability

Metrics, logs, and traces are correlated end to end. Alerts are based on SLOs, consumer lag, dependency failures, and capacity loss.

## Configuration and secrets

Secrets are not stored in repositories or container images. They are managed through institutional mechanisms compatible with Kubernetes. Institution-specific configurations are versioned and audited.

# Architecture Decisions

The decisions in this section summarize the main architectural choices for **CivisGuard Analytics**. Their details and alternatives must be maintained in ADRs.

The design recognizes that no mechanism simultaneously optimizes availability, consistency, performance, simplicity, and scalability. It therefore separates workloads and makes trade-offs explicit, following the operational systems, analytical systems, systems of record, and derived data principles discussed in *Designing Data-Intensive Applications, 2nd Edition*.

## ADR summary and traceability

| ADR | Current status | Application in this SAD |
|---|---|---|
| ADR-001 Operational Environment | Proposed | On-premise infrastructure only and VPN access. |
| ADR-0002 Analytics-Oriented Architecture | Proposed, clarification required | Limited to ETL/ELT ingestion and the analytical plane; it does not remove the operational plane required by the RFP and C4 models. |
| ADR-003 Distributed Polyglot Persistence | Proposed | Database-per-service, open source, local consistency, and events across contexts. |

## DD-01: Hybrid Event-Driven Architecture

CivisGuard uses synchronous APIs for commands requiring an immediate response and Kafka to distribute their consequences.

Persistent events are generated for:

- incident registration and classification;
- dispatch and compensation;
- escalation and status changes;
- closure;
- national-protocol activation;
- field synchronization.

This combination avoids long synchronous chains and allows consumers to process information at their own pace. Derived views may be eventually consistent, but the operational plane does not depend on their availability.

## DD-02: Separation Between Operational and Analytical Planes

The operational plane contains authoritative systems of record for incidents, dispatches, and protocols. The analytical plane is built through events, CDC, and ETL/ELT.

CQRS is applied:

- write models for rules and invariants;
- read models for maps, reports, and history;
- analytical queries outside transactional databases.

The consequence is controlled duplication and eventual consistency in exchange for workload isolation and improved scalability.

## DD-03: Distributed Polyglot Persistence

Each microservice owns its store and does not directly access stores owned by others. Technology is selected by workload profile and must be open source and replaceable.

PostgreSQL, ClickHouse, PostGIS, Redis/Valkey, Kafka, MinIO, SQLite, and Keycloak are used according to the data topology.

Strong consistency is guaranteed within the aggregate; cross-service coordination uses Sagas, events, outbox, and idempotency.

## DD-04: Immutable Audit Log with Cryptographic Verification

The operational audit log is append-only. No user, administrator, or service may modify or delete confirmed entries.

Each entry includes:

- event identifier;
- incident identifier;
- official or service identity;
- institution;
- action;
- justification;
- UTC date and time;
- correlation identifier;
- aggregate version;
- integrity hash.

Hash chaining, periodic signing, and immutable-retention storage are used. A public or distributed blockchain is not proposed.

The audit log stores audit metadata and controlled references. Personal incident information and tactical information are not indiscriminately duplicated in the immutable record.

## DD-05: At-Least-Once Delivery and Idempotency

Kafka uses at-least-once delivery semantics. An event may be received several times because of retries or recovery.

Consumers implement:

- unique identifiers;
- processed-event records;
- uniqueness constraints;
- aggregate versions;
- idempotency keys;
- local transactions.

End-to-end exactly-once delivery is not assumed. Transactional Outbox prevents inconsistent dual writes between a transactional database and Kafka.

## DD-06: On-Premise-Only Environment

Every component runs on MGPSP infrastructure and is accessed through VPN. Kubernetes maintains portability across compatible hardware but does not imply public-cloud deployment.

Benefits:

- sovereignty and control;
- reduced perimeter;
- compliance with institutional policies.

Costs:

- reduced elasticity;
- greater operational responsibility;
- dependency on institutional capacity, power, network, and recovery.

## DD-07: Offline-First Field Operation

The Mobile App uses SQLite and a durable local queue. On reconnection, the Offline Synchronization Service deduplicates, validates, and reconciles operations.

Last-write-wins is not applied to critical states. Business conflicts are resolved through versions, domain rules, or manual review.

## DD-08: Institutional Segregation Through RBAC, ABAC, and RLS

Authorization is determined by both role and contextual information. Keycloak issues identities and attributes; services validate permissions, and multi-institutional databases apply RLS or partitioning.

No security decision depends exclusively on the user interface.

# Quality Requirements

Quality requirements define how CivisGuard behaves under normal conditions, demand peaks, partial failures, degraded connectivity, and technological evolution.

Reliability does not imply an absence of failures; it means continuity of service in the presence of foreseeable failures.

```text
CivisGuard Analytics Quality
├── Reliability
│   ├── 24/7/365 availability
│   ├── Fault tolerance
│   ├── Data durability
│   └── Recovery
├── Performance
│   ├── Dispatch within the SLA
│   ├── Event propagation
│   ├── Map updates
│   └── Peak-load capacity
├── Security and Privacy
│   ├── Authentication
│   ├── Institutional segregation
│   ├── Least privilege
│   └── Sensitive data protection
├── Integrity and Auditability
│   ├── Immutable audit log
│   ├── End-to-end traceability
│   ├── Tampering detection
│   └── Historical data export
├── Connectivity Resilience
│   ├── Offline operation
│   ├── Synchronization
│   ├── Deduplication
│   └── Conflict resolution
├── Scalability
│   ├── Concurrent users
│   ├── Incidents per minute
│   └── Nationwide expansion
├── Maintainability
│   ├── Operability
│   ├── Simplicity
│   ├── Observability
│   └── Contract evolution
└── Portability
    ├── Vendor independence
    ├── Reproducible infrastructure
    └── Use of open standards
```

## Quality Requirements Overview

| ID | Attribute | Verifiable requirement | Priority |
|---|---|---|---|
| QR-01 | Availability | 24/7/365 operation; unplanned downtime ≤ two consecutive minutes. | Critical |
| QR-02 | Performance | Dispatch at least one resource for a critical incident within 90 seconds. | Critical |
| QR-03 | Timeliness | Active incident visible on the heat map within 20 seconds of registration. | Critical |
| QR-04 | Capacity | Support 2,000 concurrent users and 250 incidents per minute. | Critical |
| QR-05 | Integrity | Zero loss of confirmed commands and zero duplicate business effects caused by retries. | Critical |
| QR-06 | Security | Zero unauthorized data exposure across institutions or profiles. | Critical |
| QR-07 | Auditability | Every relevant action includes actor, institution, justification, and UTC timestamp. | Critical |
| QR-08 | Immutability | Confirmed audit entries cannot be modified or deleted. | Critical |
| QR-09 | Retention | Logs and exports remain queryable for at least five years. | High |
| QR-10 | Offline | Local operation and later synchronization without loss or duplication. | Critical |
| QR-11 | Autonomy | Each institution configures internal rules without changing those of others. | High |
| QR-12 | National coordination | The CNE changes priorities without manual confirmation by each institution. | Critical |
| QR-13 | Graceful degradation | Analytical-plane failures do not interrupt registration or dispatch. | Critical |
| QR-14 | Evolvability | Producers and consumers remain compatible during contract evolution. | High |
| QR-15 | Operability | Failures, lag, saturation, and degradation are detected through metrics and alerts. | High |
| QR-16 | Portability | Reproducible deployment on compatible on-premise infrastructure without commercial lock-in. | High |
| QR-17 | Recoverability | Failure of one instance or node must not exceed the global downtime limit. | Critical |
| QR-18 | Privacy | Personal data is minimized, encrypted, and accessible only for an authorized purpose. | Critical |

## Quality Scenarios

### QS-01: Critical instance failure

| Element | Scenario |
|---|---|
| Source | Infrastructure |
| Stimulus | An Incident or Dispatch Service instance stops responding. |
| Environment | Active emergency and peak load. |
| Artifact | Service deployed in Kubernetes. |
| Response | The load balancer removes the instance; Kubernetes reschedules a replica and traffic continues through healthy instances. |
| Measure | User-visible downtime ≤ two minutes and zero confirmed commands lost. |

### QS-02: Critical registration and dispatch

| Element | Scenario |
|---|---|
| Source | 9-1-1 operator |
| Stimulus | Registers, classifies, and requests dispatch for a critical incident. |
| Environment | Up to 250 incidents per minute and 2,000 concurrent users. |
| Artifact | Gateway, Incident, Dispatch, Kafka, and operational stores. |
| Response | The incident is confirmed and at least one resource is coordinated. |
| Measure | Dispatch confirmed within 90 seconds. |

### QS-03: Heat-map update

| Element | Scenario |
|---|---|
| Source | Incident Service |
| Stimulus | Publishes `IncidenteRegistrado`. |
| Environment | Normal or peak operation. |
| Artifact | Kafka, Heat Map Worker, and geospatial projection. |
| Response | The consumer processes the event and updates authorized views. |
| Measure | Incident visible within 20 seconds. |

### QS-04: Unauthorized access

| Element | Scenario |
|---|---|
| Source | Authenticated user from an institution |
| Stimulus | Requests information outside their role, institution, or authorized purpose. |
| Environment | Normal operation. |
| Artifact | Gateway, IAM, service, and database. |
| Response | Access is denied before protected data is serialized, and the attempt is logged. |
| Measure | Zero sensitive fields exposed and an audit event generated. |

### QS-05: Audit-log tampering

| Element | Scenario |
|---|---|
| Source | Privileged user or compromised process |
| Stimulus | Attempts to modify or delete a historical entry. |
| Environment | Normal operation. |
| Artifact | Append-only log and WORM archive. |
| Response | The operation is rejected and an integrity alert is generated. |
| Measure | Zero entries altered and a valid verification chain. |

### QS-06: Offline operation

| Element | Scenario |
|---|---|
| Source | Field unit |
| Stimulus | Loses connectivity and records operations. |
| Environment | Rural, border, or disaster-affected area. |
| Artifact | Mobile App and SQLite. |
| Response | Operations are stored locally and remain available after the application restarts. |
| Measure | Zero local data loss and local retention of up to 30 days. |

### QS-07: Reconnection and synchronization

| Element | Scenario |
|---|---|
| Source | Network |
| Stimulus | A stable VPN connection is restored. |
| Environment | Local operations and concurrent online changes exist. |
| Artifact | Offline Synchronization Service. |
| Response | Deduplicates, validates versions, applies rules, and refers unresolved conflicts. |
| Measure | Zero duplicate effects and zero invalid transitions accepted. |

### QS-08: Event redelivery

| Element | Scenario |
|---|---|
| Source | Kafka |
| Stimulus | Redelivers an already processed event. |
| Environment | Consumer recovery. |
| Artifact | Worker or consuming microservice. |
| Response | Detects the identifier and avoids repeating the effect. |
| Measure | One business effect per event. |

### QS-09: Institutional system unavailable

| Element | Scenario |
|---|---|
| Source | External system |
| Stimulus | Does not respond to a resource query or reservation. |
| Environment | Critical dispatch. |
| Artifact | Resource Availability Fetcher and Saga. |
| Response | Applies timeout, uses permitted cached information, requests a manual decision, and compensates reservations when required. |
| Measure | The operation does not block indefinitely and remains within the 90-second limit. |

### QS-10: National protocol activation

| Element | Scenario |
|---|---|
| Source | CNE Coordinator |
| Stimulus | Activates a national protocol. |
| Environment | Several institutions are operating. |
| Artifact | CNE Protocol Service and Kafka. |
| Response | Versions, publishes, and applies priorities without manual confirmation by each institution. |
| Measure | Every consuming institution receives the update; the exact time threshold remains subject to client validation. |

### QS-11: Analytical-plane failure

| Element | Scenario |
|---|---|
| Source | ClickHouse or analytical worker |
| Stimulus | Stops responding. |
| Environment | Active incidents exist. |
| Artifact | Operational and analytical planes. |
| Response | Registration and dispatch continue; events remain available for replay and views indicate delay. |
| Measure | Zero operational-flow interruptions and complete projection recovery. |

### QS-12: Contract evolution

| Element | Scenario |
|---|---|
| Source | Development team |
| Stimulus | Adds an optional field to an event. |
| Environment | Producers and consumers of different versions coexist. |
| Artifact | Schema Registry and consumers. |
| Response | Older consumers ignore the field, while newer consumers use it when present. |
| Measure | Zero events rejected because of backward incompatibility. |

### QS-13: Historical audit query

| Element | Scenario |
|---|---|
| Source | Authorized auditor |
| Stimulus | Requests records from the previous five years. |
| Environment | Normal operation. |
| Artifact | Append-only projection and MinIO WORM. |
| Response | Generates a complete, traceable, and authorized export. |
| Measure | 100% of applicable records are retrievable and verifiable. |

# Risks and Technical Debt

| ID | Risk or debt | Impact | Mitigation / required action |
|---|---|---|---|
| RT-01 | ADR-0002 contradicts the operational scope of the RFP and C4 models. | Ambiguous scope and incompatible decisions. | Update or supersede it, limiting ETL/ELT to the analytical plane. |
| RT-02 | Incorrect CNE Coordinator label in C4 Level 1. | Stakeholder and responsibility confusion. | Correct the `.drawio` source and regenerate the PNG. |
| RT-03 | Inconsistent cache TTL: 30 s in C4 Level 3 and 5 s in the topology. | Risk of dispatching with stale information. | Adopt TTL ≤ 5 s for resources and update C4 Level 3. |
| RT-04 | Store-specific RPO and RTO values are undefined. | Recovery cannot be verified. | Create an RPO/RTO matrix and recovery tests per service. |
| RT-05 | Complexity of multiple persistence technologies. | Higher operational load and learning curve. | Standardize operations, observability, backups, and runbooks; reduce engines if testing proves a store unnecessary. |
| RT-06 | On-premise capacity and lack of immediate elasticity. | Saturation during national emergencies. | Load testing, reserved capacity, planned scaling, and early procurement. |
| RT-07 | VPN as a bottleneck or single point of failure. | Loss of institutional access. | Redundancy, load balancing, failover testing, and tunnel monitoring. |
| RT-08 | Five-year Kafka retention may be expensive. | Excessive storage use and slow recovery. | Define per-topic retention and use MinIO WORM for long-term legal archival. |
| RT-09 | “Kafka as source of truth” is not bounded by domain. | Confusion between transport, event store, and system of record. | Define authoritative events, read models, and replay policies per bounded context. |
| RT-10 | No formal C4 deployment view exists yet. | Difficult validation of availability and network design. | Create a deployment diagram with nodes, zones, VPN, storage, and routes. |
| RT-11 | Complete data-classification model is missing. | Risk of exposure or excessive retention. | Create a data catalog, sensitivity levels, and minimization rules. |
| RT-12 | Complex offline conflicts. | Contradictory incident or resource states. | Define per-aggregate rules, convergence tests, and a manual-resolution queue. |
| RT-13 | Dependence on heterogeneous institutional systems. | Timeouts, incompatible formats, and incomplete data. | Adapters, contracts, contract tests, fallback, and institution-specific monitoring. |
| RT-14 | Technology versions and licenses must be reviewed before production. | Support, security, or legal-compatibility risk. | Maintain an SBOM, license review, patching, and upgrade policy. |

# Glossary

| Term | Definition |
|---|---|
| ABAC | Access control based on attributes such as institution, jurisdiction, sensitivity, and purpose. |
| ADR | Record of an architectural decision, its context, alternatives, and consequences. |
| Operational audit log | Chronological, immutable record of actions performed on incidents. |
| Bounded Context | Domain boundary within which a model and its rules have consistent meaning. |
| CDC | Capture of data changes to propagate modifications to events or projections. |
| CQRS | Separation of models and paths for write commands and read queries. |
| Data warehouse | Store optimized for analytical queries and historical aggregations. |
| Database-per-service | Principle under which each service owns and controls its own data store. |
| ETL/ELT | Extract, transform, and load processes primarily intended for analytics. |
| Event Sourcing | Persistence of change history as a sequence of immutable events. |
| Idempotency | Property that allows an operation to be repeated without additional effects. |
| Institutional incident | Event requiring formal intervention by at least one participating institution. |
| KEDA | Kubernetes component that scales workloads according to events or queue metrics. |
| Heat map | Territorial visualization of incident concentration, type, and intensity. |
| Outbox | Pattern that stores the domain change and outgoing message in one local transaction. |
| RBAC | Role-based access control. |
| RLS | Row-level security within a database. |
| Saga | Sequence of coordinated local transactions with compensating actions. |
| Institutional SLA | Maximum tolerated response or dispatch time by event and institution. |
| System of record | System that stores the authoritative version of data. |
| Derived data | Data that can be rebuilt from a system of record, such as caches and projections. |
| WORM | Write-once-read-many storage that prevents modification during retention. |
