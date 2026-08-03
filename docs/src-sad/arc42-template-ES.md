---
date: Julio 2025
title: "Plantilla ![arc42](images/arc42-logo.png)"
---

# 

**Acerca de arc42**

arc42, La plantilla de documentación para arquitectura de sistemas y de
software.

Versión de la plantilla 9.0-ES. (basada en la versión AsciiDoc), Julio 2025

Creada, mantenida y © por Dr. Peter Hruschka, Dr. Gernot Starke y
contribuyentes. Ver <https://arc42.org>.

# Introducción y Metas

## Vista de Requerimientos

**CivisGuard Analytics** es una plataforma nacional de misión crítica para la coordinación, el monitoreo y el análisis de incidentes interinstitucionales en Costa Rica. Su finalidad es proporcionar una visión compartida del territorio, coordinar el despacho de recursos, conservar la trazabilidad completa de cada caso y transformar los datos operativos en inteligencia preventiva.

La solución beneficia a las siguientes instituciones:

1. Sistema de Emergencias 9-1-1.
2. Fuerza Pública.
3. Caja Costarricense de Seguro Social (CCSS).
4. Cruz Roja Costarricense.
5. Cuerpo de Bomberos de Costa Rica.
6. Comisión Nacional de Prevención de Riesgos y Atención de Emergencias (CNE).

CivisGuard no es un canal público de denuncias ni sustituye los sistemas institucionales existentes. Se integra con ellos para consolidar información, coordinar responsabilidades y producir vistas operativas y analíticas diferenciadas.

Los procesos de negocio principales son:

- recepción, registro y clasificación de incidentes;
- despacho coordinado y seguimiento interinstitucional;
- actualización de disponibilidad y estado de recursos;
- activación de protocolos de emergencia nacional por parte del CNE;
- operación de unidades de campo bajo conectividad degradada;
- monitoreo territorial, mapas de calor y análisis de reincidencia;
- generación, consulta y exportación de bitácoras de auditoría.

La escala objetivo definida por el RFP es:

| Dimensión | Objetivo |
|---|---|
| Usuarios concurrentes | Entre 1.200 y 2.000 usuarios institucionales en horario pico. |
| Volumen inicial | Aproximadamente 30.000 incidentes mensuales en la Gran Área Metropolitana. |
| Proyección nacional | Hasta 80.000 incidentes mensuales. |
| Pico de ingreso | Hasta 250 incidentes por minuto. |
| Cobertura | Fase inicial en la GAM y expansión posterior a todo el territorio nacional. |
| Disponibilidad | Operación continua 24/7/365. |

### Nota de consistencia documental

El RFP y los modelos C4 de niveles 1, 2 y 3 incluyen funciones operativas de registro, coordinación y despacho en tiempo cercano al real. El ADR-0002, en cambio, describe una solución puramente analítica y por lotes que no participa en el despacho.

Para mantener este SAD congruente con el alcance contractual y los diagramas vigentes, el ADR-0002 se interpreta únicamente como la decisión aplicable a la **ingesta analítica desde sistemas institucionales heredados**. El plano operacional de CivisGuard conserva los servicios de incidentes, despacho, protocolos del CNE y sincronización offline. Esta interpretación deberá formalizarse mediante la actualización o sustitución del ADR-0002.

## Metas de Calidad

| Prioridad | Meta de calidad | Criterio principal |
|---:|---|---|
| 1 | Disponibilidad y tolerancia a fallos | Mantener operación 24/7/365 y limitar la indisponibilidad no planificada a un máximo de 2 minutos consecutivos. |
| 2 | Rendimiento operacional | Permitir el despacho de al menos un recurso para un incidente crítico en un máximo de 90 segundos. |
| 3 | Integridad y auditabilidad | Registrar todas las acciones relevantes en una bitácora inmutable, verificable y consultable durante al menos cinco años. |
| 4 | Seguridad y segregación institucional | Garantizar que cada institución y perfil acceda únicamente a la información necesaria para su función. |
| 5 | Resiliencia de conectividad | Permitir operación offline y sincronización posterior sin pérdida ni duplicación de registros. |
| 6 | Escalabilidad y evolutividad | Soportar los picos definidos, expansión nacional y despliegues independientes sin detener toda la plataforma. |

## Partes interesadas (Stakeholders)

| Rol/Nombre | Contacto o representación | Expectativas |
|---|---|---|
| MGPSP / DGTIC | Institución emisora y área solicitante | Gobierno arquitectónico, continuidad operativa, cumplimiento legal, visión nacional consolidada y control de costos. |
| Sistema 9-1-1 | Operadores y responsables de integración | Registro y clasificación inmediata de incidentes, despacho dentro del SLA y uso simple bajo presión. |
| Fuerza Pública | Supervisores, oficiales y equipos técnicos | Coordinación, trazabilidad, protección de información táctica y autonomía operativa. |
| CCSS | Supervisores, personal de respuesta y equipos técnicos | Coordinación de recursos, acceso mínimo necesario y protección de datos personales. |
| Cruz Roja Costarricense | Supervisores y unidades de campo | Disponibilidad de recursos, operación móvil y sincronización confiable. |
| Cuerpo de Bomberos | Supervisores y unidades operativas | Coordinación segura, autonomía funcional y respuesta ante incendios y materiales peligrosos. |
| CNE | Coordinador de emergencia nacional | Vista consolidada de recursos y capacidad de activar protocolos nacionales sin confirmación manual por institución. |
| Analista territorial | Analistas del MGPSP y de instituciones | Mapas de calor, reportes históricos, métricas y detección de reincidencia. |
| Auditor de la Contraloría | Contraloría General de la República | Bitácoras íntegras, exportables, verificables y disponibles durante al menos cinco años. |
| Administrador de accesos | Equipo de seguridad/IAM | Gestión centralizada de identidades, roles, atributos y segregación por institución. |
| Equipo de infraestructura del MGPSP | Operaciones on-premise | Despliegue reproducible, monitoreo, respaldo, recuperación, parches y capacidad suficiente. |
| Firma consultora Cenfosoft | Gustavo Castro, David Cárdenas, Allan Cascante y Randy Villareal | Diseñar, justificar, documentar y defender la arquitectura propuesta. |

# Restricciones de la Arquitectura

| Restricción | Descripción e impacto arquitectónico |
|---|---|
| Infraestructura exclusivamente on-premise | El ADR-001 excluye nube pública e híbrida. Todos los componentes se alojan y procesan en infraestructura física controlada por el MGPSP. |
| Acceso mediante VPN | El acceso institucional y operativo debe realizarse mediante una conexión VPN autorizada. No se exponen endpoints de negocio directamente a internet. |
| Independencia de proveedor | La Ley 9986 impide una dependencia tecnológica irrescindible. Se priorizan tecnologías open source, formatos abiertos, contenedores OCI e infraestructura reproducible. |
| Operación 24/7/365 | No se aceptan ventanas de mantenimiento que comprometan operaciones críticas. La indisponibilidad no planificada máxima es de 2 minutos consecutivos. |
| Despacho crítico | Un incidente crítico no puede permanecer sin al menos un recurso despachado por más de 90 segundos desde su registro y clasificación. |
| Actualización territorial | El mapa de calor debe reflejar un incidente activo en un máximo de 20 segundos desde su registro. |
| Segregación institucional | La información debe filtrarse por rol, institución, jurisdicción, participación en el incidente y sensibilidad. |
| Bitácora inmutable | Las acciones sobre un incidente no pueden modificarse ni eliminarse y deben conservarse para consulta histórica durante al menos cinco años. |
| Operación offline-first | Las unidades de campo deben registrar y actualizar información con conectividad limitada y sincronizarla posteriormente sin pérdida ni duplicación. |
| Soberanía y protección de datos | El tratamiento de datos personales debe cumplir la Ley 8968 y los principios de finalidad, proporcionalidad, seguridad y mínimo acceso. |
| Respeto a competencias institucionales | La solución debe respetar la Ley General de Policía, la Ley del Sistema Nacional de Emergencias, la autonomía de Bomberos y las competencias de las instituciones participantes. |
| Capacidad física limitada | El escalado está condicionado por el hardware on-premise disponible; el aprovisionamiento debe planificarse para picos y crecimiento nacional. |

# Alcance y Contexto del Sistema

## Contexto de Negocio

![C4 Nivel 1 — Contexto del Sistema](../c4-models/SystemContext-C4%20Nivel%201.drawio.png)

CivisGuard se encuentra en el centro de la coordinación interinstitucional. Recibe incidentes, intercambia disponibilidad y despachos con sistemas institucionales, proporciona interfaces para usuarios autorizados y exporta bitácoras para fiscalización.

### Actores y sistemas externos

| Actor o sistema | Relación con CivisGuard |
|---|---|
| Operador del 9-1-1 | Registra, clasifica y solicita el despacho de incidentes. |
| Supervisor institucional | Monitorea incidentes activos, administra recursos y coordina la participación de su institución. |
| Analista territorial | Consulta mapas de calor, reportes y métricas de reincidencia. |
| Oficial o unidad de campo | Actualiza estados, registra información desde campo y opera offline cuando es necesario. |
| Coordinador del CNE | Activa y administra protocolos de emergencia nacional. |
| Auditor de la Contraloría | Consulta y exporta bitácoras históricas para fiscalización. |
| Administrador de accesos | Gestiona identidades, roles, atributos y permisos institucionales. |
| Sistema 9-1-1 | Fuente principal de incidentes reportados por ciudadanos. |
| Sistemas institucionales | Proporcionan disponibilidad de recursos, confirmaciones y estados operativos. |
| Sistema de la Contraloría | Recibe exportaciones de bitácoras y evidencia de auditoría. |

> **Ajuste pendiente del diagrama:** el C4 Nivel 1 contiene una etiqueta duplicada para “Oficial o Unidad de Campo” donde una de las figuras representa realmente al “Coordinador de Emergencia Nacional”. El rol correcto se utiliza en este documento y debe corregirse en el archivo `.drawio`.

### Límites del alcance

Dentro del alcance:

- coordinación interinstitucional;
- registro y ciclo de vida del incidente;
- despacho y seguimiento de recursos;
- visibilidad diferenciada;
- mapas de calor y analítica territorial;
- bitácora y exportación para auditoría;
- sincronización offline;
- administración de identidades y accesos.

Fuera del alcance:

- recepción directa de denuncias ciudadanas;
- sustitución de los sistemas de despacho internos de cada institución;
- administración de infraestructura de telecomunicaciones pública;
- uso de nube pública o híbrida;
- automatización de decisiones que legalmente requieran intervención humana.

## Contexto Técnico

### Interfaces externas

| Interfaz | Dirección | Canal o protocolo | Información intercambiada | Consideraciones |
|---|---|---|---|---|
| Usuarios web | Usuario → CivisGuard | HTTPS/REST sobre VPN; JWT | Comandos, consultas, reportes y administración | Autenticación centralizada, RBAC/ABAC, rate limiting y auditoría. |
| Aplicación móvil | Bidireccional | HTTPS/REST sobre VPN y sincronización diferida | Eventos de campo, estados y confirmaciones | SQLite local, idempotencia, deduplicación y resolución de conflictos. |
| Sistema 9-1-1 | 9-1-1 → CivisGuard | API REST, webhook o integración contractual | Incidentes registrados y clasificados | Validación de esquema, autenticación mutua y claves de idempotencia. |
| Sistemas institucionales | Bidireccional | REST/gRPC para operación; ETL/ELT por lotes para analítica | Disponibilidad, reservas, confirmaciones y conjuntos históricos | Timeouts, fallback manual, contratos versionados y segregación. |
| Sistema de la Contraloría | CivisGuard → Contraloría | API o archivo firmado | Bitácoras y exportaciones históricas | Integridad, trazabilidad, autorización y formatos acordados. |
| Bus de eventos | Servicios y workers ↔ Kafka | Protocolo Kafka | Eventos de dominio y eventos de integración | Entrega al menos una vez, esquemas versionados y partición por incidente. |
| Persistencia interna | Servicio → almacén propietario | JDBC/SQL, S3 API o protocolo nativo | Datos del bounded context | Database-per-service; no se permiten consultas directas entre bases de servicios. |

### Mapeo de entradas y salidas a canales

| Entrada o salida | Productor | Consumidor | Canal |
|---|---|---|---|
| `IncidenteRegistrado` | Servicio de Incidentes | Despacho, mapa de calor, bitácora y analítica | Kafka |
| `RecursoDespachado` / `RecursosDespachados` | Servicio de Despacho | Bitácora, analítica, sistemas interesados | Kafka |
| `ProtocoloEmergenciaNacional` | Servicio de Protocolos CNE | Servicios operativos y workers | Kafka de alta prioridad lógica |
| `EventoCampo` | Servicio de Sincronización Offline | Servicios de dominio y bitácora | Kafka |
| Consulta de disponibilidad | Servicio de Despacho | Caché y sistemas institucionales | Redis/Valkey y REST |
| Exportación de auditoría | Servicio/worker de bitácora | Sistema de la Contraloría | API o archivo firmado |
| Datos históricos | Sistemas institucionales | Pipeline analítico | ETL/ELT por lotes |

# Estrategia de solución

## Estilo Arquitectónico Macro: Event-Driven Híbrido sobre Kubernetes On-Premise

La solución combina un plano operacional síncrono para comandos críticos con un plano asíncrono basado en eventos para integración, proyecciones, auditoría y analítica.

La arquitectura se ejecuta exclusivamente sobre un clúster de Kubernetes on-premise del MGPSP y se accede mediante VPN.

## Plano operacional

Los servicios de Incidentes, Despacho, Protocolos CNE y Sincronización Offline contienen la lógica de negocio principal. Exponen APIs contractuales a través del API Gateway y mantienen consistencia fuerte dentro de sus propios agregados y bases de datos.

Las operaciones que requieren respuesta inmediata utilizan REST o gRPC:

- registrar y clasificar incidentes;
- consultar disponibilidad;
- iniciar y confirmar despachos;
- activar protocolos nacionales;
- sincronizar operaciones offline.

Las transacciones que atraviesan instituciones o bounded contexts se coordinan mediante Sagas y acciones compensatorias.

## Plano asíncrono y analítico

Los eventos confirmados se publican en Apache Kafka. Los workers stateless consumen dichos eventos para:

- mantener el mapa de calor;
- construir la bitácora append-only;
- alimentar el data warehouse;
- actualizar cachés y proyecciones;
- generar inteligencia territorial.

La ingesta histórica proveniente de sistemas institucionales heredados puede realizarse mediante ETL/ELT programado. Esta ruta por lotes corresponde al alcance analítico del ADR-0002 y no sustituye el flujo operacional interno.

## Persistencia políglota distribuida

Se aplica database-per-service y cada bounded context elige el almacén adecuado:

- PostgreSQL para OLTP, reglas ACID y RLS;
- ClickHouse para OLAP y agregaciones territoriales;
- PostGIS para consultas geoespaciales;
- Redis/Valkey para disponibilidad y cachés geográficas;
- SQLite para operación offline;
- MinIO con Object Lock para evidencia y archivo WORM;
- Kafka como bus EDA y registro durable de eventos;
- Keycloak para identidades, roles y atributos.

## Kubernetes como plataforma de orquestación

Kubernetes proporciona:

- aislamiento y despliegue independiente por servicio;
- reinicio y reprogramación automática de contenedores;
- rolling updates;
- escalado horizontal;
- políticas de red;
- administración reproducible mediante manifiestos e infraestructura como código.

KEDA escala los workers según el retraso o tamaño de las colas de Kafka. El escalado está limitado por la capacidad física del entorno on-premise, por lo que debe acompañarse de planificación de capacidad.

## Seguridad por diseño

El API Gateway actúa como punto único de entrada y delega autenticación a Keycloak. La autorización combina RBAC y ABAC por institución, rol, jurisdicción, sensibilidad y participación en el incidente. Los datos se cifran en tránsito y en reposo, y toda acción sensible genera una entrada de auditoría.

# Vista de Bloques

## Sistema General de Caja Blanca

![C4 Nivel 2 — Contenedores](../c4-models/SystemContext-C4%20Nivel%202.drawio.png)

### Motivación

La división en contenedores separa canales de usuario, lógica operacional, procesamiento asíncrono y persistencia. Esto limita el radio de impacto de los fallos, permite escalar cada carga de manera independiente y evita que las consultas analíticas afecten las operaciones de registro y despacho.

### Bloques de construcción contenidos

| Bloque | Tecnología | Responsabilidad |
|---|---|---|
| Web App Institucional | React / TypeScript | Portal para operadores, supervisores y analistas. |
| App Móvil de Campo | React Native + SQLite | Operación de unidades de campo con soporte offline-first. |
| API Gateway | Kong o Tyk/Nginx | Entrada única, TLS, autenticación, autorización, rate limiting y enrutamiento. |
| IAM | Keycloak | Identidades, MFA, LDAP, RBAC/ABAC y JWT por institución. |
| Servicio de Incidentes | Node.js / Express | Registro, clasificación y ciclo de vida de incidentes. |
| Servicio de Despacho | Java / Spring Boot | Disponibilidad, reservas, Saga de despacho, confirmación y compensación. |
| Servicio de Protocolos CNE | Node.js / Express | Activación y distribución de protocolos nacionales. |
| Servicio de Sincronización Offline | Go | Recepción, deduplicación, validación y reconciliación de eventos de campo. |
| Bus de Eventos | Apache Kafka 3.7 | Integración EDA, retención durable y distribución de eventos. |
| Worker Mapa de Calor | Python / KEDA | Actualización de proyecciones territoriales en menos de 20 segundos. |
| Worker de Bitácora | Python / KEDA | Persistencia append-only y preparación de exportaciones. |
| Worker Analítica | Python / KEDA | Alimentación del data warehouse y métricas de reincidencia. |
| Persistencia operacional | PostgreSQL 16 | Datos ACID de incidentes, despacho, IAM y metadatos. |
| Almacén analítico | ClickHouse 24 | Reportes, mapas de calor e históricos. |
| Capa geoespacial | PostGIS 3.4 + Redis GEO | Zonas de riesgo, recursos cercanos e incidentes activos. |
| Archivo de evidencia | MinIO | Objetos, evidencia y exportaciones WORM. |

### Interfaces importantes

- HTTPS/REST entre clientes y API Gateway.
- REST/gRPC entre Gateway y servicios.
- Kafka para eventos de dominio e integración.
- JDBC/SQL únicamente entre cada servicio y su base propietaria.
- S3 API para MinIO.
- Redis/Valkey para cachés de disponibilidad y geoespaciales.
- API REST contractual con sistemas institucionales.
- ETL/ELT para conjuntos históricos destinados al plano analítico.

### Web App Institucional

**Propósito:** proporcionar vistas operativas y analíticas diferenciadas para operadores, supervisores y analistas.

**Interfaces:** HTTPS con API Gateway; actualización mediante consultas periódicas o canales autorizados de notificación.

**Características de calidad:** accesibilidad institucional, segregación por perfil, respuesta rápida y ausencia de lógica de autorización confiada únicamente al cliente.

### App Móvil de Campo

**Propósito:** permitir registro y actualización de incidentes y recursos desde campo.

**Interfaces:** API Gateway y Servicio de Sincronización Offline.

**Características de calidad:** almacenamiento local SQLite por hasta 30 días, cola durable, reintentos, idempotencia y trabajo con conectividad intermitente.

### API Gateway e IAM

**Propósito:** centralizar autenticación, autorización, TLS, límites de consumo, observabilidad de entrada y enrutamiento.

**Interfaces:** HTTPS/REST, gRPC interno, Keycloak/LDAP y JWT.

**Características de calidad:** alta disponibilidad, políticas consistentes, trazabilidad y ausencia de bypass hacia los servicios internos.

### Servicio de Incidentes

**Propósito:** registrar, clasificar y administrar el ciclo de vida del incidente.

**Interfaces:** REST a través del Gateway, PostgreSQL propietario, Transactional Outbox y Kafka.

**Requerimientos satisfechos:** registro inmediato, trazabilidad, segregación institucional y generación de `IncidenteRegistrado`.

### Servicio de Despacho

**Propósito:** coordinar la selección, reserva y confirmación de recursos entre instituciones.

**Interfaces:** REST, Redis/Valkey, sistemas institucionales, PostgreSQL y Kafka.

**Características de calidad:** confirmación dentro de 90 segundos, fallback manual, Saga orquestada e idempotencia.

### Servicio de Protocolos CNE

**Propósito:** validar y distribuir protocolos de emergencia nacional.

**Interfaces:** REST y Kafka.

**Características de calidad:** propagación sin confirmación manual institución por institución, control de acceso estricto y versionado de reglas.

### Servicio de Sincronización Offline

**Propósito:** reconciliar operaciones acumuladas por las unidades de campo.

**Interfaces:** App Móvil, PostgreSQL/almacén propietario y Kafka.

**Características de calidad:** deduplicación, orden lógico, validación de versiones y resolución explícita de conflictos.

### Workers de proyección

**Propósito:** construir vistas derivadas sin bloquear el plano operacional.

**Interfaces:** Kafka, ClickHouse, PostgreSQL append-only, PostGIS, Redis/Valkey y MinIO.

**Características de calidad:** escalado mediante KEDA, reprocesamiento, checkpoints e idempotencia.

## Nivel 2 — Persistencia y topología de datos

Archivo fuente: [`Topologia-datos.drawio`](../c4-models/Topologia-datos.drawio)

La topología se organiza en capas:

1. clientes web, móviles y sistemas externos;
2. API Gateway e IAM sobre VPN;
3. microservicios alineados a bounded contexts;
4. bus EDA Apache Kafka;
5. persistencia políglota distribuida.

### Bounded contexts y almacenes

| Bounded Context | Almacén principal | Modelo de consistencia |
|---|---|---|
| BC1 Incidentes | PostgreSQL, particionado por `institucion_id` | ACID dentro del agregado; eventos hacia otros contextos. |
| BC2 Despacho y Recursos | PostgreSQL + Redis GEO | ACID local; Saga para coordinación interinstitucional. |
| BC3 Bitácora y Auditoría | Kafka + PostgreSQL append-only + MinIO WORM | Inmutabilidad, verificación y proyección consultable. |
| BC4 Analítica y BI | ClickHouse | Consistencia eventual y cargas OLAP. |
| BC5 Geoespacial | PostGIS + Redis GEO | Proyecciones de baja latencia y fuente geoespacial persistente. |
| BC6 IAM | Keycloak + almacén PostgreSQL | Consistencia fuerte para identidades y permisos. |
| BC7 Sincronización Offline | SQLite local + servicio de sincronización | Convergencia posterior, idempotencia y resolución de conflictos. |
| BC9 Archivos y Evidencia | PostgreSQL de metadatos + MinIO | Integridad de metadatos y retención WORM. |

## Nivel 3 — Servicio de Despacho

![C4 Nivel 3 — Componentes del Servicio de Despacho](../c4-models/SystemContext-C4%20Nivel%203.drawio.png)

El Servicio de Despacho se divide mediante CQRS en un lado de consulta y un lado de comando.

### Lado Query

| Componente | Responsabilidad |
|---|---|
| Availability Query Handler | Recibe consultas de disponibilidad y consulta primero la caché. |
| Resource Availability Fetcher | Consulta los sistemas institucionales cuando no existe información suficientemente fresca. |
| Availability Cache | Mantiene el último estado conocido de recursos por institución. |
| Fallback Alert Publisher | Notifica al operador o supervisor cuando una institución no responde y se requiere decisión manual. |

> La topología de datos define un TTL de 5 segundos para la caché de recursos del BC2, mientras que el C4 Nivel 3 indica 30 segundos. Para el despacho crítico se adopta como objetivo **TTL ≤ 5 segundos** y el diagrama de componentes debe actualizarse para eliminar la discrepancia.

### Lado Command

| Componente | Responsabilidad |
|---|---|
| Dispatch Command Handler | Valida el comando e inicia la Saga de coordinación. |
| Dispatch Saga Orchestrator | Solicita reservas, espera confirmaciones y decide confirmar o compensar. |
| Dispatch Confirmation Handler | Confirma el despacho global, persiste el resultado y publica `RecursosDespachados`. |
| Compensation Handler | Libera reservas y notifica el fallo cuando ocurre timeout o rechazo. |
| Dispatch Repository | Único componente autorizado para escribir en la base de datos de despacho. |

### Dependencias externas del Servicio de Despacho

- API Gateway para comandos y consultas autenticadas.
- Sistemas institucionales para disponibilidad, reserva y confirmación.
- Redis/Valkey para lectura de disponibilidad.
- PostgreSQL para estado del despacho.
- Kafka para eventos confirmados.
- Operador o supervisor para fallback manual.

# Vista de Ejecución

## Escenario 1: Registro de incidente y actualización del mapa de calor

1. El operador registra y clasifica un incidente desde la Web App.
2. El API Gateway valida el token, la institución, el rol y los límites de consumo.
3. El Servicio de Incidentes valida las reglas y persiste el incidente junto con una entrada de outbox en una transacción local.
4. Un publicador entrega `IncidenteRegistrado` a Kafka.
5. El Worker Mapa de Calor consume el evento y actualiza la proyección geoespacial.
6. El Worker de Bitácora agrega el evento al registro append-only.
7. El Worker Analítica actualiza las proyecciones del data warehouse.
8. Las vistas autorizadas reflejan el incidente en un máximo de 20 segundos.

Aspectos notables:

- la confirmación del registro no depende de ClickHouse;
- los consumidores son idempotentes;
- una falla analítica no impide registrar el incidente;
- el evento se particiona por `incidentId` para preservar el orden del caso.

## Escenario 2: Despacho coordinado de un incidente crítico

1. El operador consulta recursos disponibles.
2. Availability Query Handler consulta Redis/Valkey.
3. Ante datos ausentes o vencidos, Resource Availability Fetcher consulta los sistemas institucionales.
4. Si una institución no responde, Fallback Alert Publisher solicita decisión manual.
5. El operador envía el comando de despacho.
6. Dispatch Command Handler inicia la Saga.
7. Dispatch Saga Orchestrator solicita reservas a las instituciones competentes.
8. Dispatch Confirmation Handler recibe las confirmaciones.
9. Si se cumplen las condiciones dentro de 90 segundos, el despacho se persiste y se publica `RecursosDespachados`.
10. Si ocurre un timeout o rechazo, Compensation Handler libera reservas y notifica al operador.

Aspectos notables:

- no existe una transacción ACID global;
- la consistencia se alcanza mediante Saga, compensación e idempotencia;
- el repositorio de despacho es el único escritor de su base;
- el fallo de una institución no debe bloquear indefinidamente a las demás.

## Escenario 3: Operación y sincronización offline

1. La unidad de campo pierde conectividad.
2. La App Móvil conserva las operaciones en SQLite con identificadores únicos, versión y orden local.
3. La aplicación continúa mostrando confirmaciones locales y mantiene una cola durable.
4. Al recuperar la conexión VPN, envía las operaciones pendientes al Servicio de Sincronización Offline.
5. El servicio deduplica, valida versiones y aplica reglas de conflicto.
6. Las operaciones aceptadas se publican como `EventoCampo`.
7. Los conflictos que no pueden resolverse automáticamente se remiten a un supervisor.

Aspectos notables:

- no se utiliza “última escritura gana” para transiciones críticas;
- las operaciones confirmadas por el servidor se eliminan de la cola local;
- el almacenamiento local conserva hasta 30 días según la topología vigente.

## Escenario 4: Activación de un Protocolo de Emergencia Nacional

1. El Coordinador CNE autenticado activa un protocolo.
2. El Servicio de Protocolos CNE valida permisos, vigencia y versión.
3. Persiste la activación y publica `ProtocoloEmergenciaNacional`.
4. Los servicios operativos actualizan sus reglas y prioridades.
5. Los workers y vistas reflejan el estado de emergencia.
6. La bitácora registra quién activó el protocolo y su justificación.

Aspectos notables:

- no se requiere confirmación manual institución por institución;
- los consumidores deben poder recibir nuevamente el evento sin duplicar efectos;
- la versión del protocolo permite auditoría y reversión controlada.

## Escenario 5: Ingesta analítica por lotes desde sistemas heredados

1. Una institución genera un conjunto histórico según el contrato acordado.
2. El archivo o lote se transmite por un canal seguro.
3. El pipeline valida esquema, integridad, institución y periodo.
4. Los datos se normalizan y se cargan en el plano analítico.
5. Se producen métricas, reportes y mapas históricos.
6. Los errores se aíslan para reproceso sin afectar sistemas operativos.

Este escenario materializa el alcance analítico del ADR-0002 sin eliminar las capacidades operativas de CivisGuard.

## Escenario 6: Exportación de bitácoras para la Contraloría

1. Un auditor autorizado solicita un rango de incidentes.
2. El servicio valida permisos, finalidad y filtros institucionales.
3. Se consultan las proyecciones append-only y los objetos archivados.
4. Se genera una exportación con metadatos de integridad y trazabilidad.
5. El archivo se almacena temporalmente en MinIO y se entrega por API o canal acordado.
6. La solicitud y descarga quedan registradas en la bitácora.

# Vista de Despliegue

## Nivel de infraestructura 1

Archivo de referencia: [`Topologia-datos.drawio`](../c4-models/Topologia-datos.drawio)

### Motivación

El despliegue debe preservar la soberanía de los datos, cumplir la decisión on-premise y sostener operación continua. Kubernetes desacopla el software del hardware específico y permite reconstruir el entorno dentro de la infraestructura institucional.

### Características de Calidad y Rendimiento

- acceso exclusivo mediante VPN;
- ausencia de endpoints de negocio públicos;
- redundancia de componentes críticos;
- Kafka con factor de replicación 3 y `min.insync.replicas=2`;
- escalado de workers con KEDA;
- separación de cargas OLTP, OLAP, geoespaciales y de objetos;
- almacenamiento WORM para exportaciones y evidencia;
- monitoreo centralizado;
- respaldo y recuperación probados;
- capacidad física dimensionada para 2.000 usuarios y 250 incidentes por minuto.

### Mapeo de bloques a infraestructura

| Infraestructura | Bloques desplegados |
|---|---|
| Perímetro VPN institucional | Acceso de usuarios, unidades y sistemas externos. |
| Balanceadores / entrada Kubernetes | API Gateway y terminación TLS. |
| Clúster Kubernetes on-premise | Microservicios, workers, Web App, conectores y componentes de integración. |
| Plataforma IAM | Keycloak, LDAP/MFA y almacenamiento de identidades. |
| Clúster Kafka | Tópicos, KRaft, Schema Registry y conectores CDC. |
| Clúster PostgreSQL/PostGIS | Bases propietarias de servicios, RLS y datos geoespaciales. |
| Clúster ClickHouse | Data warehouse y consultas OLAP. |
| Redis/Valkey | Cachés de disponibilidad y geoespaciales. |
| MinIO | Objetos, evidencia, exportaciones y retención WORM. |
| Dispositivos móviles | App React Native y SQLite local. |
| Plataforma de observabilidad | Prometheus, Grafana, logs centralizados y alertas. |

## Nivel de Infraestructura 2

### Perímetro, VPN y acceso

Todo acceso atraviesa la VPN institucional. El API Gateway es el único punto de entrada a los servicios. Las políticas de red de Kubernetes impiden acceso directo desde clientes a bases de datos o microservicios.

Riesgos principales:

- la VPN puede convertirse en cuello de botella o punto único de fallo;
- las unidades remotas dependen de la disponibilidad del canal;
- se requiere redundancia de concentradores VPN y monitoreo de capacidad.

### Clúster Kubernetes on-premise

El clúster ejecuta los servicios en réplicas independientes y distribuidas entre nodos físicos. Debe configurarse con:

- control plane altamente disponible;
- múltiples worker nodes;
- anti-affinity para réplicas críticas;
- PodDisruptionBudgets;
- rolling updates;
- cuotas y límites;
- almacenamiento persistente redundante;
- NetworkPolicies.

### Apache Kafka y contratos

Kafka utiliza KRaft, factor de replicación 3 y al menos dos réplicas sincronizadas. Apicurio Schema Registry administra la compatibilidad de eventos. Kafka Connect y Debezium construyen proyecciones y CDC cuando corresponda.

La retención operativa y la retención legal no deben confundirse: Kafka conserva el historial requerido por la estrategia de eventos, mientras MinIO WORM y las proyecciones append-only proporcionan archivo de largo plazo y exportación.

### Persistencia políglota

Cada almacén debe desplegarse con respaldo y recuperación acordes con su criticidad. Los objetivos RPO/RTO específicos por motor todavía deben formalizarse.

- PostgreSQL/PostGIS: replicación, failover y respaldos consistentes.
- ClickHouse: réplicas y particiones para consultas históricas.
- Redis/Valkey: alta disponibilidad; nunca es la única fuente persistente.
- MinIO: Object Lock, versionado y replicación/erasure coding.
- SQLite: cifrado del dispositivo, retención local y borrado tras confirmación.

### Observabilidad y operación

Prometheus y Grafana consolidan métricas. Los logs y trazas deben incluir `correlationId`, `incidentId`, institución y servicio, evitando datos personales innecesarios.

Indicadores mínimos:

- disponibilidad y tasa de error;
- latencia p95/p99;
- tiempo de despacho;
- retraso de consumidores;
- profundidad de colas;
- edad de proyecciones;
- fallos de sincronización;
- conflictos offline;
- accesos denegados;
- estado de réplicas y respaldos.

# Conceptos Transversales (Cross-cutting)

## Seguridad e Identidad Federada con JWT

La seguridad es un concepto transversal obligatorio en toda la solución. Todos los microservicios deben validar identidad y autorización antes de procesar cualquier operación, tanto en APIs síncronas como en flujos asíncronos por eventos.

**Reglas de arquitectura:**

1. Todo request HTTP debe incluir un JWT válido (firma, vigencia, emisor, audiencia).
2. El `API Gateway` valida el JWT como primer control, y cada microservicio vuelve a validar como defensa en profundidad (*zero trust interno*).
3. Todo evento publicado en Kafka debe transportar contexto de identidad (JWT o token de delegación equivalente) en headers del mensaje.
4. Todo consumidor Kafka debe validar ese token antes de procesar el evento.
5. Los claims mínimos obligatorios son: `sub` (usuario/servicio emisor), `rol`, `institucion_id`, `iat`, `exp`, `iss`, `aud`.
6. Cada evento debe preservar correlación entre identidad y operación (`event_id`, `correlation_id`, `causation_id`) para trazabilidad y auditoría.

**Aplicación sobre el dominio:**

- La autorización RBAC institucional se deriva de `rol` + `institucion_id` (ver ADR-0004).
- En solicitudes de apoyo del CNE, la identidad del emisor del evento debe mantenerse verificable de extremo a extremo (ver ADR-0005).

**Implicaciones operativas y de cumplimiento:**

- Rechazo automático de tokens expirados, inválidos o sin claims obligatorios.
- Registro auditable de validaciones y rechazos en bitácora inmutable.
- Cumplimiento de segregación institucional y principio de mínimo privilegio.

## *\<Otros conceptos transversales\>*

*\<Agregar aquí otros conceptos globales: observabilidad, resiliencia, versionado de eventos, etc.\>*

# Decisiones de Diseño

Las decisiones descritas en esta sección resumen las principales elecciones arquitectónicas de **CivisGuard Analytics**. Sus detalles y alternativas deben mantenerse en ADRs.

El diseño reconoce que ningún mecanismo optimiza simultáneamente disponibilidad, consistencia, rendimiento, simplicidad y escalabilidad. Por ello, separa cargas y hace explícitos los trade-offs, siguiendo los principios de sistemas operacionales, sistemas analíticos, sistemas de registro y datos derivados descritos en *Designing Data-Intensive Applications, 2nd Edition*.

## Resumen y trazabilidad de ADRs

| ADR | Estado actual | Aplicación en este SAD |
|---|---|---|
| ADR-001 Entorno Operativo | Propuesto | Infraestructura exclusivamente on-premise y acceso mediante VPN. |
| ADR-0002 Arquitectura Orientada al Análisis | Propuesto, requiere aclaración | Se limita a ingesta ETL/ELT y al plano analítico; no elimina el plano operacional exigido por el RFP y los C4. |
| ADR-003 Persistencia Políglota Distribuida | Propuesto | Database-per-service, open source, consistencia local y eventos entre contextos. |

## DD-01: Arquitectura híbrida orientada a eventos

CivisGuard utiliza APIs síncronas para comandos que requieren respuesta inmediata y Kafka para distribuir sus consecuencias.

Generan eventos persistentes:

- registro y clasificación de incidentes;
- despacho y compensación;
- escalamiento y cambio de estado;
- cierre;
- activación de protocolos nacionales;
- sincronización de campo.

Esta combinación evita cadenas síncronas largas y permite que los consumidores procesen información a su propio ritmo. Las vistas derivadas pueden ser eventualmente consistentes, pero el plano operacional no depende de su disponibilidad.

## DD-02: Separación entre el plano operacional y el plano analítico

El plano operacional contiene los sistemas de registro autoritativos para incidentes, despachos y protocolos. El plano analítico se construye mediante eventos, CDC y ETL/ELT.

Se aplica CQRS:

- modelos de escritura para reglas e invariantes;
- modelos de lectura para mapas, reportes e históricos;
- consultas analíticas fuera de las bases transaccionales.

La consecuencia es duplicación controlada y consistencia eventual, a cambio de aislamiento de cargas y mejor escalabilidad.

## DD-03: Persistencia políglota distribuida

Cada microservicio posee su almacén y no accede directamente al de otros. La tecnología se selecciona por perfil de carga y debe ser open source y sustituible.

Se utilizan PostgreSQL, ClickHouse, PostGIS, Redis/Valkey, Kafka, MinIO, SQLite y Keycloak de acuerdo con la topología de datos.

La consistencia fuerte se garantiza dentro del agregado; la coordinación entre servicios usa Saga, eventos, outbox e idempotencia.

## DD-04: Bitácora inmutable con verificación criptográfica

La bitácora operativa es de solo anexado. Ningún usuario, administrador o servicio puede modificar o eliminar entradas confirmadas.

Cada entrada incluye:

- identificador del evento;
- identificador del incidente;
- identidad del funcionario o servicio;
- institución;
- acción;
- justificación;
- fecha y hora UTC;
- identificador de correlación;
- versión del agregado;
- hash de integridad.

Se utilizan encadenamiento de hashes, firma periódica y almacenamiento con retención inmutable. No se propone una blockchain pública o distribuida.

La bitácora almacena metadatos de auditoría y referencias controladas. No se duplicará indiscriminadamente información personal del incidente ni información táctica dentro del registro inmutable.

## DD-05: Entrega al menos una vez e idempotencia

Kafka utiliza semántica de entrega al menos una vez. Un evento puede recibirse varias veces debido a reintentos o recuperación.

Los consumidores implementan:

- identificadores únicos;
- registro de eventos procesados;
- restricciones de unicidad;
- versiones de agregado;
- claves de idempotencia;
- transacciones locales.

No se asume exactamente una vez de extremo a extremo. Transactional Outbox evita escrituras duales inconsistentes entre la base transaccional y Kafka.

## DD-06: Entorno exclusivamente on-premise

Todos los componentes se ejecutan en infraestructura del MGPSP y se acceden mediante VPN. Kubernetes mantiene portabilidad dentro de hardware compatible, pero no implica que la solución se despliegue en nube pública.

Beneficios:

- soberanía y control;
- perímetro reducido;
- cumplimiento con políticas institucionales.

Costos:

- menor elasticidad;
- mayor responsabilidad operativa;
- dependencia de capacidad, energía, red y recuperación institucional.

## DD-07: Offline-first en unidades de campo

La App Móvil utiliza SQLite y una cola local durable. Al reconectar, el Servicio de Sincronización Offline deduplica, valida y reconcilia.

No se aplica “última escritura gana” a estados críticos. Los conflictos de negocio se resuelven mediante versiones, reglas de dominio o revisión manual.

## DD-08: Segregación institucional mediante RBAC, ABAC y RLS

La autorización se determina por rol e información contextual. Keycloak emite identidades y atributos; los servicios validan permisos y las bases multiinstitucionales aplican RLS o particionamiento.

Ninguna decisión de seguridad depende exclusivamente de la interfaz de usuario.

# Requerimientos de Calidad

Los requerimientos de calidad determinan cómo debe comportarse CivisGuard bajo condiciones normales, picos de demanda, fallos parciales, conectividad degradada y evolución tecnológica.

La confiabilidad no implica ausencia de fallos, sino continuidad del servicio frente a fallos previsibles.

```text
Calidad de CivisGuard Analytics
├── Confiabilidad
│   ├── Disponibilidad 24/7/365
│   ├── Tolerancia a fallos
│   ├── Durabilidad de datos
│   └── Recuperación
├── Rendimiento
│   ├── Despacho dentro del SLA
│   ├── Propagación de eventos
│   ├── Actualización del mapa
│   └── Capacidad en picos de demanda
├── Seguridad y privacidad
│   ├── Autenticación
│   ├── Segregación institucional
│   ├── Mínimo privilegio
│   └── Protección de datos sensibles
├── Integridad y auditabilidad
│   ├── Bitácora inmutable
│   ├── Trazabilidad de extremo a extremo
│   ├── Detección de alteraciones
│   └── Exportación histórica
├── Resiliencia de conectividad
│   ├── Operación offline
│   ├── Sincronización
│   ├── Deduplicación
│   └── Resolución de conflictos
├── Escalabilidad
│   ├── Usuarios concurrentes
│   ├── Incidentes por minuto
│   └── Expansión nacional
├── Mantenibilidad
│   ├── Operabilidad
│   ├── Simplicidad
│   ├── Observabilidad
│   └── Evolución de contratos
└── Portabilidad
    ├── Independencia de proveedor
    ├── Infraestructura reproducible
    └── Uso de estándares abiertos
```

## Vista General de Requerimientos de Calidad

| ID | Atributo | Requerimiento verificable | Prioridad |
|---|---|---|---|
| RC-01 | Disponibilidad | Operación 24/7/365; indisponibilidad no planificada ≤ 2 minutos consecutivos. | Crítica |
| RC-02 | Rendimiento | Despacho de al menos un recurso para incidentes críticos ≤ 90 segundos. | Crítica |
| RC-03 | Oportunidad | Incidente visible en el mapa de calor ≤ 20 segundos desde su registro. | Crítica |
| RC-04 | Capacidad | Soportar 2.000 usuarios concurrentes y 250 incidentes por minuto. | Crítica |
| RC-05 | Integridad | Cero pérdida de comandos confirmados y cero duplicación de efectos de negocio por reintentos. | Crítica |
| RC-06 | Seguridad | Cero exposición de datos no autorizados entre instituciones o perfiles. | Crítica |
| RC-07 | Auditabilidad | Toda acción relevante incluye actor, institución, justificación y marca UTC. | Crítica |
| RC-08 | Inmutabilidad | Las entradas confirmadas no pueden modificarse ni eliminarse. | Crítica |
| RC-09 | Retención | Bitácoras y exportaciones consultables durante al menos cinco años. | Alta |
| RC-10 | Offline | Operación local y sincronización posterior sin pérdida ni duplicación. | Crítica |
| RC-11 | Autonomía | Cada institución configura reglas internas sin alterar las de otras. | Alta |
| RC-12 | Coordinación nacional | El CNE modifica prioridades sin confirmación manual por institución. | Crítica |
| RC-13 | Degradación controlada | Fallos del plano analítico no interrumpen registro ni despacho. | Crítica |
| RC-14 | Evolutividad | Productores y consumidores compatibles durante evolución de contratos. | Alta |
| RC-15 | Operabilidad | Detección de fallos, lag, saturación y degradación mediante métricas y alertas. | Alta |
| RC-16 | Portabilidad | Despliegue reproducible sobre infraestructura on-premise compatible sin lock-in comercial. | Alta |
| RC-17 | Recuperabilidad | Fallo de una instancia o nodo no debe exceder el límite global de indisponibilidad. | Crítica |
| RC-18 | Privacidad | Datos personales minimizados, cifrados y accesibles únicamente para una finalidad autorizada. | Crítica |

## Escenarios de Calidad

### EC-01: Fallo de una instancia crítica

| Elemento | Escenario |
|---|---|
| Fuente | Infraestructura |
| Estímulo | Una instancia del Servicio de Incidentes o Despacho deja de responder. |
| Entorno | Emergencia activa y carga pico. |
| Artefacto | Servicio desplegado en Kubernetes. |
| Respuesta | El balanceador retira la instancia; Kubernetes reprograma una réplica y el tráfico continúa por instancias saludables. |
| Medida | Indisponibilidad visible ≤ 2 minutos y cero comandos confirmados perdidos. |

### EC-02: Registro y despacho crítico

| Elemento | Escenario |
|---|---|
| Fuente | Operador del 9-1-1 |
| Estímulo | Registra, clasifica y solicita despacho para un incidente crítico. |
| Entorno | Hasta 250 incidentes por minuto y 2.000 usuarios concurrentes. |
| Artefacto | Gateway, Incidentes, Despacho, Kafka y almacenes operativos. |
| Respuesta | El incidente se confirma y se coordina al menos un recurso. |
| Medida | Despacho confirmado ≤ 90 segundos. |

### EC-03: Actualización del mapa de calor

| Elemento | Escenario |
|---|---|
| Fuente | Servicio de Incidentes |
| Estímulo | Publica `IncidenteRegistrado`. |
| Entorno | Operación normal o pico. |
| Artefacto | Kafka, Worker Mapa de Calor y proyección geoespacial. |
| Respuesta | El consumidor procesa el evento y actualiza las vistas autorizadas. |
| Medida | Incidente visible ≤ 20 segundos. |

### EC-04: Acceso no autorizado

| Elemento | Escenario |
|---|---|
| Fuente | Usuario autenticado de una institución |
| Estímulo | Solicita información fuera de su rol, institución o finalidad. |
| Entorno | Operación normal. |
| Artefacto | Gateway, IAM, servicio y base. |
| Respuesta | Se deniega antes de serializar datos protegidos y se registra el intento. |
| Medida | Cero campos sensibles expuestos y evento de auditoría generado. |

### EC-05: Alteración de bitácora

| Elemento | Escenario |
|---|---|
| Fuente | Usuario privilegiado o proceso comprometido |
| Estímulo | Intenta modificar o eliminar una entrada histórica. |
| Entorno | Operación normal. |
| Artefacto | Bitácora append-only y archivo WORM. |
| Respuesta | La operación se rechaza y se genera una alerta de integridad. |
| Medida | Cero entradas alteradas; cadena de verificación válida. |

### EC-06: Operación offline

| Elemento | Escenario |
|---|---|
| Fuente | Unidad de campo |
| Estímulo | Pierde conectividad y registra operaciones. |
| Entorno | Zona rural, fronteriza o afectada por un desastre. |
| Artefacto | App Móvil y SQLite. |
| Respuesta | Las operaciones se almacenan localmente y permanecen disponibles tras reiniciar la aplicación. |
| Medida | Cero datos locales perdidos; retención local de hasta 30 días. |

### EC-07: Reconexión y sincronización

| Elemento | Escenario |
|---|---|
| Fuente | Red |
| Estímulo | Se restablece una conexión VPN estable. |
| Entorno | Existen operaciones locales y cambios concurrentes. |
| Artefacto | Servicio de Sincronización Offline. |
| Respuesta | Deduplica, valida versiones, aplica reglas y remite conflictos no resolubles. |
| Medida | Cero efectos duplicados y cero transiciones inválidas aceptadas. |

### EC-08: Redelivery de un evento

| Elemento | Escenario |
|---|---|
| Fuente | Kafka |
| Estímulo | Entrega nuevamente un evento ya procesado. |
| Entorno | Recuperación de consumidor. |
| Artefacto | Worker o microservicio consumidor. |
| Respuesta | Detecta el identificador y evita repetir el efecto. |
| Medida | Un único efecto de negocio por evento. |

### EC-09: Sistema institucional no disponible

| Elemento | Escenario |
|---|---|
| Fuente | Sistema externo |
| Estímulo | No responde a la consulta o reserva de recursos. |
| Entorno | Despacho crítico. |
| Artefacto | Resource Availability Fetcher y Saga. |
| Respuesta | Aplica timeout, usa información permitida de caché y solicita decisión manual; compensa reservas si corresponde. |
| Medida | La operación no queda bloqueada indefinidamente y respeta el límite de 90 segundos. |

### EC-10: Activación de protocolo nacional

| Elemento | Escenario |
|---|---|
| Fuente | Coordinador CNE |
| Estímulo | Activa un protocolo nacional. |
| Entorno | Varias instituciones operando. |
| Artefacto | Servicio de Protocolos CNE y Kafka. |
| Respuesta | Versiona, publica y aplica prioridades sin confirmación manual por institución. |
| Medida | Todas las instituciones consumidoras reciben la actualización; umbral temporal exacto pendiente de validación con el cliente. |

### EC-11: Falla del plano analítico

| Elemento | Escenario |
|---|---|
| Fuente | ClickHouse o worker analítico |
| Estímulo | El componente deja de responder. |
| Entorno | Incidentes activos. |
| Artefacto | Planos operacional y analítico. |
| Respuesta | Registro y despacho continúan; eventos quedan disponibles para reproceso y las vistas indican retraso. |
| Medida | Cero interrupciones del flujo operacional y recuperación completa de proyecciones. |

### EC-12: Evolución de contrato

| Elemento | Escenario |
|---|---|
| Fuente | Equipo de desarrollo |
| Estímulo | Se agrega un campo opcional a un evento. |
| Entorno | Conviven productores y consumidores de distintas versiones. |
| Artefacto | Schema Registry y consumidores. |
| Respuesta | Consumidores antiguos ignoran el campo y nuevos lo utilizan cuando existe. |
| Medida | Cero eventos rechazados por incompatibilidad hacia atrás. |

### EC-13: Consulta histórica de auditoría

| Elemento | Escenario |
|---|---|
| Fuente | Auditor autorizado |
| Estímulo | Solicita registros dentro de los últimos cinco años. |
| Entorno | Operación normal. |
| Artefacto | Proyección append-only y MinIO WORM. |
| Respuesta | Genera una exportación íntegra, trazable y autorizada. |
| Medida | 100 % de los registros aplicables recuperables y verificables. |

# Riesgos y deuda técnica

| ID | Riesgo o deuda | Impacto | Mitigación / acción requerida |
|---|---|---|---|
| RT-01 | ADR-0002 contradice el alcance operacional del RFP y los C4. | Ambigüedad de alcance y decisiones incompatibles. | Actualizarlo o sustituirlo, limitando ETL/ELT al plano analítico. |
| RT-02 | Etiqueta incorrecta del Coordinador CNE en C4 Nivel 1. | Confusión de stakeholders y responsabilidades. | Corregir el archivo `.drawio` y regenerar el PNG. |
| RT-03 | TTL de caché inconsistente: 30 s en C4 Nivel 3 y 5 s en topología. | Riesgo de despachar con información obsoleta. | Adoptar TTL ≤ 5 s para recursos y actualizar el C4 Nivel 3. |
| RT-04 | RPO y RTO por almacén no definidos. | Recuperación no verificable frente a fallos. | Crear matriz RPO/RTO y pruebas de recuperación por servicio. |
| RT-05 | Complejidad de múltiples tecnologías de persistencia. | Mayor carga operativa y curva de aprendizaje. | Estandarizar operación, observabilidad, backups y runbooks; reducir motores si una prueba demuestra redundancia innecesaria. |
| RT-06 | Capacidad on-premise y falta de elasticidad inmediata. | Saturación durante emergencias nacionales. | Pruebas de carga, reserva de capacidad, escalado planificado y adquisición anticipada. |
| RT-07 | VPN como cuello de botella o punto único de fallo. | Pérdida de acceso institucional. | Redundancia, balanceo, pruebas de failover y monitoreo de túneles. |
| RT-08 | Retención de Kafka durante cinco años puede ser costosa. | Consumo excesivo de almacenamiento y recuperación lenta. | Definir retención por tópico y usar MinIO WORM como archivo legal de largo plazo. |
| RT-09 | “Kafka como source of truth” no está delimitado por dominio. | Confusión entre transporte, event store y sistema de registro. | Definir eventos autoritativos, read models y políticas de reconstrucción por bounded context. |
| RT-10 | No existe aún una vista de despliegue C4 formal. | Dificultad para validar alta disponibilidad y red. | Crear diagrama de despliegue con nodos, zonas, VPN, almacenamiento y rutas. |
| RT-11 | Falta modelo completo de clasificación de datos. | Riesgo de exposición o retención excesiva. | Crear catálogo de datos, niveles de sensibilidad y reglas de minimización. |
| RT-12 | Conflictos offline complejos. | Estados contradictorios de incidentes o recursos. | Definir reglas por agregado, pruebas de convergencia y bandeja de resolución manual. |
| RT-13 | Dependencia de sistemas institucionales heterogéneos. | Timeouts, formatos incompatibles y datos incompletos. | Adaptadores, contratos, pruebas de contrato, fallback y monitoreo por institución. |
| RT-14 | Versiones y licencias de tecnologías deben revisarse antes de producción. | Riesgo de soporte, seguridad o incompatibilidad legal. | Inventario SBOM, revisión de licencias, parches y política de actualización. |

# Glosario

| Término | Definición |
|---|---|
| ABAC | Control de acceso basado en atributos como institución, jurisdicción, sensibilidad y finalidad. |
| ADR | Registro de una decisión arquitectónica, su contexto, alternativas y consecuencias. |
| Bitácora operativa | Registro cronológico e inmutable de acciones realizadas sobre incidentes. |
| Bounded Context | Límite de dominio dentro del cual un modelo y sus reglas tienen significado consistente. |
| CDC | Captura de cambios de datos para propagar modificaciones hacia eventos o proyecciones. |
| CQRS | Separación de modelos y rutas para comandos de escritura y consultas de lectura. |
| Data warehouse | Almacén optimizado para consultas analíticas y agregaciones históricas. |
| Database-per-service | Principio según el cual cada servicio posee y controla su propio almacén. |
| ETL/ELT | Procesos de extracción, transformación y carga de datos destinados principalmente a analítica. |
| Event Sourcing | Persistencia del historial de cambios como una secuencia de eventos inmutables. |
| Idempotencia | Propiedad que permite repetir una operación sin producir efectos adicionales. |
| Incidente institucional | Evento que requiere intervención formal de al menos una institución participante. |
| KEDA | Componente de Kubernetes que escala cargas según eventos o colas. |
| Mapa de calor | Visualización territorial de concentración, tipo e intensidad de incidentes. |
| Outbox | Patrón que almacena el cambio de dominio y el mensaje a publicar en una misma transacción local. |
| RBAC | Control de acceso basado en roles. |
| RLS | Seguridad a nivel de fila dentro de una base de datos. |
| Saga | Secuencia de transacciones locales coordinadas con acciones compensatorias. |
| SLA institucional | Tiempo máximo tolerable para atención o despacho según evento e institución. |
| Sistema de registro | Sistema que conserva la versión autoritativa de un dato. |
| Datos derivados | Datos reconstruibles a partir de un sistema de registro, como cachés y proyecciones. |
| WORM | Almacenamiento que permite escribir una vez y leer muchas, impidiendo modificaciones durante la retención. |