"""
PyInstaller runtime hook for graphviz
Sets up environment so graphviz can find the dot executable and plugins
"""
import os
import sys

# Add the bundle directory to PATH so graphviz can find dot executable
if hasattr(sys, '_MEIPASS'):
    bundle_dir = sys._MEIPASS
    # Add bundle directory to PATH
    os.environ['PATH'] = bundle_dir + os.pathsep + os.environ.get('PATH', '')

    # Set GRAPHVIZ_DOT to point to bundled dot executable
    dot_path = os.path.join(bundle_dir, 'dot')
    if os.path.exists(dot_path):
        os.environ['GRAPHVIZ_DOT'] = dot_path
