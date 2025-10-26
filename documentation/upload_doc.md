# upload.py Documentation

## Overview

The `upload.py` module provides functionality for importing pseudocode files (.psc) into Python as text strings. It is responsible for validating file types, ensuring the file exists, and reading its contents for further processing in the pseudocode-to-flowchart pipeline.

**Author:** Phurich Amornnara (Phu)  
**Date:** 03/10/2025

### File Loader

FileLoader is responsible for loading the pseudocode file (.psc) and store the path and content of the file as string.

**Attributes:**
- `filepath` (str): Path to the current pseudocode file
- `content` (str): Content of the file

**Example:**
```python
loader = FileLoader()
```

#### Methods

##### load_file()

```python
load_file(self, path: str) -> str:
```

Reads a pseudocode file and return the content as string

**Parameters:**
- `path` (str): Path to the pseudocode file

**Returns:**
- `content` (str): content of the pseudocode file

**Raises:**
- `FileNotFoundError`: If the file doesn't exist
- `ValueError`: If the file suffix is not .psc 

**Example:**
```python
loader = FileLoader()
code = loader.load_file("example.psc")
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
from upload import FileLoader

loader = FileLoader()
code = loader.load_file_dialog()

if code:
    print("File loaded successfully!")
    print(code)
else:
    print("No file was selected.")
```

## Notes

- The module strictly accepts .psc files for pseudocode input.
- File reading is performed using UTF-8 encoding to support Unicode characters.

## Error Handling

- `FileNotFoundError` is raised when the program load the file that does not exist
- The file must have a suffix as .psc else the error `ValueError` will be raised