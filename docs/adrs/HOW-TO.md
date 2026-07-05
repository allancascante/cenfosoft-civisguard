# ADRs del proyecto

Este directorio contiene los **Architecture Decision Records (ADR)** del proyecto.

## Propósito

Los ADR sirven para documentar decisiones de arquitectura y diseño relevantes, junto con su contexto, alternativas consideradas y la decisión final tomada.

## Herramienta utilizada

Para la creación y gestión de los registros ADR se utiliza la librería:

- https://github.com/phodal/adr

Esta dependencia está declarada en el archivo `package.json` del proyecto como `devDependency`.

## Instalación

No es necesario instalar nada manualmente adicional. Solo ejecuta:

```bash
npm install
```

Con eso se descargará e instalará [adr](https://github.com/phodal/adr) junto con las demás dependencias del proyecto.

## Uso

Una vez instaladas las dependencias, se pueden generar y administrar los ADR siguiendo el flujo de trabajo definido por la herramienta `adr`.

## Convención recomendada

Se sugiere mantener cada registro con un nombre descriptivo y numerado para conservar el orden cronológico de las decisiones.

Ejemplo:

- `0001-crear-autenticacion.md`
- `0002-definir-api-rest.md`
- `0003-elegir-base-de-datos.md`

## Alcance

Cada ADR debe ser breve, claro y enfocarse en una sola decisión importante.
