# Makefile para versionado, build y publicación

PYTHON := python3
PIP := $(PYTHON) -m pip
BUILD_DIR := dist
PACKAGE := data-leak-inspector
PYPROJECT := pyproject.toml

# Target para crear un nuevo release
# Uso: make release VERSION=0.2.0
.PHONY: release
release:
ifndef VERSION
	$(error Debes proporcionar la nueva versión: make release VERSION=x.y.z)
endif
	@echo "Actualizando versión a $(VERSION) en $(PYPROJECT)..."
	# Actualiza la versión en pyproject.toml
	sed -i '' -e 's/^version = .*/version = "$(VERSION)"/' $(PYPROJECT)
	# Git commit
	git add $(PYPROJECT)
	git commit -m "Bump version to $(VERSION)"
	# Crear tag
	git tag v$(VERSION)
	# Push commit y tag
	git push origin HEAD
	git push origin v$(VERSION)
	@echo "Release v$(VERSION) creado y subido al repositorio remoto."