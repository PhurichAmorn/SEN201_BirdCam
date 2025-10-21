"""
export_flowchart.py

This module let the program export flowcharts to PNG format
with a file dialog to let the user choose location of the save and filename.

Author: Phurich Amornnara (Phu)
Date: 12/10/2025
"""

from flowchart_generator import FlowchartBuilder
from tkinter import filedialog, Tk
import os

class FlowchartExporter:
    def __init__(self, tokens):
        self.tokens = tokens
        self.builder = FlowchartBuilder(tokens)

    def export_file(self, default_name="flowchart"):
        """
        Open a file save dialog and export the flowchart as a PNG.
        """
        # Hide root Tk window
        root = Tk()
        root.withdraw()

        # Ask the user where the file will save into
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            initialfile=default_name,
            filetypes=(("PNG files", "*.png"),),
            title="Save Flowchart As"
        )
        root.destroy()

        if file_path:
            # Generate and render the flowchart
            dot = self.builder.add_flow()
            dot.format = "png"

            # Render without double extensions
            base_name, _ = os.path.splitext(file_path)
            output_path = dot.render(base_name, cleanup=True)
            
            print(f"Flowchart exported: {output_path}")
        else:
            print("Export canceled!")


if __name__ == "__main__":
    # Test the flowchart export
    demo_tokens = [
        {"type": "SET", "text": "set total = 0", "indent": 0},
        {"type": "FOR", "text": "for x in range 0 to 10", "indent": 0},
        {"type": "IF", "text": "if x%2 equals 0", "indent": 1},
        {"type": "SET", "text": "set total = total + x", "indent": 2},
        {"type": "ENDIF", "text": "endif", "indent": 1},
        {"type": "ENDFOR", "text": "endfor", "indent": 0},
        {"type": "PRINT", "text": 'print "Total: {total}"', "indent": 0},
    ]

    exporter = FlowchartExporter(demo_tokens)
    exporter.export_file(default_name="flowchart_demo")
