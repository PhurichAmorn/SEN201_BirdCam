# Packaging Scripts

This folder contains scripts for building and packaging the BirdCam application for distribution.

## Files

### pyinstaller.py
PyInstaller build script that creates a standalone macOS application bundle (.app).

**Features:**
- Bundles Python interpreter and all dependencies
- Includes Cairo libraries for SVG rendering
- Includes Graphviz executables and plugins for flowchart generation
- Auto-detects conda environment path
- Creates a self-contained .app file

**Usage:**
```bash
pythonw packaging/pyinstaller.py
```

### pyi_rth_graphviz.py
Runtime hook for PyInstaller that configures Graphviz paths when the app starts.

**Purpose:**
- Adds the bundle directory to PATH
- Sets GRAPHVIZ_DOT environment variable
- Ensures the bundled `dot` executable is found at runtime

This file is automatically included by the build script and runs when the app launches.

## Output

After running the build script:
- `dist/BirdCam.app` - The standalone application
- `BirdCam.spec` - PyInstaller specification (auto-generated)
- `build/` - Temporary build files

## Documentation

See [BUILD.md](../BUILD.md) for complete build instructions and troubleshooting.
