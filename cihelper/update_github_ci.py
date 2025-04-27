from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from packaging.version import Version

app = typer.Typer(pretty_exceptions_short=True, pretty_exceptions_enable=False)


def find_package_by_name(name: str, cwd: Path) -> Path:
    """Find the Python package by name."""
    dirs = [file.parent for file in cwd.glob(f"**/{name}/pyproject.toml")]
    if len(dirs) == 0:
        raise ValueError(f"Package {name} not found")
    if len(dirs) > 1:
        raise ValueError(
            f"Multiple packages found with name {name}: {', '.join(str(match) for match in dirs)}"
        )
    return dirs[0]


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
    if template == "python":
        content = (template_dir / "python.yml").read_text()
        if max_python is None:
            content = content.replace("__PYTHON_VERSION__", f'"{min_python}"')
        else:
            # get list of python versions from min_python to max_python (e.g., 3.8 to 3.12 we will output "3.8 3.9 3.10 3.11 3.12")
            min_ver = Version(min_python)
            max_ver = Version(max_python)
            versions = []
            current_ver = min_ver

            while current_ver <= max_ver:
                versions.append(f"{current_ver.major}.{current_ver.minor}")
                current_ver = Version(f"{current_ver.major}.{current_ver.minor + 1}")

            content = content.replace(
                "__PYTHON_VERSION__", '"' + " ".join(versions) + '"'
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
