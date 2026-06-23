.PHONY: run install build clean

VENV ?= $(HOME)/.hermes/hermes-agent/venv
PYTHON := $(VENV)/bin/python3

run:
	$(PYTHON) src/smartclipai.py

install:
	$(PYTHON) -m pip install -r requirements.txt

build: clean
	@echo "Creating SmartClipAI.app bundle..."
	@mkdir -p dist/SmartClipAI.app/Contents/MacOS dist/SmartClipAI.app/Contents/Resources
	@cp src/smartclipai.py dist/SmartClipAI.app/Contents/Resources/
	@cp assets/icon.icns dist/SmartClipAI.app/Contents/Resources/ 2>/dev/null || true
	@# Generate Info.plist
	@/bin/cat > dist/SmartClipAI.app/Contents/Info.plist << 'PLIST'
	@echo "Building app bundle..."
	@# Create executable (shell wrapper)
	@/bin/cat > dist/SmartClipAI.app/Contents/MacOS/SmartClipAI << 'SHELL'
	@# Register the app
	@/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -f dist/SmartClipAI.app 2>/dev/null || true
	@echo "Done! Run: open dist/SmartClipAI.app"

clean:
	rm -rf dist/ build/
