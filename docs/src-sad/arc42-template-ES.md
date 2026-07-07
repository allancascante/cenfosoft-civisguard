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

# Requerimientos de Calidad

## Vista General de Requerimientos de Calidad

## Escenarios de Calidad

# Riesgos y deuda técnica

# Glosario

| Término          | Definición          |
|------------------|---------------------|
| *\<Término-1\>*  | *\<definición-1\>*  |
| *\<Término-2\>*  | *\<definición-2\>*  |
