# SEN201_BirdCam

Software Engineering Process Project (Pseudocode to Flowchart)

## Team Members

- Phurich Amornnara
- Thanakit Thanasuwanditee
- Phasin Noomkan
- Puttipong Srisuwantat

## Project Overview

This project focuses on converting pseudocode to flowcharts as part of the Software Engineering Process course (SEN201).

## Documentation

- **[BIRDCAM_pseudocode_standard](birdcam_pseudocode_standard.txt)** - Complete reference guide for pseudocode conventions used in this course, including syntax rules, formatting guidelines, and examples.

## Files

- `BIRDCAM_pseudocode_standard.txt` - Comprehensive pseudocode standard documentation

## Requirements

### Using Conda Environment (Recommended for macOS)

This project includes an `environment.yml` file that sets up all required dependencies including proper GUI support for macOS.

To create and use the conda environment:

```bash
# Create the environment (first time only)
conda env create -f environment.yml

# Activate the environment
conda activate birdcam
```

### Using pip

Alternatively, this project includes a **[BIRDCAM_REQUIREMENT](requirements.txt)** file at the repository root which lists the Python packages needed to run and test the project.

To install the required packages into your active Python environment, run:

```bash
python -m pip install -r requirements.txt
```

### Development dependencies

Development and test tools should be kept separate from runtime dependencies. Install requirements from `dev-requirements.txt` to get packages used only during development.

Install development dependencies with:

```bash
python -m pip install -r dev-requirements.txt
```

Common dev commands:

```bash
# Run tests
pytest -q
```

Keep `requirements.txt` for packages required by the application at runtime and `dev-requirements.txt` for tools used during development.

## Running the Application

After setting up the environment, run the GUI application:

```bash
# Activate conda environment first
conda activate birdcam

# Run the GUI (macOS)
pythonw src/gui.py
```

**Note for macOS users:** Use `pythonw` instead of `python` to ensure the GUI windows appear properly in the foreground with full macOS integration.


## Running tests

Unit tests are in the `tests/` folder. To run them, execute:

```bash
pytest -q
```

---

## Building & Distribution

BirdCam can be packaged as a standalone macOS application and distributed as a `.dmg` installer. Users won't need to install Python, conda, or any dependencies - everything is bundled!

### Quick Build Guide

#### Option 1: Conda Build **Recommended**

For users who already have conda environment set up.

**Build:**
```bash
# Ensure conda environment is activated
conda activate birdcam

# Build the app
pythonw packaging/macos/pyinstaller.py
```

#### Option 2: Portable Build (No Conda)

Bundles all system dependencies for maximum portability. Requires Homebrew dependencies.

**Setup (one-time):**
```bash
# Install system dependencies (macOS)
brew install graphviz cairo
```

**Build:**
```bash
python packaging/macos/pyinstaller_portable.py
```

### Creating DMG Installer

After building the app, create a DMG installer for distribution:

```bash
./packaging/macos/create_dmg.sh
```

This creates `BirdCam-Installer.dmg` (~34 MB) in the project root.

### Build Outputs

After building, you'll find:

```
dist/
└── BirdCam.app              # Standalone application

BirdCam-Installer.dmg        # DMG installer (distribute this!)
```

### Distribution

**Give users:** `BirdCam-Installer.dmg`

Users can simply:
1. Download and open the DMG file
2. Drag BirdCam.app to Applications folder
3. Launch BirdCam - no dependencies needed!

### Build Scripts Comparison

| Script | Conda Required | Complexity | Best For |
|--------|---------------|------------|----------|
| `pyinstaller.py` | Yes | Medium | Conda users (recommended) |
| `pyinstaller_portable.py` | No | High | Maximum portability, non-conda users |

### Packaging Directory Structure

```
packaging/
├── README.md                    # Packaging documentation
└── macos/                       # macOS build scripts
    ├── pyinstaller.py           # Conda-based build (recommended)
    ├── pyinstaller_portable.py  # Portable build for non-conda users
    ├── pyi_rth_graphviz.py      # PyInstaller runtime hook
    └── create_dmg.sh            # Creates DMG installer
```

For detailed packaging documentation, see [packaging/README.md](packaging/README.md).
