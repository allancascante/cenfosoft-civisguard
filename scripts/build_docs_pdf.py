from __future__ import annotations

import re
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
OUT_QMD = DOCS / "consolidado.qmd"

SKIP_FILES = {OUT_QMD.name, "HOW-TO.md", "how-to.md"}
SKIP_PATHS = {
    "adrs/README.md",
    "c4-models/README.md",
    "src-sad/README.md",
}
DIAGRAM_EXTENSIONS = {".drawio", ".png", ".svg", ".jpg", ".jpeg", ".puml", ".mmd"}


def strip_front_matter(text: str) -> str:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[end + 5 :]
    return text


def is_external_target(target: str) -> bool:
    t = target.strip().lower()
    return (
        t.startswith("http://")
        or t.startswith("https://")
        or t.startswith("mailto:")
        or t.startswith("#")
        or t.startswith("data:")
    )


def normalize_link(target: str, source_file: Path) -> str:
    target = target.strip()
    if is_external_target(target):
        return target

    if " " in target and not target.startswith("<"):
        first, rest = target.split(" ", 1)
        path_part, suffix = first, " " + rest
    else:
        path_part, suffix = target, ""

    if "#" in path_part:
        base, anchor = path_part.split("#", 1)
        anchor = "#" + anchor
    else:
        base, anchor = path_part, ""

    if base.startswith("/"):
        return target

    resolved = (source_file.parent / base).resolve()
    try:
        rel = resolved.relative_to(DOCS).as_posix()
    except ValueError:
        rel = base

    return f"{rel}{anchor}{suffix}"


def rewrite_relative_links(text: str, source_file: Path) -> str:
    pattern = re.compile(r"(!?\[[^\]]*\])\(([^)]+)\)")

    def _repl(match: re.Match[str]) -> str:
        label = match.group(1)
        target = match.group(2)
        new_target = normalize_link(target, source_file)
        return f"{label}({new_target})"

    return pattern.sub(_repl, text)


def list_markdown_files() -> List[Path]:
    files = [
        p
        for p in DOCS.rglob("*.md")
        if p.is_file()
        and p.name not in SKIP_FILES
        and p.relative_to(DOCS).as_posix() not in SKIP_PATHS
    ]

    base = DOCS / "src-sad" / "arc42-template-ES.md"
    ordered: List[Path] = []
    if base in files:
        ordered.append(base)
        files.remove(base)

    ordered.extend(sorted(files, key=lambda p: p.as_posix()))
    return ordered


def list_diagram_assets() -> List[Path]:
    assets = [
        p
        for p in DOCS.rglob("*")
        if p.is_file() and p.suffix.lower() in DIAGRAM_EXTENSIONS
    ]
    return sorted(assets, key=lambda p: p.as_posix())


def build_qmd(markdown_files: List[Path], assets: List[Path]) -> str:
    lines = [
        "---",
        'title: "Consolidado de Arquitectura (arc42 + docs)"',
        "lang: es",
        "format:",
        "  pdf:",
        "    toc: true",
        "    number-sections: true",
        "    colorlinks: true",
        "    geometry:",
        "      - margin=1in",
        "---",
        "",
        "# Documento consolidado",
        "",
        "Este PDF se genera automáticamente desde el contenido de la carpeta `docs`.",
        "La referencia base es el archivo arc42 en español.",
        "",
    ]

    for md in markdown_files:
        rel = md.relative_to(DOCS).as_posix()
        raw = md.read_text(encoding="utf-8")
        raw = strip_front_matter(raw)
        raw = rewrite_relative_links(raw, md).strip()

        lines.extend(
            [
                r"\newpage",
                "",
                f"## Fuente: {rel}",
                "",
                raw,
                "",
            ]
        )

    lines.extend([r"\newpage", "", "# Inventario de diagramas y artefactos visuales", ""])

    if assets:
        for a in assets:
            lines.append(f"- {a.relative_to(DOCS).as_posix()}")
    else:
        lines.append("- No se detectaron archivos de diagramas en `docs`.")

    lines.append("")
    return "\n".join(lines)


def main() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    markdown_files = list_markdown_files()
    assets = list_diagram_assets()
    OUT_QMD.write_text(build_qmd(markdown_files, assets), encoding="utf-8")
    print(f"Generado: {OUT_QMD.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
