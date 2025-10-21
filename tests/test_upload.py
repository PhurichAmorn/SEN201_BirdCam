"""
test_upload.py

Pytest unit tests for the upload module.
These tests verify correct file loading, error handling, and file type validation.

Author: Phurich Amornnara (Phu)
Date: 14/10/2025
"""

import os
import sys
import pytest

# Ensure `src` is on sys.path so tests can import the upload module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from upload import FileLoader


def test_load_valid_psc_file(tmp_path):
    """load_file should correctly read a valid .psc file and store its contents."""
    loader = FileLoader()

    # Create a temporary .psc file
    file_path = tmp_path / "example.psc"
    content = "set total = 0\nprint total"
    file_path.write_text(content, encoding="utf-8")

    result = loader.load_file(str(file_path))

    assert result == content
    assert loader.filepath == str(file_path)
    assert loader.content == content


def test_load_file_not_found(tmp_path):
    """load_file should raise FileNotFoundError for a missing file."""
    loader = FileLoader()
    missing_file = tmp_path / "nonexistent.psc"

    with pytest.raises(FileNotFoundError):
        loader.load_file(str(missing_file))


def test_load_file_invalid_extension(tmp_path):
    """load_file should raise ValueError for a non-.psc file."""
    loader = FileLoader()

    # Create a fake text file
    invalid_file = tmp_path / "example.txt"
    invalid_file.write_text("some text", encoding="utf-8")

    with pytest.raises(ValueError, match=r"Invalid file type.*Only '.psc' files are allowed"):
        loader.load_file(str(invalid_file))


def test_load_file_dialog_no_selection(monkeypatch):
    """load_file_dialog should print a message and return empty string when user cancels dialog."""

    loader = FileLoader()

    # Mock filedialog.askopenfilename to simulate "no file selected"
    monkeypatch.setattr("upload.filedialog.askopenfilename", lambda **kwargs: "")
    monkeypatch.setattr("upload.Tk", lambda: type("DummyTk", (), {"withdraw": lambda self: None, "destroy": lambda self: None})())

    result = loader.load_file_dialog()
    assert result == ""


def test_load_file_dialog_valid_selection(monkeypatch, tmp_path):
    """load_file_dialog should load content when a valid file is selected."""

    loader = FileLoader()

    # Create a sample file
    file_path = tmp_path / "sample.psc"
    content = "set x = 10"
    file_path.write_text(content, encoding="utf-8")

    # Mock file dialog to return our file path
    monkeypatch.setattr("upload.filedialog.askopenfilename", lambda **kwargs: str(file_path))
    monkeypatch.setattr("upload.Tk", lambda: type("DummyTk", (), {"withdraw": lambda self: None, "destroy": lambda self: None})())

    result = loader.load_file_dialog()
    assert result == content
    assert loader.filepath == str(file_path)
    assert loader.content == content
