# CivisGuard Analytics
### Sistema Nacional de Coordinación de Emergencias e Incidentes Institucionales

Curso: **PSWE-04 - Diseño de Sistemas de Software** Sección: **Maestría en Ingeniería de Software** — Periodo Q02 2026  
Docente Facilitador: **M.Sc. Kevin A. Hernández Rostrán**

## Equipo Consultor (Grupo: Cenfosoft)
* **Gustavo Castro**
* **David Cárdenas**
* **[Allan Cascante](https://github.com/allancascante)**
* **Randy Villareal**

---

## Descripción del Proyecto
**CivisGuard Analytics** es una plataforma nacional de misión crítica diseñada para la coordinación, monitoreo y análisis de incidentes interinstitucionales en Costa Rica ([fuente](RFP_CivisGuard_Gobernacion.docx)).

Su propósito principal es unificar los esfuerzos operativos de seis entidades clave del Estado ([fuente](RFP_CivisGuard_Gobernacion.docx)):
1. Sistema de Emergencias 9-1-1
2. Fuerza Pública
3. Caja Costarricense de Seguro Social (CCSS)
4. Cruz Roja Costarricense
5. Cuerpo de Bomberos de Costa Rica
6. Comisión Nacional de Prevención de Riesgos y Atención de Emergencias (CNE)

La plataforma transforma los datos operativos generados durante la atención de emergencias en inteligencia preventiva territorial, garantizando alta disponibilidad (24/7/365), resiliencia en zonas de conectividad degradada (*Offline-First*) y el estricto cumplimiento del marco legal costarricense (Leyes 8968, 7410, 8654, 8488, 8228) ([fuente](RFP_CivisGuard_Gobernacion.docx)).

---

## Enfoque Arquitectónico y Estándares
Este repositorio contiene el **Documento de Arquitectura de Software (SAD)** y los artefactos de diseño técnico elaborados de forma iterativa bajo estándares de la industria ([fuente principal](RFP_CivisGuard_Gobernacion.docx), [lineamientos académicos](Especificación%20Proyecto%2002.pdf)):

* **Estructura de Documentación:** Estándar **arc42** ([fuente](RFP_CivisGuard_Gobernacion.docx)).
* **Modelado Visual:** Modelo **C4** (Contexto N1, Contenedores N2, Componentes N3) ([fuente](RFP_CivisGuard_Gobernacion.docx)).
* **Registro de Decisiones:** **ADRs** (*Architecture Decision Records*) estructurados para justificar cada compensación (*trade-off*) técnica ([fuente](RFP_CivisGuard_Gobernacion.docx)).
* **Principios de Diseño:** Arquitectura orientada a eventos (EDA), persistencia políglota distribuida, y patrones tácticos de Domain-Driven Design (DDD) ([fuente](RFP_CivisGuard_Gobernacion.docx)).

---

## Cronograma de Entregables (Evolución del Repositorio)
El desarrollo arquitectónico se gestiona de manera incremental a través de las siguientes iteraciones semanales ([fuente](Especificación%20Proyecto%2002.pdf)):

* [ ] **Semana 08 (Iteración 1):** Kick-off, Estilo Arquitectónico Macro, C4 Nivel 1 (Contexto) y primeros 2 ADRs ([fuente](Especificación%20Proyecto%2002.pdf)).
* [ ] **Semana 09-10 (Iteración 2 & Review Board):** C4 Nivel 2 (Contenedores), Estrategia de Persistencia y sesión de retroalimentación con el cliente ([fuente](Especificación%20Proyecto%2002.pdf)).
* [ ] **Semana 11 (Iteración 3):** C4 Nivel 3 (Componente Crítico) y propuesta ilustrada de patrones arquitectónicos/diseño ([fuente](Especificación%20Proyecto%2002.pdf)).
* [ ] **Semana 12 (Inyección de Caos):** Mitigación del requerimiento sorpresa del negocio y ADR de impacto ([fuente](Especificación%20Proyecto%2002.pdf)).
* [ ] **Semana 13-14 (Refinamiento y Defensa):** Consolidación final del documento SAD arc42 y Pitch Final ([fuente](Especificación%20Proyecto%2002.pdf)).

---

## Estructura del Repositorio
```text
├── .github/
│   └── workflows/
│       └── docs-pdf.yml    # Workflow: genera PDF automáticamente en cada cambio de docs/
├── docs/
│   ├── adrs/               # Registros de Decisión Arquitectónica (ADRs)
│   ├── c4-models/          # Diagramas del Modelo C4 (Contexto, Contenedores, Componentes)
│   ├── src-sad/            # Archivos fuente del Documento de Arquitectura (SAD)
│   ├── consolidado.qmd     # Fuente consolidada generada automáticamente
│   └── consolidado-docs.pdf# PDF consolidado generado automáticamente
├── scripts/
│   └── build_docs_pdf.py   # Script para consolidar docs/ en un archivo Quarto
└── README.md               # Presentación del proyecto
```

## Generación del PDF consolidado

El repositorio genera automáticamente un PDF con toda la documentación de `docs/`
mediante **Quarto**. El proceso se ejecuta en GitHub Actions en cada cambio de `docs/`
y el PDF resultante se commitea automáticamente a `main`.

> ⚠️ **Quarto no se instala con npm.** Es un binario independiente.
> Instalación oficial: <https://quarto.org/docs/get-started/>

### Ejecución local

```bash
# 1. Generar el archivo fuente consolidado
python3 scripts/build_docs_pdf.py

# 2. Renderizar el PDF
cd docs && quarto render consolidado.qmd --to pdf
```

Resultado: `docs/consolidado.pdf`


## Disclaimer
El presente repositorio se creó exclusivamente con fines académicos en el marco de un curso de maestría universitaria. No tiene la intención de servir como referencia técnica oficial ni material para un proyecto en entorno de producción real. Toda la información, escenarios, datos transaccionales y simulaciones aquí presentadas son ficticias y de autoría exclusiva de los estudiantes que integran este equipo consultor.