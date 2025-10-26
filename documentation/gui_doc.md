# Gui.py Documentation

## Overview

A GUI application for converting pseudocode files (`.psc`) to visual flowcharts using Python Tkinter.

**Author:** Puttipong Srisuwantat (Non)
**Date:** 01/10/2025

## Features

- **Multi-tab Interface**: Support for multiple flowchart projects simultaneously
- **File Upload**: Upload and edit `.psc` pseudocode files
- **Pseudocode Editor**: Full-featured text editor with scrolling, unlimited lines
- **Editor Controls**: Clear, Undo, Redo, Save, and Generate buttons
- **Interactive Flowchart Display**: Zoom and pan functionality for flowchart viewing
- **Tab Management**: Add new tabs, close tabs, and rename tabs based on file names
- **Cross-platform**: Runs on Windows, macOS, and Linux

## Requirements

- Python 3.6 or higher
- tkinter (usually included with Python)
- Optional: Pillow (PIL) and CairoSVG to render the SVG upload icon (fallback icon is used if not installed)
- Optional: Upload.svg asset placed next to gui.py to display the upload icon
- No additional dependencies required for basic functionality

## Installation

1. Download or clone the repository
2. Ensure Python 3 is installed on your system
3. (Optional) Install extras for the SVG upload icon:
   - pip3 install pillow cairosvg
4. Run the application:
   ```bash
   python3 gui.py
   ```

## Optional: SVG Upload Icon

If Pillow and CairoSVG are installed and an Upload.svg file exists in the project root (same folder as gui.py), the app will render a circular SVG upload icon on the upload screen. Otherwise, it falls back to a built-in canvas icon, and you may see a "Failed to load SVG" message in the console.

- Place Upload.svg in the project root.
- Install extras: pip3 install pillow cairosvg

## Usage

### Starting the Application

1. Run the application script
2. The app opens with a single tab showing the upload screen
3. Click "Choose File" to upload a `.psc` pseudocode file

### Working with Files

1. **Upload**: Click "Choose File" and select a `.psc` file
2. **Edit**: After upload, use the pseudocode editor on the left side
3. **Save**: Use the save button (💾) or Ctrl+S to save changes
4. **Generate**: Click "Generate" to create a flowchart from your pseudocode

### Editor Controls

- **Clear**: Remove all text from the editor
- **Undo** (↩): Undo the last action
- **Redo** (↪): Redo the previously undone action
- **Save** (💾): Save the current file
- **Generate**: Convert pseudocode to flowchart

### Flowchart Interaction

- **Zoom**: Use mouse wheel to zoom in/out on the flowchart
- **Pan**: Click and drag to move around the flowchart
- **Scrollbars**: Use scrollbars for navigation

### Tab Management

- **New Tab**: Use Ctrl/Cmd+T or File menu → New Tab
- **Close Tab**: Use Ctrl/Cmd+W, Middle-click the tab, or right-click → Close Tab
- **Close Other Tabs**: Right-click on a tab → Close Other Tabs
- **Switch Tabs**: Click on tab headers to switch between projects

### Keyboard Shortcuts

- **Ctrl/Cmd+T**: New tab
- **Ctrl/Cmd+O**: Open file in current tab
- **Ctrl/Cmd+S**: Save
- **Ctrl/Cmd+Shift+S**: Save As
- **Ctrl/Cmd+W**: Close current tab
- **Ctrl/Cmd+Z**: Undo
- **Ctrl/Cmd+Shift+Z** or **Ctrl/Cmd+Y**: Redo
- **Ctrl/Cmd+X**: Cut
- **Ctrl/Cmd+C**: Copy
- **Ctrl/Cmd+V**: Paste
- **Ctrl/Cmd+Q**: Exit application

## File Format

The application works with `.psc` files containing pseudocode. Example format:

```
set total_items = 0
set total_vat = 0
set grand_total = 0
for item in item_set
    set vat = 0
    if item_price >= 100
        Set vat = item_price * 0.07
    endif
    print "Name: {item_name} Price: {item_price} VAT: {vat} Price+VAT: {item_price + vat}"
    set total_items = total_items + item_price
    set total_vat = total_vat + vat
    set grand_total = grand_total + item_price + vat
endfor
print "Number of item: {total_items}, VAT: {total_vat}฿, Total: {grand_total}฿"
```

## Architecture

The application consists of two main classes:

- **PseudocodeFlowchartApp**: Main application window with tab management
- **FlowchartTab**: Individual tab handling upload, editing, and flowchart display


## Troubleshooting

- **Application won't start**: Ensure Python 3 and tkinter are properly installed
- **File won't upload**: Check that the file has a `.psc` extension
- **Flowchart not generating**: Currently shows a sample flowchart (implementation in progress)
- **Upload icon not showing / console says "Failed to load SVG"**: Install Pillow and CairoSVG (`pip3 install pillow cairosvg`) and place Upload.svg next to gui.py. If not available, a fallback canvas icon is used automatically.

## TODO

- Complete pseudocode parsing and flowchart generation logic
- Export flowcharts to various formats (PNG, JPG)