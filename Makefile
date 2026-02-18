# Makefile for Garmin Connect IQ App - SunPredict

# SDK Path - update this or set GARMIN_SDK_HOME environment variable
GARMIN_SDK_HOME ?= C:\Users\mail\AppData\Roaming\Garmin\ConnectIQ\Sdks\connectiq-sdk-win-8.4.1-2026-02-03-e9f77eeaa

# Variables
MONKEYC = "$(GARMIN_SDK_HOME)/bin/monkeyc"
MONKEYDO = "$(GARMIN_SDK_HOME)/bin/monkeydo"
SIMULATOR = "$(GARMIN_SDK_HOME)/bin/connectiq"
DEVICE = epix2pro47mm
OUTPUT = sunpredict.prg
# Developer key path - set this in your environment or pass as argument
# Example: make build DEVELOPER_KEY=/path/to/your/developer_key
DEVELOPER_KEY ?= developer_key
JUNGLE_FILE = monkey.jungle

# Default target
.PHONY: all
all: build

# Build the application (debug version)
.PHONY: build
build:
	@echo "Building app for $(DEVICE)..."
	$(MONKEYC) -d $(DEVICE) -f $(JUNGLE_FILE) -o $(OUTPUT) -y $(DEVELOPER_KEY)
	@echo "Build complete: $(OUTPUT)"

# Build release version (no debug info, smaller file)
.PHONY: release
release:
	@echo "Building app RELEASE for $(DEVICE)..."
	$(MONKEYC) -d $(DEVICE) -f $(JUNGLE_FILE) -o $(OUTPUT) -y $(DEVELOPER_KEY) -r
	@echo "Release build complete: $(OUTPUT)"

# Start the simulator standalone
.PHONY: simulator
simulator:
	@echo "Starting Connect IQ simulator..."
	$(SIMULATOR) &
	@echo "Simulator started. Use 'make run' to load your app."

# Run the application in simulator (always builds first)
.PHONY: run
run: build
	@echo "Loading app in simulator for $(DEVICE)..."
	@echo "Note: If this fails, first run 'make simulator' to start the simulator."
	$(MONKEYDO) $(OUTPUT) $(DEVICE)

# Clean build artifacts
.PHONY: clean
clean:
	@echo "Cleaning build artifacts..."
	rm -f $(OUTPUT)
	rm -f *.prg.debug.xml
	@echo "Clean complete"

# Help target
.PHONY: help
help:
	@echo "Garmin Connect IQ App - Makefile targets:"
	@echo "  make build     - Compile the application"
	@echo "  make simulator - Start the Connect IQ simulator"
	@echo "  make run       - Build and load in simulator"
	@echo "  make release   - Build release version"
	@echo "  make clean     - Remove build artifacts"
	@echo "  make help      - Show this help message"
	@echo ""
	@echo "Required environment variable:"
	@echo "  GARMIN_SDK_HOME - Path to Connect IQ SDK"
	@echo ""
	@echo "Current settings:"
	@echo "  GARMIN_SDK_HOME = $(GARMIN_SDK_HOME)"
	@echo "  Device = $(DEVICE)"
	@echo "  Output = $(OUTPUT)"