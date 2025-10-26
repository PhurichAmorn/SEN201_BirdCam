# SEN201_BirdCam

Software Engineering Process Project (Pseudocode to Flowchart)

## Team Members

- Phurich Amornnara
- Thanakit Thanasuwanditee
- Phasin Noomkan
- Puttipong Srisuwantat

## Project Overview

This project focuses on converting pseudocode to flowcharts as part of the Software Engineering Process course (SEN201).

## Documentation

- **[BIRDCAM_pseudocode_standard](birdcam_pseudocode_standard.txt)** - Complete reference guide for pseudocode conventions used in this course, including syntax rules, formatting guidelines, and examples.

## Files

- `BIRDCAM_pseudocode_standard.txt` - Comprehensive pseudocode standard documentation

## Requirements

### Using Conda Environment (Recommended for macOS)

This project includes an `environment.yml` file that sets up all required dependencies including proper GUI support for macOS.

To create and use the conda environment:

```bash
# Create the environment (first time only)
conda env create -f environment.yml

# Activate the environment
conda activate birdcam
```

### Using pip

Alternatively, this project includes a **[BIRDCAM_REQUIREMENT](requirements.txt)** file at the repository root which lists the Python packages needed to run and test the project.

To install the required packages into your active Python environment, run:

```bash
python -m pip install -r requirements.txt
```

### Development dependencies

Development and test tools should be kept separate from runtime dependencies. Install requirements from `dev-requirements.txt` to get packages used only during development.

Install development dependencies with:

```bash
python -m pip install -r dev-requirements.txt
```

Common dev commands:

```bash
# Run tests
pytest -q
```

Keep `requirements.txt` for packages required by the application at runtime and `dev-requirements.txt` for tools used during development.

## Running the Application

After setting up the environment, run the GUI application:

```bash
# Activate conda environment first
conda activate birdcam

# Run the GUI (macOS)
pythonw src/gui.py
```

**Note for macOS users:** Use `pythonw` instead of `python` to ensure the GUI windows appear properly in the foreground with full macOS integration.

**Alternative:** You can also use the provided shell script:

```bash
./run_gui.sh
```

## Running tests

Unit tests are in the `tests/` folder. To run them, execute:

```bash
pytest -q
```
