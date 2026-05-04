.PHONY: release test-release check-clean

PACKAGE = leak_inspector

UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
    SED_CMD = sed -i ''
else
    SED_CMD = sed -i
endif

# -------------------------
# 🧪 TEST RELEASE (TestPyPI)
# -------------------------
test-release:
	@BASE=$$(python -c "import re; print(re.search(r'version = \"(.*)\"', open('pyproject.toml').read()).group(1))"); \
	COUNT=$$(git tag -l "$${BASE}.dev*" | wc -l | tr -d ' '); \
	DEV_VERSION="$${BASE}.dev$$(($$COUNT + 1))"; \
	echo "🧪 TestPyPI version: $$DEV_VERSION"; \
	$(SED_CMD) "s/version = .*/version = \"$$DEV_VERSION\"/" pyproject.toml; \
	python -m build; \
	twine upload --repository testpypi --skip-existing dist/*; \
	git checkout pyproject.toml

# -------------------------
# 🚀 RELEASE FINAL (PyPI)
# -------------------------
release: check-clean
	@if [ -z "$(VERSION)" ]; then \
		echo "❌ Debes especificar VERSION=x.y.z"; exit 1; \
	fi
	@echo "🚀 Creating release v$(VERSION)"
	@git tag v$(VERSION)
	@git push origin v$(VERSION)
	@echo "✅ PyPI publish triggered via GitHub Actions"

# -------------------------
check-clean:
	@if [ -n "$$(git status --porcelain)" ]; then \
		echo "❌ Tienes cambios sin commit"; \
		git status; \
		exit 1; \
	fi