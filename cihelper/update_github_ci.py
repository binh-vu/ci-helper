from __future__ import annotations

from pathlib import Path
from typing import Annotated, Optional

import typer
from packaging.version import Version
from sbt.package.discovery import get_candidate_pyprojects

app = typer.Typer(pretty_exceptions_short=True, pretty_exceptions_enable=False)


def find_package_by_name(name: str, cwd: Path) -> Path:
    """Find the Python package by name."""
    dirs = [
        dir
        for dir in get_candidate_pyprojects(
            cwd,
            ignore_dirs={},
            ignore_dirnames={"__pycache__", "data", "node_modules", ".venv"},
        )
        if dir.name == name
    ]

    if len(dirs) == 0:
        raise ValueError(f"Package {name} not found")
    if len(dirs) > 1:
        raise ValueError(
            f"Multiple packages found with name {name}: {', '.join(str(match) for match in dirs)}"
        )
    return dirs[0]


def get_python_versions(min_python: str, max_python: Optional[str]) -> str:
    """Get a list of Python versions from min_ver to max_ver."""
    if max_python is None:
        return min_python
    else:
        # get list of python versions from min_python to max_python (e.g., 3.8 to 3.12 we will output "3.8 3.9 3.10 3.11 3.12")
        min_ver = Version(min_python)
        max_ver = Version(max_python)
        versions = []
        current_ver = min_ver

        while current_ver <= max_ver:
            versions.append(f"{current_ver.major}.{current_ver.minor}")
            current_ver = Version(f"{current_ver.major}.{current_ver.minor + 1}")

        return " ".join(versions)


@app.command(help="Update Github CI for a Python (+Rust) package")
def main(
    template: Annotated[
        str,
        typer.Option("--template", help="Name of the template to use"),
    ],
    target: Annotated[
        str,
        typer.Option("--target", help="Target package to update"),
    ],
    min_python: Annotated[
        str,
        typer.Option(
            "--min-python",
            help="Minimum Python version to support (e.g. 3.8)",
        ),
    ],
    max_python: Annotated[
        str | None,
        typer.Option(
            "--max-python",
            help="Maximum Python version to support (e.g. 3.12)",
        ),
    ] = None,
    cwd: Annotated[
        Path,
        typer.Option(
            "--cwd",
            help="Current working directory to find the package",
        ),
    ] = Path.cwd(),
):
    typer.echo(f"Updating CI for template: {template} and target: {target}")

    template_dir = Path(__file__).parent / "github_actions"

    PYTHON_VERSION = get_python_versions(min_python, max_python)
    PYTHON_MULTILINE_VERSION = PYTHON_VERSION.replace(" ", "\\n")
    PYTHON_MIN_VERSION = min_python

    content = (template_dir / f"{template}.yml").read_text()
    if template == "poetry":
        content = content.replace("__PYTHON_VERSION__", PYTHON_VERSION).replace(
            "__PYTHON_MULTILINE_VERSION__", PYTHON_MULTILINE_VERSION
        )
    elif template == "maturin":
        PKG_DIR = "rust"

        content = (
            content.replace("__PYTHON_VERSION__", PYTHON_VERSION)
            .replace("__PYTHON_MIN_VERSION__", PYTHON_MIN_VERSION)
            .replace("__PKG_DIR__", PKG_DIR)
            .replace("__PYTHON_MULTILINE_VERSION__", PYTHON_MULTILINE_VERSION)
        )
    else:
        raise ValueError(f"Unknown template: {template}")

    pkgdir = find_package_by_name(target, cwd)
    cifile = pkgdir / ".github" / "workflows" / f"{template}.yml"
    typer.echo(f"Writing CI file to {cifile}")
    cifile.parent.mkdir(parents=True, exist_ok=True)
    cifile.write_text(content)


if __name__ == "__main__":
    app()
