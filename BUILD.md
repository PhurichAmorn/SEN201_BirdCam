# Building BirdCam for macOS

This guide explains how to build a standalone macOS application (.app) and DMG installer for BirdCam.

## Prerequisites

1. **Conda environment** with all dependencies installed:
   ```bash
   conda env create -f environment.yml
   conda activate birdcam
   ```

2. **PyInstaller** installed in the environment:
   ```bash
   pip install pyinstaller
   ```

3. **Assets folder** must contain `Upload.svg`:
   - The SVG file should be located at `assets/Upload.svg`
   - If it's in `src/Upload.svg`, copy it to assets:
     ```bash
     cp src/Upload.svg assets/
     ```

## Build Steps

### 1. Build the Application

Run the PyInstaller build script:
```bash
pythonw packaging/pyinstaller.py
```

This will create:
- `dist/BirdCam.app` - The standalone macOS application
- `build/` - Temporary build files (can be deleted)
- `BirdCam.spec` - PyInstaller specification file

### 2. Create DMG Installer (Optional)

To create a disk image for easy distribution:
```bash
hdiutil create -volname "BirdCam" -srcfolder dist/BirdCam.app -ov -format UDZO BirdCam.dmg
```

This creates `BirdCam.dmg` - a compressed disk image ready for distribution.

## Build Configuration

The build script (`src/pyinstaller.py`) includes:

- **Python interpreter** and all dependencies
- **Cairo libraries** for SVG rendering (`libcairo`, `libpng`, etc.)
- **Graphviz executables** and plugins (`dot`, layout engines)
- **Runtime hook** (`pyi_rth_graphviz.py`) to configure paths at startup
- **Assets folder** with UI resources

## Customizing the Build

### Change Conda Environment Path

Edit `packaging/pyinstaller.py` and uncomment/modify line 26:
```python
conda_prefix = '/Users/YOUR_USERNAME/miniconda3/envs/birdcam'
```

### Modify App Settings

Edit the args list in `packaging/pyinstaller.py`:
- `--name=BirdCam` - Application name
- `--windowed` - No console window (GUI only)
- `--onedir` - Create a directory bundle
- `--add-data=assets:assets` - Include assets folder

## Distribution

### Option 1: Distribute BirdCam.app
- Share the `dist/BirdCam.app` folder
- Users copy it to their Applications folder

### Option 2: Distribute BirdCam.dmg (Recommended)
- Share the `BirdCam.dmg` file
- Users double-click to mount, then drag to Applications
- Standard macOS installation experience

## Troubleshooting

### "Cannot find conda environment"
Make sure you've activated the birdcam environment:
```bash
conda activate birdcam
```

### "Cairo library not found"
Ensure Cairo is installed in your conda environment:
```bash
conda install -c conda-forge cairo
```

### "Graphviz dot executable not found"
Install Graphviz in the conda environment:
```bash
conda install -c conda-forge graphviz
```

### Clean Build
If you encounter issues, clean the build artifacts and try again:
```bash
rm -rf build dist BirdCam.spec
pythonw packaging/pyinstaller.py
```

## Files Used in Build

- `packaging/pyinstaller.py` - Build script
- `packaging/pyi_rth_graphviz.py` - Runtime hook for Graphviz
- `assets/` - Application resources
- `src/gui.py` - Main application entry point
- `environment.yml` - Conda environment specification
- `requirements.txt` - Python dependencies

## System Requirements

- **macOS** 10.14 or later
- **Conda** or **Miniconda** installed
- **Xcode Command Line Tools** (for compiling)

The built application is standalone and doesn't require end users to have Python, Conda, or any dependencies installed.
