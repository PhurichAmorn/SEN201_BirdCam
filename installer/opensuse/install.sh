#!/bin/bash
#
# This script installs the 'graphviz' dependency
# required to run the BirdCam application on openSUSE.
#
echo "This will install the 'graphviz' package."
echo "You may be asked for your password."
sudo zypper install graphviz
echo ""
echo "Installation complete."
echo "The Application will now start"
./BirdCam
