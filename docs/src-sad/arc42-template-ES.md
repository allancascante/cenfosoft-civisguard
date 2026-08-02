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

## Metas de Calidad

## Partes interesadas (Stakeholders)

| Rol/Nombre    | Contacto          | Expectativas          |
|---------------|-------------------|-----------------------|
| *\<Rol-1\>*   | *\<Contacto-1\>*  | *\<Expectativa-1\>*   |
| *\<Rol-2\>*   | *\<Contacto-2\>*  | *\<Expectativa-2\>*   |

# Restricciones de la Arquitectura

| Restricción | Descripción |
|---|---|
| Independencia de proveedor cloud | La Ley 9986 exige que la plataforma de infraestructura no genere dependencia de un proveedor comercial. La solución debe poder ejecutarse en cualquier nube pública o infraestructura on-premise. Esto determina el uso de Kubernetes como orquestador open source. |

# Alcance y Contexto del Sistema

## Contexto de Negocio

**\<Diagrama o Tabla\>**

**\<optionally: Explanation of external domain interfaces\>**

## Contexto Técnico

**\<Diagrama o Tabla\>**

**\<Opcional: Explicación de las interfases técnicas\>**

**\<Mapeo de Entrada/Salida a canales\>**

# Estrategia de solución

## Estilo Arquitectónico Macro: Event-Driven Híbrido sobre Kubernetes

El sistema combina dos patrones que responden a las dos naturalezas operativas del problema.

## Pipeline ETL orientado a eventos

La mayor parte del volumen del sistema — ingesta de incidentes, actualización del mapa de calor, analítica territorial y bitácora — sigue un flujo lineal: un evento entra al procesador de eventos, un worker lo consume, lo transforma y lo persiste. Estos workers son *stateless*, no exponen APIs ni toman decisiones de negocio. En el orquestador de contenedores escalan automáticamente proporcionalmente al tamaño de la cola, absorbiendo los picos de carga sin intervención manual.

## Microservicios para coordinación operativa

Los componentes con lógica de negocio real — despacho de recursos, protocolos de emergencia del CNE y sincronización offline de unidades de campo — se implementan como microservicios independientes. Cada uno tiene su propio ciclo de despliegue y base de datos, y se comunica con el resto del sistema a través del mismo bus de eventos. La capa de reportes y visualización institucional también son microservicios livianos que leen del datawarehouse.

## Gobierno y segregación de datos por `institucion_id`

`institucion_id` se establece como atributo canónico de dominio para garantizar aislamiento institucional, trazabilidad y cumplimiento normativo en toda la arquitectura de datos.

**Reglas obligatorias de datos:**

1. Todo registro de incidente, bitácora y proyección analítica debe persistir `institucion_id`.
2. Todo evento en Kafka debe incluir `institucion_id` en su payload y/o headers, además de `event_id`, `correlation_id` y `causation_id`.
3. Los almacenes multiinstitucionales deben aplicar **RLS (Row-Level Security)** o particionamiento equivalente por `institucion_id`.
4. Las consultas operativas y analíticas deben filtrar explícitamente por `institucion_id`, salvo vistas nacionales autorizadas para rol `coordinador_cne`.
5. `institucion_id` forma parte del contrato de datos entre microservicios; no es opcional ni derivable por conveniencia.

**Resultado esperado:**

- Separación efectiva de datos por institución (RNF-03).
- Coherencia entre identidad (JWT), autorización (RBAC) y persistencia (ADR-0003 y ADR-0004).
- Trazabilidad de extremo a extremo en flujos de coordinación interinstitucional (ADR-0005).

## Kubernetes como plataforma de orquestación

Ambos segmentos se despliegan sobre un clúster de **Kubernetes**, que provee:

- resiliencia automática ante fallos;
- *rolling updates* sin downtime;
- escalado independiente por servicio.

Al ser una plataforma open source que corre en cualquier nube o infraestructura on-premise, cumple además la restricción legal de independencia de proveedor establecida en la **Ley 9986**.

# Vista de Bloques

## Sistema General de Caja Blanca

***\<Diagrama general\>***

Motivación  
*\<Explicación en texto\>*

Bloques de construcción contenidos  
*\<Descripción de los bloques de construcción contenidos (Cajas negras)\>*

Interfases importantes  
*\<Descripción de las interfases importantes\>*

### \<Caja Negra 1\>

*\<Propósito/Responsabilidad\>*

*\<Interfase(s)\>*

*\<(Opcional) Características de Calidad/Performance\>*

*\<(Opcional) Ubicación Archivo/Directorio\>*

*\<(Opcional) Requerimientos Satisfechos\>*

*\<(Opcional) Riesgos/Problemas/Incidentes Abiertos\>*

### \<Caja Negra 2\>

*\<plantilla de caja negra\>*

### \<Caja Negra N\>

*\<Plantilla de caja negra\>*

### \<Interfase 1\>

...​

### \<Interfase m\>

## Nivel 2

### Caja Blanca *\<bloque de construcción 1\>*

*\<plantilla de caja blanca\>*

### Caja Blanca *\<bloque de construcción 2\>*

*\<plantilla de caja blanca\>*

...​

### Caja Blanca *\<bloque de construcción m\>*

*\<plantilla de caja blanca\>*

## Nivel 3

### Caja Blanca \<\_bloque de construcción x.1\_\>

*\<plantilla de caja blanca\>*

### Caja Blanca \<\_bloque de construcción x.2\_\>

*\<plantilla de caja blanca\>*

### Caja Blanca \<\_bloque de construcción y.1\_\>

*\<plantilla de caja blanca\>*

# Vista de Ejecución

## \<Escenario de ejecución 1\>

-   *\<Inserte un diagrama de ejecución o la descripción del
    escenario\>*

-   *\<Inserte la descripción de aspectos notables de las interacciones
    entre los bloques de construcción mostrados en este diagrama.\>*

## \<Escenario de ejecución 2\>

## ...​

## \<Escenario de ejecución n\>

# Vista de Despliegue

## Nivel de infraestructura 1

***\<Diagrama General\>***

Motivación  
*\<Explicación en forma textual\>*

Características de Calidad/Rendimiento  
*\<Explicación en forma textual\>*

Mapeo de los Bloques de Construcción a Infraestructura  
*\<Descripción del mapeo\>*

## Nivel de Infraestructura 2

### *\<Elemento de Infraestructura 1\>*

*\<diagrama + explicación\>*

### *\<Elemento de Infraestructura 2\>*

*\<diagrama + explicación\>*

...​

### *\<Elemento de Infraestructura n\>*

*\<diagrama + explicación\>*

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

# Requerimientos de Calidad

## Vista General de Requerimientos de Calidad

## Escenarios de Calidad

# Riesgos y deuda técnica

# Glosario

| Término          | Definición          |
|------------------|---------------------|
| *\<Término-1\>*  | *\<definición-1\>*  |
| *\<Término-2\>*  | *\<definición-2\>*  |
