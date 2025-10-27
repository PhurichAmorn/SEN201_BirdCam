# macOS Build Scripts

Scripts for building BirdCam as a standalone macOS application.

---

## Files

| File | Purpose |
|------|---------|
| `pyinstaller.py` | Conda-based build (recommended) |
| `pyinstaller_portable.py` | Portable build for non-conda users |
| `pyi_rth_graphviz.py` | Runtime hook for graphviz |
| `create_dmg.sh` | Creates DMG installer |

---

## Usage

**Option 1: Conda Build (Recommended)**
```bash
conda activate birdcam
pythonw packaging/macos/pyinstaller.py
```

**Option 2: Portable Build**
```bash
brew install graphviz cairo
python packaging/macos/pyinstaller_portable.py
```

**Create DMG Installer**
```bash
./packaging/macos/create_dmg.sh
```

---

## Output

- `dist/BirdCam.app` - Standalone application
- `BirdCam-Installer.dmg` - DMG installer

See [main documentation](../../README.md#building--distribution) for complete instructions.
