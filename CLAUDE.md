# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands
- macOS: `PYTHONMAJOR=3.11 pythonLocation=/Library/Frameworks/Python.framework/Versions/3.11 ./build_macos.sh`
- Linux: `./build_linux.sh`
- Create wheel: `python -m build --wheel`

## Test Commands
- Run all tests: `python -m pytest -s .`
- Run verbose tests: `python -m pytest -v .`
- Run single test: `python -m pytest -v <test_file.py> -k "test_name"`
- Run GUI tests: `python -m pytest -v test_plugins.py -k "test_plugin_editor" -p no:faulthandler`

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