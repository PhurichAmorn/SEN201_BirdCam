"""
PyInstaller build script for BirdCam macOS application.

This script bundles the BirdCam GUI application with all dependencies including:
- Python interpreter
- Required Python packages (tkinter, PIL, cairosvg, graphviz)
- Cairo libraries for SVG rendering
- Graphviz executables and plugins for flowchart generation

Usage:
    pythonw packaging/pyinstaller.py

Requirements:
    - Conda environment 'birdcam' activated with all dependencies installed
    - PyInstaller installed in the environment
"""

import PyInstaller.__main__
import os
import stat
import glob

import sys
conda_prefix = os.environ.get('CONDA_PREFIX', '')

if not conda_prefix or not os.path.exists(os.path.join(conda_prefix, 'bin', 'dot')):
    # Try to get environment from current Python executable
    python_path = sys.executable
    if 'envs' in python_path:
        # Extract environment path from Python executable
        # e.g., /path/to/miniconda3/envs/birdcam/bin/python -> /path/to/miniconda3/envs/birdcam
        conda_prefix = os.path.dirname(os.path.dirname(python_path))

# Uncomment and modify the line below if you need to specify a custom path:
# conda_prefix = '/Users/YOUR_USERNAME/miniconda3/envs/birdcam'

if not conda_prefix or not os.path.exists(os.path.join(conda_prefix, 'bin', 'dot')):
    conda_prefix = os.path.expanduser('~/miniconda3/envs/birdcam')

print(f"Detected conda environment: {conda_prefix}")
print(f"Checking for dot at: {os.path.join(conda_prefix, 'bin', 'dot')}")

args = [
    '--name=BirdCam',
    '--onedir',
    '--windowed',
    '--noconsole',
    '--add-data=assets:assets',
    '--runtime-hook=packaging/pyi_rth_graphviz.py',  # Runtime hook for graphviz
    '--hidden-import=PIL._tkinter_finder',  # Ensure PIL works with tkinter
    '--hidden-import=cairosvg',
    '--hidden-import=cairocffi',
    '--collect-all=graphviz',  # Include graphviz Python package
    'src/gui.py'
]

# Add graphviz binaries and libraries from conda
if conda_prefix and os.path.exists(os.path.join(conda_prefix, 'bin', 'dot')):
    graphviz_bin = os.path.join(conda_prefix, 'bin')
    # Add main dot executable
    args.insert(-1, f'--add-binary={graphviz_bin}/dot:.')

    lib_dir = os.path.join(conda_prefix, 'lib')

    # Add graphviz core libraries
    graphviz_libs = [
        'libgvc.6.dylib',
        'libgvc.dylib',
        'libcgraph.6.dylib',
        'libcgraph.dylib',
        'libcdt.5.dylib',
        'libcdt.dylib',
        'libpathplan.4.dylib',
        'libpathplan.dylib',
    ]

    for lib in graphviz_libs:
        lib_path = os.path.join(lib_dir, lib)
        if os.path.exists(lib_path):
            args.insert(-1, f'--add-binary={lib_path}:.')

    # Add graphviz plugins directory (essential for rendering)
    graphviz_plugins = os.path.join(lib_dir, 'graphviz')
    if os.path.exists(graphviz_plugins):
        args.insert(-1, f'--add-data={graphviz_plugins}:graphviz')

# Add Cairo libraries and dependencies
if conda_prefix:
    lib_dir = os.path.join(conda_prefix, 'lib')

    # Cairo and its dependencies
    cairo_libs = [
        'libcairo.2.dylib',
        'libcairo.dylib',
        'libpng16.16.dylib',
        'libfontconfig.1.dylib',
        'libfreetype.6.dylib',
        'libpixman-1.0.dylib',
        'libz.1.dylib',
        # Additional Cairo modules
        'libcairo-gobject.2.dylib',
        'libcairo-script-interpreter.dylib',
        # Font rendering
        'libharfbuzz.0.dylib',
    ]

    for lib in cairo_libs:
        lib_path = os.path.join(lib_dir, lib)
        if os.path.exists(lib_path):
            args.insert(-1, f'--add-binary={lib_path}:.')

# Run PyInstaller
PyInstaller.__main__.run(args)

# Post-build: Fix permissions on dot executable
print("\nFixing permissions on bundled executables...")
app_path = 'dist/BirdCam.app'

if os.path.exists(app_path):
    # Find all 'dot' executables in the bundle
    for dot_path in glob.glob(f'{app_path}/**/dot', recursive=True):
        try:
            # Add execute permission
            st = os.stat(dot_path)
            os.chmod(dot_path, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
            print(f"  Fixed permissions: {dot_path}")
        except Exception as e:
            print(f"  Failed to fix permissions for {dot_path}: {e}")

print("\nBuild complete! App location: dist/BirdCam.app")