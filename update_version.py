# update_version.py
import pathlib
import tomli
import tomli_w
import sys

if len(sys.argv) < 2:
    print("Por favor pasa la nueva versión como argumento")
    sys.exit(1)

new_version = sys.argv[1]

pyproject_path = pathlib.Path("pyproject.toml")
init_path = pathlib.Path("src/leak_inspector/__init__.py")

# Actualizar pyproject.toml
with pyproject_path.open("rb") as f:
    data = tomli.load(f)

data["project"]["version"] = new_version

with pyproject_path.open("wb") as f:
    tomli_w.dump(data, f)

# Actualizar __init__.py
lines = init_path.read_text().splitlines()
found = False
for i, line in enumerate(lines):
    if line.startswith("__version__"):
        lines[i] = f'__version__ = "{new_version}"'
        found = True
        break
if not found:
    lines.insert(0, f'__version__ = "{new_version}"')

init_path.write_text("\n".join(lines) + "\n")

print(f"Versión actualizada a {new_version}")