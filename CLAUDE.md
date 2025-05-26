# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Environment Setup (Story 0 - COMPLETED ✅)

### Prerequisites
- Python 3.11 (required for build compatibility)
- Xcode command line tools (macOS)
- CMake
- Git

### Initial Setup
1. **Create Virtual Environment:**
   ```bash
   python3.11 -m venv venv_dawdreamer
   source venv_dawdreamer/bin/activate
   pip install --upgrade pip build wheel setuptools pytest numpy
   ```

2. **Download Faust Libraries:**
   ```bash
   cd thirdparty/libfaust
   python download_libfaust.py
   cd ../..
   ```

3. **Build DawDreamer:**
   ```bash
   # Find correct Python path
   PYTHON_PATH=$(find /opt/homebrew/Cellar/python@3.11 -name "Frameworks" | head -1)
   
   # Build
   PYTHONMAJOR=3.11 pythonLocation=$PYTHON_PATH/Python.framework/Versions/3.11 ./build_macos.sh
   ```

4. **Create Wheel:**
   ```bash
   ARCHS=arm64 python -m build --wheel
   ```

### Build Commands
- macOS: `PYTHONMAJOR=3.11 pythonLocation=/opt/homebrew/Cellar/python@3.11/3.11.11/Frameworks/Python.framework/Versions/3.11 ./build_macos.sh`
- Linux: `./build_linux.sh`
- Create wheel: `ARCHS=arm64 python -m build --wheel` (macOS ARM64)

## Test Commands
- Run all tests: `python -m pytest -s .`
- Run verbose tests: `python -m pytest -v .`
- Run single test: `python -m pytest -v <test_file.py> -k "test_name"`
- Run GUI tests: `python -m pytest -v test_plugins.py -k "test_plugin_editor" -p no:faulthandler`
- Run baseline tests: `python -m pytest tests/test_baseline_functionality.py -v`
- Test plugin discovery: `python tests/test_plugin_discovery.py`

## VST Plugin Testing
- **Working Test Plugins:** RoughRider3.vst3 (13 params), TAL-NoiseMaker.vst3 (2174+ params), ValhallaFreqEcho.vst3 (9 params)
- **Plugin Directory:** `tests/plugins/`
- **Current Capabilities:** Plugin loading, parameter extraction, parameter range info, patch operations
- **Status:** All core functionality verified ✅

## Code Style
- Use snake_case for variables and functions
- Use PEP 8 spacing (4 spaces indentation)
- Import order: standard library, third-party, local imports
- Use NumPy arrays for audio data (shape: channels × samples)
- For processors in graphs, use descriptive names that match their function
- Add assertions to verify audio output is non-silent and doesn't contain NaN values

## Error Handling
- Use try/except blocks with specific exceptions
- Check file existence before operations
- Validate audio parameters before processing
- Use assertions for testing and validation

## Audio Processing Practices
- Use absolute file paths in all file operations
- Set sample rate (usually 44100Hz) and block size explicitly
- Build audio graphs with proper connections between processors
- Verify audio output quality with assertions on mean amplitude

## VST Parameter Feature Development

### Current Status
Story 0 (Build Environment & Plugin Testing) - **COMPLETED ✅**
- Build system working with Python 3.11 + macOS ARM64
- 3 test plugins verified working with full parameter extraction
- Baseline functionality test suite created

### Next Steps
See `VST_PARAMETER_FEATURES_BACKLOG.md` for detailed feature roadmap:
- **Phase 1:** Preset saving/export, parameter validation, preset browsing
- **Phase 2:** Parameter grouping, value mapping, automation curves  
- **Phase 3:** Advanced features like preset comparison and dependency detection

### Development Environment
- Always work in virtual environment: `source venv_dawdreamer/bin/activate`
- Test changes with: `python tests/test_plugin_discovery.py`
- Verify builds with: Test plugin loading before committing changes