#!/bin/bash
#
# This script installs all required dependencies
# to run the BirdCam application on openSUSE (WSL).
#
echo "This will install required system libraries:"
echo "  - graphviz (for flowcharts)"
echo "  - graphviz-plugin-gd (for PNG/JPG support)"
echo "  - libxcb1 (for windowing)"
echo "  - fontconfig, libXft2, dejavu-fonts (for fonts)"
echo ""
echo "You may be asked for your password."

sudo zypper install -y graphviz graphviz-plugin-gd libxcb1 fontconfig libXft2 dejavu-fonts

echo ""
echo "Installation complete."
echo "The Application will now start"
./BirdCam