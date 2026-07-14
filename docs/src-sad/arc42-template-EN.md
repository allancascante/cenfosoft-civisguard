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

## Quality Goals

## Stakeholders

| Role/Name    | Contact         | Expectations        |
|--------------|-----------------|---------------------|
| *\<Role-1\>* | *\<Contact-1\>* | *\<Expectation-1\>* |
| *\<Role-2\>* | *\<Contact-2\>* | *\<Expectation-2\>* |

# Architecture Constraints

# Context and Scope

## Business Context

**\<Diagram or Table\>**

**\<optionally: Explanation of external domain interfaces\>**

## Technical Context

**\<Diagram or Table\>**

**\<optionally: Explanation of technical interfaces\>**

**\<Mapping Input/Output to Channels\>**

# Solution Strategy

# Building Block View

## Whitebox Overall System

***\<Overview Diagram\>***

Motivation  
*\<text explanation\>*

Contained Building Blocks  
*\<Description of contained building block (black boxes)\>*

Important Interfaces  
*\<Description of important interfaces\>*

### \<Name black box 1\>

*\<Purpose/Responsibility\>*

*\<Interface(s)\>*

*\<(Optional) Quality/Performance Characteristics\>*

*\<(Optional) Directory/File Location\>*

*\<(Optional) Fulfilled Requirements\>*

*\<(optional) Open Issues/Problems/Risks\>*

### \<Name black box 2\>

*\<black box template\>*

### \<Name black box n\>

*\<black box template\>*

### \<Name interface 1\>

…​

### \<Name interface m\>

## Level 2

### White Box *\<building block 1\>*

*\<white box template\>*

### White Box *\<building block 2\>*

*\<white box template\>*

…​

### White Box *\<building block m\>*

*\<white box template\>*

## Level 3

### White Box \<\_building block x.1\_\>

*\<white box template\>*

### White Box \<\_building block x.2\_\>

*\<white box template\>*

### White Box \<\_building block y.1\_\>

*\<white box template\>*

# Runtime View

## \<Runtime Scenario 1\>

- *\<insert runtime diagram or textual description of the scenario\>*

- *\<insert description of the notable aspects of the interactions
  between the building block instances depicted in this diagram.\>*

## \<Runtime Scenario 2\>

## …​

## \<Runtime Scenario n\>

# Deployment View

## Infrastructure Level 1

***\<Overview Diagram\>***

Motivation  
*\<explanation in text form\>*

Quality and/or Performance Features  
*\<explanation in text form\>*

Mapping of Building Blocks to Infrastructure  
*\<description of the mapping\>*

## Infrastructure Level 2

### *\<Infrastructure Element 1\>*

*\<diagram + explanation\>*

### *\<Infrastructure Element 2\>*

*\<diagram + explanation\>*

…​

### *\<Infrastructure Element n\>*

*\<diagram + explanation\>*

# Cross-cutting Concepts

## *\<Concept 1\>*

*\<explanation\>*

## *\<Concept 2\>*

*\<explanation\>*

…​

## *\<Concept n\>*

*\<explanation\>*

# Architecture Decisions

The decisions described in this section summarize the main architectural choices for **CivisGuard Analytics**. Each decision should later be formalized through an **ADR** (*Architecture Decision Record*) documenting:

- The context.
- The alternatives considered.
- The selected decision.
- The consequences.
- The accepted risks.

The design assumes that no single mechanism can simultaneously optimize availability, consistency, performance, simplicity, and scalability. Therefore, the architecture divides the system according to the criticality and nature of each workload, making the *trade-offs* explicit.

This separation follows the principle of distinguishing between operational systems, analytical systems, systems of record, and derived data systems.

---

## DD-01: Hybrid Event-Driven Architecture

CivisGuard will use an event-driven architecture as the primary integration mechanism between its components.

The following actions will produce persistent domain events:

- Incident registration.
- Incident classification.
- Resource dispatch.
- Escalation.
- Status changes.
- Incident closure.
- Activation of national emergency protocols.

Operations that require an immediate response to the user, such as registering, classifying, or confirming a dispatch, will be executed through **synchronous APIs**.

After the operation has been validated and persisted, its consequences will be distributed asynchronously through the event bus.

This combination avoids relying on long chains of synchronous calls between institutions and allows consumers to process information at their own pace.

---

## DD-02: Separation Between the Operational and Analytical Planes

The platform will explicitly separate two types of processing:

- **Operational plane:** incident registration, classification, dispatch, coordination, and status updates.
- **Analytical plane:** heat maps, reports, historical analysis, and preventive territorial intelligence.

The operational plane will contain the authoritative systems of record. The analytical plane will be built through projections and derived data generated from operational events.

A variation of the **CQRS** (*Command Query Responsibility Segregation*) pattern will be applied:

- The write model will enforce business rules and consistency constraints.
- The read models will be optimized for geographic queries, reporting, and historical analysis.
- Analytical queries will not run directly against transactional databases.

This separation prevents expensive historical queries from affecting the system’s ability to register or dispatch incidents.

As a consequence, the architecture introduces controlled data duplication and eventual consistency between the operational state and the analytical views.

The term **ETL** will be reserved for preparing and transforming analytical information. Operational propagation between services will be performed through domain events rather than ETL processes.

---

## DD-04: Immutable Audit Log with Cryptographic Verification

The operational audit log will be append-only. No user, administrator, or service will be allowed to modify or delete previously confirmed events.

Each entry will include at least:

- Event identifier.
- Incident identifier.
- Identity of the public official or service.
- Institution.
- Action performed.
- Justification.
- Date and time in UTC.
- Correlation identifier.
- Aggregate version.
- Integrity hash.

The following mechanisms will be used to detect tampering:

- Hash chaining.
- Periodic block signing.
- Storage with immutable retention policies.

A public or distributed blockchain is not proposed because its complexity and operational cost are unnecessary for this context.

The audit log will store audit metadata and references to sensitive information. Clinical records and tactical information will not be indiscriminately duplicated within the immutable log.

---

## DD-05: At-Least-Once Delivery and Idempotency

The event bus will use **at-least-once delivery** semantics.

Because of retries, network failures, or consumer recovery, the same event may be received more than once.

All consumers must be idempotent by using:

- Unique event identifiers.
- Processed-event tracking.
- Uniqueness constraints.
- Aggregate versions.
- Idempotency keys for commands.
- Transactional operations within each service.

An end-to-end **exactly-once processing** guarantee will not be assumed across distributed systems.

To prevent inconsistent dual writes between a transactional database and the event bus, the **Transactional Outbox** pattern will be applied.

The domain modification and the insertion of the outgoing message will be performed within the same local transaction.

This pattern decouples the internal model from public event contracts and reduces inconsistencies between databases and event streams.

# Quality Requirements

Quality requirements define how CivisGuard must behave under normal operating conditions, demand spikes, partial failures, degraded connectivity, and future changes.

Reliability does not mean that no component will ever fail. Instead, it means that the system must continue providing its services when foreseeable failures occur. In addition to reliability, CivisGuard’s priority quality attributes are performance, security, integrity, scalability, operability, portability, and evolvability.

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

## Quality Requirements Overview

## Quality Scenarios

# Risks and Technical Debts

# Glossary

| Term         | Definition         |
|--------------|--------------------|
| *\<Term-1\>* | *\<definition-1\>* |
| *\<Term-2\>* | *\<definition-2\>* |
