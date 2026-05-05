# Makefile para preparar releases localmente
PYPROJECT_FILE := pyproject.toml
INIT_FILE := src/leak_inspector/__init__.py

# Leer versión base del pyproject.toml
PYPROJECT_VERSION := $(shell python3 get_version.py)

.PHONY: testpypi pypi

# Función para actualizar versión en pyproject.toml y __init__.py
define update_version
python - <<PYTHON_EOF
import pathlib, tomli, tomli_w

pyproject_path = pathlib.Path("$(PYPROJECT_FILE)")
init_path = pathlib.Path("$(INIT_FILE)")
new_version = "$(1)"

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
init_path.write_text("\\n".join(lines) + "\\n")

print(f"Versión actualizada a {new_version}")
PYTHON_EOF
endef

# Preparar release de Test PyPI
# Solo actualiza versión a .devX y hace push a main
testpypi:
	@echo "Preparando Test PyPI..."
	@if [ -z "$(DEV)" ]; then \
		echo "Por favor define DEV, ej: make testpypi DEV=1"; exit 1; \
	fi
	$(call update_version,$(PYPROJECT_VERSION).dev$(DEV))
	git add $(PYPROJECT_FILE) $(INIT_FILE)
	git commit -m "Preparando Test PyPI $(PYPROJECT_VERSION).dev$(DEV)" || echo "No hay cambios para commitear"
	git push origin main
	@echo "Test PyPI listo"

# Preparar release estable para PyPI
# Actualiza versión, hace commit, tag y push
pypi:
	@echo "Preparando release PyPI..."
	@if [ -z "$(VERSION)" ]; then \
		echo "Por favor define VERSION, ej: make pypi VERSION=1.2.0"; exit 1; \
	fi
	$(call update_version,$(VERSION))
	git add $(PYPROJECT_FILE) $(INIT_FILE)
	git commit -m "Release version $(VERSION)"
	git tag -a "v$(VERSION)" -m "Version $(VERSION)"
	git push origin main --follow-tags
	@echo "Release PyPI listo"