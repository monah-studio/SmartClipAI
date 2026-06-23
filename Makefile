.PHONY: run install build clean

VENV ?= $(HOME)/.hermes/hermes-agent/venv
PYTHON := $(VENV)/bin/python3

run:
	$(PYTHON) src/clipai.py

install:
	$(PYTHON) -m pip install -r requirements.txt

build: clean
	@echo "Creating ClipAI.app bundle..."
	@mkdir -p dist/ClipAI.app/Contents/MacOS dist/ClipAI.app/Contents/Resources
	@cp src/clipai.py dist/ClipAI.app/Contents/Resources/
	@cp assets/icon.icns dist/ClipAI.app/Contents/Resources/ 2>/dev/null || true
	@# Generate Info.plist
	@/bin/cat > dist/ClipAI.app/Contents/Info.plist << 'PLIST'
	@echo "Building app bundle..."
	@# Create executable (shell wrapper)
	@/bin/cat > dist/ClipAI.app/Contents/MacOS/ClipAI << 'SHELL'
	@# Register the app
	@/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -f dist/ClipAI.app 2>/dev/null || true
	@echo "Done! Run: open dist/ClipAI.app"

clean:
	rm -rf dist/ build/
