# Modelos C4 del proyecto

Este directorio contiene los diagramas de arquitectura del proyecto usando el **modelo C4**.

## Propósito

Describir la arquitectura del sistema en diferentes niveles de detalle para facilitar:

- comprensión del sistema por parte del equipo;
- comunicación técnica con stakeholders;
- mantenimiento y evolución de la solución.

## Contenido de este folder

Aquí se deben almacenar los diagramas C4 del proyecto:

- **Nivel 1 – Contexto del Sistema (System Context)**
- **Nivel 2 – Contenedores (Container Diagram)**
- **Nivel 3 – Componentes (Component Diagram)**
- **Nivel 4 – Código (Code Diagram, opcional según necesidad)**

> Nota: el nivel 4 se recomienda solo cuando aporte valor para explicar componentes complejos.

## Herramienta de edición

Los diagramas se crean y editan con **draw.io (diagrams.net)**. draw.io

Se recomienda guardar:

- el archivo fuente editable (`.drawio`), y
- una versión exportada para visualización (`.png` o `.svg`).

## Convención sugerida de nombres

Para mantener consistencia, usar nombres como:

- `c4-l1-contexto.drawio`
- `c4-l2-contenedores.drawio`
- `c4-l3-componentes-<modulo>.drawio`
- `c4-l4-codigo-<modulo>.drawio` (si aplica)

## Buenas prácticas

- Mantener cada diagrama actualizado con los cambios de arquitectura.
- Incluir título, fecha de actualización y autor del cambio en el diagrama o metadatos.
- Evitar sobrecargar diagramas; dividir por módulos cuando sea necesario.
