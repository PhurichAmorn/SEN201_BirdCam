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

# Get conda environment path
conda_prefix = os.environ.get('CONDA_PREFIX', '')

# If CONDA_PREFIX is not set or points to base environment, use fixed path
# Uncomment and modify the line below if you need to specify a custom path:
# conda_prefix = '/Users/YOUR_USERNAME/miniconda3/envs/birdcam'

if not conda_prefix:
    conda_prefix = os.path.expanduser('~/miniconda3/envs/birdcam')

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

PyInstaller.__main__.run(args)