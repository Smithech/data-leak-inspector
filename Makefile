.PHONY: release bump-version check-clean

PACKAGE = data_leak_inspector

release: check-clean bump-version
	git add .
	git commit -m "release: v$(VERSION)"
	git tag v$(VERSION)
	git push origin main
	git push origin v$(VERSION)

bump-version:
	@if [ -z "$(VERSION)" ]; then \
		echo "❌ Debes especificar VERSION=x.y.z"; \
		exit 1; \
	fi
	@echo "🔖 Bumping version to $(VERSION)"
	sed -i 's/__version__ = .*/__version__ = "$(VERSION)"/' src/$(PACKAGE)/__init__.py

check-clean:
	@if [ -n "$$(git status --porcelain)" ]; then \
		echo "❌ Tienes cambios sin commit"; \
		exit 1; \
	fi