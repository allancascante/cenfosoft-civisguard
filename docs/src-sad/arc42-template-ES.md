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

## *\<Concepto 1\>*

*\<explicación\>*

## *\<Concepto 2\>*

*\<explicación\>*

...​

## *\<Concepto n\>*

*\<explicación\>*

# Decisiones de Diseño

Las decisiones descritas en esta sección resumen las principales elecciones arquitectónicas de **CivisGuard Analytics**. Cada decisión deberá formalizarse posteriormente mediante un **ADR** (*Architecture Decision Record*) que documente:

- El contexto.
- Las alternativas consideradas.
- La decisión tomada.
- Las consecuencias.
- Los riesgos aceptados.

El diseño parte de que ningún mecanismo resuelve simultáneamente la disponibilidad, consistencia, rendimiento, simplicidad y escalabilidad. Por ello, la arquitectura divide el sistema según la criticidad y naturaleza de cada carga, haciendo explícitos los *trade-offs*.

Esta separación sigue el principio de distinguir entre sistemas operacionales, sistemas analíticos, sistemas de registro y datos derivados.

---

## DD-01: Arquitectura híbrida orientada a eventos

CivisGuard utilizará una arquitectura orientada a eventos como mecanismo principal de integración entre sus componentes.

Las siguientes acciones producirán eventos de dominio persistentes:

- Registro de un incidente.
- Clasificación de un incidente.
- Despacho de recursos.
- Escalamiento.
- Cambio de estado.
- Cierre del incidente.
- Activación de protocolos nacionales.

Las operaciones que requieren una respuesta inmediata al usuario, como registrar, clasificar o confirmar un despacho, se ejecutarán mediante **APIs síncronas**.

Después de validar y persistir la operación, sus consecuencias se distribuirán de forma asíncrona mediante el bus de eventos.

Esta combinación evita depender de cadenas extensas de llamadas síncronas entre instituciones y permite que los consumidores procesen la información a su propio ritmo.

---

## DD-02: Separación entre el plano operacional y el plano analítico

La plataforma separará explícitamente dos tipos de procesamiento:

- **Plano operacional:** registro, clasificación, despacho, coordinación y actualización del estado de los incidentes.
- **Plano analítico:** mapas de calor, reportes, análisis histórico e inteligencia preventiva territorial.

El plano operacional contendrá los sistemas de registro autoritativos. El plano analítico se construirá mediante proyecciones y datos derivados generados a partir de los eventos operacionales.

Se aplicará una variante del patrón **CQRS** (*Command Query Responsibility Segregation*):

- El modelo de escritura aplicará las reglas de negocio y las restricciones de consistencia.
- Los modelos de lectura estarán optimizados para consultas geográficas, reportes y análisis histórico.
- Las consultas analíticas no se ejecutarán directamente sobre las bases de datos transaccionales.

Esta separación evita que una consulta histórica costosa afecte la capacidad de registrar o despachar incidentes.

Como consecuencia, se introduce duplicación controlada de información y consistencia eventual entre el estado operacional y las vistas analíticas.

El término **ETL** se reservará para la preparación y transformación de información analítica. La propagación operacional entre servicios se realizará mediante eventos de dominio y no mediante procesos ETL.

---

## DD-04: Bitácora inmutable con verificación criptográfica

La bitácora operativa será un registro de solo anexado. Ningún usuario, administrador o servicio podrá modificar o eliminar eventos previamente confirmados.

Cada entrada incluirá como mínimo:

- Identificador del evento.
- Identificador del incidente.
- Identidad del funcionario o servicio.
- Institución.
- Acción realizada.
- Justificación.
- Fecha y hora en UTC.
- Identificador de correlación.
- Versión del agregado.
- Hash de integridad.

Para detectar alteraciones se utilizarán los siguientes mecanismos:

- Encadenamiento de hashes.
- Firma periódica de bloques.
- Almacenamiento con políticas de retención inmutable.

No se propone utilizar una cadena de bloques pública o distribuida, debido a su complejidad y al costo operacional innecesario para este contexto.

La bitácora almacenará metadatos de auditoría y referencias a información sensible. No se duplicarán indiscriminadamente expedientes clínicos ni información táctica dentro del registro inmutable.

---

## DD-05: Entrega al menos una vez e idempotencia

El bus de eventos utilizará una semántica de entrega **al menos una vez**.

Debido a reintentos, fallos de red o recuperación de consumidores, un mismo evento podría recibirse más de una vez.

Todos los consumidores deberán ser idempotentes mediante:

- Identificadores únicos de eventos.
- Control de eventos procesados.
- Restricciones de unicidad.
- Versiones de agregados.
- Claves de idempotencia para comandos.
- Operaciones transaccionales en cada servicio.

No se asumirá una garantía de procesamiento **exactamente una vez** de extremo a extremo entre sistemas distribuidos.

Para evitar escrituras duales inconsistentes entre una base de datos transaccional y el bus de eventos, se aplicará el patrón **Transactional Outbox**.

La modificación del dominio y la inserción del mensaje de salida se realizarán dentro de la misma transacción local.

Este patrón permite desacoplar el modelo interno de los contratos públicos de eventos y reducir las inconsistencias entre las bases de datos y los flujos de eventos.

# Requerimientos de Calidad

Los requerimientos de calidad determinan cómo debe comportarse CivisGuard bajo condiciones normales, picos de demanda, fallos parciales, conectividad degradada y cambios futuros.

La confiabilidad no significa que ningún componente falle, sino que el sistema continúe prestando su servicio cuando ocurran fallos previsibles. Además de la confiabilidad, los atributos prioritarios para CivisGuard son rendimiento, seguridad, integridad, escalabilidad, operabilidad, portabilidad y capacidad de evolución.

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

## Vista General de Requerimientos de Calidad

## Escenarios de Calidad

# Riesgos y deuda técnica

# Glosario

| Término          | Definición          |
|------------------|---------------------|
| *\<Término-1\>*  | *\<definición-1\>*  |
| *\<Término-2\>*  | *\<definición-2\>*  |
