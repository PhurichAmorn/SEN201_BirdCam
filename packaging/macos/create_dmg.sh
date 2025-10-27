#!/bin/bash
# Script to create a DMG installer for BirdCam

set -e  # Exit on error

APP_NAME="BirdCam"
APP_PATH="dist/${APP_NAME}.app"
DMG_NAME="${APP_NAME}-Installer.dmg"
DMG_TEMP="${APP_NAME}-temp.dmg"
VOLUME_NAME="${APP_NAME} Installer"
SOURCE_FOLDER="dmg_contents"

echo "============================================================"
echo " Creating DMG Installer for ${APP_NAME}"
echo "============================================================"

# Check if app exists
if [ ! -d "$APP_PATH" ]; then
    echo "Error: ${APP_PATH} not found!"
    echo "Please build the app first using one of the build scripts."
    exit 1
fi

# Clean up previous builds
echo "Cleaning up previous builds..."
rm -f "${DMG_NAME}" "${DMG_TEMP}"
rm -rf "${SOURCE_FOLDER}"

# Create source folder
echo "Creating DMG contents folder..."
mkdir -p "${SOURCE_FOLDER}"

# Copy app to source folder
echo "Copying ${APP_NAME}.app..."
cp -R "${APP_PATH}" "${SOURCE_FOLDER}/"

# Create Applications folder symlink for drag-and-drop
echo "Creating Applications symlink..."
ln -s /Applications "${SOURCE_FOLDER}/Applications"

# Optional: Add a background image or README
# You can add custom background: mkdir -p "${SOURCE_FOLDER}/.background" && cp background.png "${SOURCE_FOLDER}/.background/"

echo ""
echo "Creating temporary DMG..."
# Get the size of the source folder (in MB) and add some padding
SIZE=$(du -sm "${SOURCE_FOLDER}" | awk '{print $1}')
SIZE=$((SIZE + 50))  # Add 50 MB padding

# Create temporary DMG
hdiutil create -srcfolder "${SOURCE_FOLDER}" \
    -volname "${VOLUME_NAME}" \
    -fs HFS+ \
    -fsargs "-c c=64,a=16,e=16" \
    -format UDRW \
    -size ${SIZE}m \
    "${DMG_TEMP}"

# Mount the temporary DMG
echo "Mounting temporary DMG..."
MOUNT_DIR=$(hdiutil attach -readwrite -noverify -noautoopen "${DMG_TEMP}" | grep Volumes | awk '{print $3}')

echo "Mounted at: ${MOUNT_DIR}"

# Set window appearance using AppleScript
echo "Setting DMG window appearance..."
osascript <<EOF
tell application "Finder"
    tell disk "${VOLUME_NAME}"
        open
        set current view of container window to icon view
        set toolbar visible of container window to false
        set statusbar visible of container window to false
        set the bounds of container window to {100, 100, 700, 500}
        set viewOptions to the icon view options of container window
        set arrangement of viewOptions to not arranged
        set icon size of viewOptions to 128
        set position of item "${APP_NAME}.app" of container window to {150, 200}
        set position of item "Applications" of container window to {450, 200}
        update without registering applications
        delay 2
        close
    end tell
end tell
EOF

# Unmount
echo "Unmounting temporary DMG..."
# Try to unmount, but don't fail if already unmounted
hdiutil detach "${MOUNT_DIR}" 2>/dev/null || hdiutil detach "/Volumes/${VOLUME_NAME}" 2>/dev/null || echo "DMG already unmounted"
sleep 2  # Give system time to fully unmount

# Convert to compressed, read-only DMG
echo "Creating final compressed DMG..."
hdiutil convert "${DMG_TEMP}" \
    -format UDZO \
    -imagekey zlib-level=9 \
    -o "${DMG_NAME}"

# Clean up
echo "Cleaning up..."
rm -f "${DMG_TEMP}"
rm -rf "${SOURCE_FOLDER}"

echo ""
echo "============================================================"
echo " DMG created successfully!"
echo "============================================================"
echo ""
echo "DMG file: ${DMG_NAME}"
echo "Size: $(du -h "${DMG_NAME}" | awk '{print $1}')"
echo ""
echo "You can now distribute this DMG file to users."
echo "Users can simply:"
echo "  1. Open the DMG file"
echo "  2. Drag ${APP_NAME}.app to Applications folder"
echo "  3. Launch ${APP_NAME} from Applications"
echo ""
echo "============================================================"
