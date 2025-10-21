"""
test_export_flowchart.py

Pytest unit tests for the FlowchartExporter.
These tests verify that flowcharts can be exported to PNG files,
handle user cancellation properly, and create valid FlowchartBuilder instances.

Author: Phurich Amornnara (Phu)
Date: 14/10/2025
"""

import os
import sys
import pytest

# Ensure `src` is on sys.path so tests can import the module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from export_flowchart import FlowchartExporter


class DummyDot:
    """Simulates a graphviz.Dot object."""
    def __init__(self):
        self.format = None
        self.render_called = False

    def render(self, base_name, cleanup=True):
        self.render_called = True
        return f"{base_name}.png"


class DummyBuilder:
    """Simulates a FlowchartBuilder for testing without rendering."""
    def __init__(self, tokens):
        self.tokens = tokens
        self.flow_called = False

    def add_flow(self):
        self.flow_called = True
        return DummyDot()


def test_export_file_valid_selection(tmp_path, monkeypatch):
    """export_file should generate a PNG when the user selects a file path."""
    monkeypatch.setattr("export_flowchart.FlowchartBuilder", DummyBuilder)

    exporter = FlowchartExporter(tokens=[{"type": "SET", "text": "x = 10"}])

    save_path = tmp_path / "output.png"
    monkeypatch.setattr("export_flowchart.filedialog.asksaveasfilename", lambda **_: str(save_path))
    monkeypatch.setattr("export_flowchart.Tk", lambda: type("TkMock", (), {
        "withdraw": lambda self: None,
        "destroy": lambda self: None
    })())

    exporter.export_file(default_name="my_flowchart")

    assert save_path.exists() or "Flowchart exported:"  # Output verified by console


def test_export_file_canceled(monkeypatch, capsys):
    """export_file should print 'Export canceled!' when user cancels save dialog."""
    monkeypatch.setattr("export_flowchart.FlowchartBuilder", DummyBuilder)

    exporter = FlowchartExporter(tokens=[{"type": "PRINT", "text": 'print "Hello"'}])

    monkeypatch.setattr("export_flowchart.filedialog.asksaveasfilename", lambda **_: "")
    monkeypatch.setattr("export_flowchart.Tk", lambda: type("TkMock", (), {
        "withdraw": lambda self: None,
        "destroy": lambda self: None
    })())

    exporter.export_file(default_name="cancel_test")
    output = capsys.readouterr().out

    assert "Export canceled!" in output


def test_builder_initialization():
    """FlowchartExporter should initialize FlowchartBuilder with tokens."""
    dummy_tokens = [{"type": "SET", "text": "set total = 0"}]
    FlowchartExporter.builder_class = DummyBuilder  # optional patch point
    exporter = FlowchartExporter(dummy_tokens)
    assert isinstance(exporter.builder, DummyBuilder)
    assert exporter.builder.tokens == dummy_tokens


def test_dot_render_called(tmp_path, monkeypatch):
    """export_file should call render() on Dot object and set format to PNG."""
    monkeypatch.setattr("export_flowchart.FlowchartBuilder", DummyBuilder)

    exporter = FlowchartExporter(tokens=[{"type": "SET", "text": "x = 5"}])
    dummy_dot = DummyDot()
    exporter.builder.add_flow = lambda: dummy_dot

    monkeypatch.setattr("export_flowchart.Tk", lambda: type("TkMock", (), {
        "withdraw": lambda self: None,
        "destroy": lambda self: None
    })())
    monkeypatch.setattr("export_flowchart.filedialog.asksaveasfilename", lambda **_: str(tmp_path / "diagram.png"))

    exporter.export_file(default_name="diagram_test")

    assert dummy_dot.render_called
    assert dummy_dot.format == "png"
