# 1. Entorno Operativo

Date: 2026-07-05

## Status

2026-07-05 proposed

## Context

El proyecto requiere desplegar una solución tecnológica para el Departamento de Gobernación. Durante la fase de definición de la arquitectura tecnológica, se evaluaron diferentes opciones de despliegue, incluyendo proveedores de nube pública (como AWS, Azure o Google Cloud) y la infraestructura física local.
Debido a la naturaleza de los datos gestionados, el entorno regulatorio estricto y las políticas internas de seguridad de la información del departamento, se requiere un control absoluto sobre la soberanía de los datos y el perímetro de red.

## Decision

Se ha decidido utilizar exclusivamente la infraestructura On-Premise existente del Departamento de Gobernación para el alojamiento, procesamiento y almacenamiento de todos los componentes del proyecto.
Asimismo, se establece que el acceso a estos entornos quedará restringido única y exclusivamente a través de una conexión VPN directa (Virtual Private Network). Queda completamente descartado el uso de cualquier proveedor de nube pública o híbrida externa.

## Consequences

**Aspectos Positivos (Beneficios)**
- Cumplimiento Normativo Absoluto: Se garantiza la adherencia total a las leyes de protección de datos y gobernación de la información vigentes para el sector público.

- Soberanía y Control de Datos: Toda la información confidencial permanece dentro de los servidores físicos controlados por la institución, minimizando el riesgo de exposición en infraestructuras compartidas.

- Aislamiento del Perímetro: Al no exponer endpoints públicos a internet y canalizar todo el tráfico por VPN, se reduce drásticamente la superficie de ataque frente a amenazas externas.

**Aspectos Negativos (Riesgos o Limitaciones)**
- Escabilidad Limitada: La capacidad de cómputo y almacenamiento queda sujeta a la disponibilidad del hardware físico actual de la institución. No se cuenta con la elasticidad inmediata que ofrece la nube.

- Mantenimiento Operativo Técnico: El equipo técnico interno de Gobernación asume la responsabilidad total del aprovisionamiento, parches de seguridad de hardware, respaldos físicos y redundancia energética.

- Fricción en el Desarrollo y Pruebas: El acceso exclusivo por VPN puede ralentizar los procesos de integración continua y despliegue (CI/CD), además de requerir una gestión estricta de credenciales y accesos para el equipo de desarrollo.