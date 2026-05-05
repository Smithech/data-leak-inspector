# Makefile para preparar releases localmente
PYPROJECT_FILE := pyproject.toml
INIT_FILE := src/leak_inspector/__init__.py

# Leer versión base del pyproject.toml
PYPROJECT_VERSION := $(shell python -c "import tomli; print(tomli.load(open('$(PYPROJECT_FILE)','rb'))['project']['version'])")

.PHONY: testpypi pypi

# Preparar release de Test PyPI (.devX)
# Solo actualiza versión .devX y hace push a main
testpypi:
	@echo "Preparando Test PyPI..."
	@if [ -z "$(DEV)" ]; then \
		echo "Por favor define DEV, ej: make testpypi DEV=1"; exit 1; \
	fi
	python update_version.py $(PYPROJECT_VERSION).dev$(DEV)
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
	python update_version.py $(VERSION)
	git add $(PYPROJECT_FILE) $(INIT_FILE)
	git commit -m "Release version $(VERSION)"
	git tag -a "v$(VERSION)" -m "Version $(VERSION)"
	git push origin main --follow-tags
	@echo "Release PyPI listo"