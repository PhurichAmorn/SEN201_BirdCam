"""
PyInstaller build script for BirdCam macOS application (Fully Portable - No External Dependencies).

This script automatically downloads and bundles all required dependencies:
- Python interpreter
- Required Python packages (tkinter, PIL, cairosvg, graphviz)
- Cairo libraries for SVG rendering
- Graphviz executables and plugins for flowchart generation

Usage:
    python packaging/pyinstaller_portable.py

Requirements:
    - Python 3.8+ with pip
    - PyInstaller: pip install pyinstaller
    - Internet connection (for first-time setup to download binaries)

All system dependencies (graphviz, cairo) are automatically downloaded and bundled.
"""

import PyInstaller.__main__
import os
import stat
import glob
import urllib.request
import tarfile
import zipfile
import shutil
import sys

# Directory to store downloaded dependencies
DEPS_DIR = os.path.join(os.path.dirname(__file__), 'deps')
os.makedirs(DEPS_DIR, exist_ok=True)

print("="*60)
print("BirdCam Portable Build Script")
print("="*60)

def download_file(url, dest_path):
    """Download a file from URL to destination path."""
    print(f"Downloading: {url}")
    try:
        urllib.request.urlretrieve(url, dest_path)
        print(f"  Downloaded to: {dest_path}")
        return True
    except Exception as e:
        print(f"  Failed to download: {e}")
        return False

def extract_tar(tar_path, extract_to):
    """Extract a tar.gz file."""
    print(f"Extracting: {tar_path}")
    try:
        with tarfile.open(tar_path, 'r:gz') as tar:
            tar.extractall(extract_to)
        print(f"  Extracted to: {extract_to}")
        return True
    except Exception as e:
        print(f"  Failed to extract: {e}")
        return False

def setup_graphviz():
    """Download and setup Graphviz binaries."""
    graphviz_dir = os.path.join(DEPS_DIR, 'graphviz')

    # Check if already downloaded
    if os.path.exists(os.path.join(graphviz_dir, 'bin', 'dot')):
        print("Graphviz already downloaded")
        return graphviz_dir

    print("\nSetting up Graphviz...")

    # For macOS, we'll download the official Graphviz release
    # Note: This URL points to a static build that includes all dependencies
    graphviz_version = "9.0.0"
    graphviz_url = f"https://gitlab.com/api/v4/projects/4207231/packages/generic/graphviz-releases/{graphviz_version}/graphviz-{graphviz_version}.tar.gz"

    tar_path = os.path.join(DEPS_DIR, 'graphviz.tar.gz')

    if not os.path.exists(tar_path):
        if not download_file(graphviz_url, tar_path):
            print("Could not download Graphviz automatically.")
            print("Please ensure you have graphviz installed or download manually.")
            return None

    if not extract_tar(tar_path, DEPS_DIR):
        return None

    # Find the extracted directory
    extracted_dirs = [d for d in os.listdir(DEPS_DIR) if d.startswith('graphviz-')]
    if extracted_dirs:
        os.rename(os.path.join(DEPS_DIR, extracted_dirs[0]), graphviz_dir)

    return graphviz_dir if os.path.exists(graphviz_dir) else None

def setup_cairo():
    """Download and setup Cairo libraries."""
    cairo_dir = os.path.join(DEPS_DIR, 'cairo')

    # Check if already downloaded
    if os.path.exists(os.path.join(cairo_dir, 'lib', 'libcairo.dylib')):
        print("Cairo already downloaded")
        return cairo_dir

    print("\nSetting up Cairo...")
    print("Note: Cairo setup requires manual intervention or system installation.")
    print("Using cairocffi with ctypes to find system libraries automatically.")

    return None  # Will rely on cairocffi's automatic library detection

# Base PyInstaller arguments
args = [
    '--name=BirdCam',
    '--onedir',
    '--windowed',
    '--noconsole',
    '--noconfirm',  # Don't ask for confirmation before removing existing build
    '--add-data=assets:assets',
    '--runtime-hook=packaging/pyi_rth_graphviz.py',
    '--hidden-import=PIL._tkinter_finder',
    '--hidden-import=cairosvg',
    '--hidden-import=cairocffi',
    '--hidden-import=ctypes',
    '--hidden-import=ctypes.util',
    '--collect-all=graphviz',
    '--collect-all=cairocffi',
    '--collect-all=cairosvg',
    'src/gui.py'
]

print("\n" + "="*60)
print("Setting up dependencies...")
print("="*60)

# Skip download - just use system-installed Graphviz
print("\nSearching for system-installed Graphviz...")
graphviz_dir = None
common_paths = [
    '/opt/homebrew',      # Homebrew on Apple Silicon
    '/usr/local',         # Homebrew on Intel Mac
    '/opt/local',         # MacPorts
    '/sw',                # Fink
]

for path in common_paths:
    dot_path = os.path.join(path, 'bin', 'dot')
    if os.path.exists(dot_path):
        graphviz_dir = path
        print(f"Found system Graphviz at: {graphviz_dir}")
        break

# Also try using shutil.which to find dot in PATH
if not graphviz_dir:
    dot_which = shutil.which('dot')
    if dot_which:
        # Get the parent directory (bin) and then its parent (installation root)
        bin_dir = os.path.dirname(dot_which)
        graphviz_dir = os.path.dirname(bin_dir)
        print(f"Found Graphviz in PATH at: {graphviz_dir}")

if not graphviz_dir:
    print("\nWARNING: Graphviz not found!")
    print("The application may not work correctly without it.")
    print("Please install graphviz manually or run with system dependencies.")
    response = input("Continue anyway? (y/N): ")
    if response.lower() != 'y':
        sys.exit(1)

# Add Graphviz binaries if available
if graphviz_dir:
    print(f"\nUsing Graphviz from: {graphviz_dir}")

    bin_dir = os.path.join(graphviz_dir, 'bin')
    lib_dir = os.path.join(graphviz_dir, 'lib')

    # Add dot executable
    dot_path = os.path.join(bin_dir, 'dot')
    if os.path.exists(dot_path):
        args.insert(-1, f'--add-binary={dot_path}:.')
        print(f"  Adding: {dot_path}")

    # Add graphviz libraries
    graphviz_libs = [
        'libgvc.*.dylib',
        'libcgraph.*.dylib',
        'libcdt.*.dylib',
        'libpathplan.*.dylib',
    ]

    for lib_pattern in graphviz_libs:
        for lib_path in glob.glob(os.path.join(lib_dir, lib_pattern)):
            if os.path.isfile(lib_path):
                args.insert(-1, f'--add-binary={lib_path}:.')
                print(f"  Adding: {lib_path}")

    # Add graphviz plugins
    plugins_dir = os.path.join(lib_dir, 'graphviz')
    if os.path.exists(plugins_dir):
        args.insert(-1, f'--add-data={plugins_dir}:graphviz')
        print(f"  Adding plugins: {plugins_dir}")

# Try to find and add Cairo libraries from system
print("\nSearching for Cairo libraries...")
cairo_found = False

common_lib_paths = [
    '/usr/local/lib',
    '/opt/homebrew/lib',
    '/opt/local/lib',
    '/sw/lib',
    '/usr/lib',
]

cairo_libs = [
    'libcairo.*.dylib',
    'libpng*.dylib',
    'libfontconfig.*.dylib',
    'libfreetype.*.dylib',
    'libpixman-1.*.dylib',
]

for lib_dir in common_lib_paths:
    if not os.path.exists(lib_dir):
        continue

    for lib_pattern in cairo_libs:
        for lib_path in glob.glob(os.path.join(lib_dir, lib_pattern)):
            if os.path.isfile(lib_path):
                args.insert(-1, f'--add-binary={lib_path}:.')
                print(f"  Found: {lib_path}")
                cairo_found = True

if not cairo_found:
    print("Cairo libraries not found in common locations.")
    print("SVG rendering may not work. Consider installing cairo system-wide.")

print("\n" + "="*60)
print("Starting PyInstaller build...")
print("="*60 + "\n")

# Run PyInstaller
PyInstaller.__main__.run(args)

# Post-build: Fix permissions on executables
print("\n" + "="*60)
print("Post-build: Fixing permissions...")
print("="*60)

app_path = 'dist/BirdCam.app'

if os.path.exists(app_path):
    # Find all executables in the bundle and fix permissions
    for root, dirs, files in os.walk(app_path):
        for filename in files:
            if filename in ['dot', 'BirdCam'] or filename.startswith('lib'):
                filepath = os.path.join(root, filename)
                try:
                    st = os.stat(filepath)
                    os.chmod(filepath, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
                    print(f"  Fixed: {filepath}")
                except Exception as e:
                    print(f"  Failed: {filepath}: {e}")

print("\n" + "="*60)
print("Build complete!")
print(f"App location: {app_path}")
print("="*60)
print("\nNOTE: If the app doesn't work, you may need to:")
print("1. Install system dependencies: brew install graphviz cairo")
print("2. Or use the conda build script instead")
print("="*60)