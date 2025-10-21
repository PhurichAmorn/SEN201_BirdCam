# export_flowchart.py Documentation

## Overview

The `export_flowchart.py` module provides functionality to export pseudocode-generated flowcharts into PNG format. It integrates with the FlowchartBuilder class from the flowchart_generator module to construct the visual diagram and offers a simple file dialog interface for users to choose the save location and filename.

**Author:** Phurich Amornnara (Phu)  
**Date:** 19/10/2025

### Flowchart Exporter

FileLoader is responsible for loading the pseudocode file (.psc) and store the path and content of the file as string.

**Attributes:**
- `token` (list[dict]): A list of pseudocode tokens
- `builder` (FlowchartBuilder): Use to craete the flowchart diagram

**Example:**
```python
exporter = FlowchartExporter(tokens)
```

#### Methods

##### export_file()

```python
export_file(self, default_name: str = "flowchart") -> None
```

Opens a save file dialog, generates the flowchart using the provided pseudocode tokens, and exports it as a PNG image on the selected file path.

**Parameters:**
- `deafault_name` (str): Path to the pseudocode file

**Example:**
```python
tokens = [
    {"type": "SET", "text": "set total = 0", "indent": 0},
    {"type": "FOR", "text": "for x in range 0 to 10", "indent": 0},
    {"type": "IF", "text": "if x%2 equals 0", "indent": 1},
    {"type": "SET", "text": "set total = total + x", "indent": 2},
    {"type": "ENDIF", "text": "endif", "indent": 1},
    {"type": "ENDFOR", "text": "endfor", "indent": 0},
    {"type": "PRINT", "text": 'print "Total: {total}"', "indent": 0},
]

exporter = FlowchartExporter(tokens)
exporter.export_file(default_name="flowchart")
```

#### load_file_dialog()
```python
load_file_dialog(self) -> str
```
Opens a file dialog and allow the user to browse and select the pseudocode file (.psc). Then the file is loaded and returned as string.

**Example**
```python
loader = FileLoader()
code = loader.load_file_dialog()
```

## Usage Examples

### Basic Usage

```python
from export_flowchart import FlowchartExporter

exporter = FlowchartExporter(demo_tokens)
exporter.export_file(default_name="flowchart")
```

## Notes

- This module only export the flowchart file as a PNG format
- The user can choose the path where the file will be exported and the name of the file

## Error Handling

- If the user cancels the save dialog, the program will not create any file.