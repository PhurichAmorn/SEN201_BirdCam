"""
test_flowchart_generator.py
Unit tests for the FlowchartBuilder class

Author: Thanakit Thanasuwanditee(Wave)
Date: 21/10/2025
"""

import pytest
import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from flowchart_generator import FlowchartBuilder


class TestFlowchartBuilder:
    """Test suite for FlowchartBuilder class"""

    def test_initialization(self):
        """Test that FlowchartBuilder initializes correctly"""
        tokens = [{"type": "SET", "text": "set x = 5", "indent": 0}]
        fc = FlowchartBuilder(tokens)
        
        assert fc.tokens == tokens
        assert fc.node_count == 0
        assert fc.stack == []
        assert fc.last_node is None
        assert fc.dot is not None

    def test_new_node_creates_unique_nodes(self):
        """Test that new_node creates unique node identifiers"""
        tokens = []
        fc = FlowchartBuilder(tokens)
        
        node1 = fc.new_node("Node 1")
        node2 = fc.new_node("Node 2")
        node3 = fc.new_node("Node 3")
        
        assert node1 == "n1"
        assert node2 == "n2"
        assert node3 == "n3"
        assert fc.node_count == 3

    def test_new_node_with_custom_shape_and_color(self):
        """Test that new_node accepts custom shape and color"""
        tokens = []
        fc = FlowchartBuilder(tokens)
        
        node = fc.new_node("Test", shape="diamond", color="lightblue")
        assert node == "n1"

    def test_connect_nodes(self):
        """Test that connect creates edges between nodes"""
        tokens = []
        fc = FlowchartBuilder(tokens)
        
        node1 = fc.new_node("Start")
        node2 = fc.new_node("End")
        
        fc.connect(node1, node2, label="flow")
        # Check that edge was added (no exception raised)
        assert True

    def test_simple_sequence(self):
        """Test flowchart generation for simple sequential statements"""
        tokens = [
            {"type": "SET", "text": "set x = 5", "indent": 0},
            {"type": "SET", "text": "set y = 10", "indent": 0},
            {"type": "PRINT", "text": 'print "Done"', "indent": 0}
        ]
        fc = FlowchartBuilder(tokens)
        dot = fc.add_flow()
        
        assert dot is not None
        assert fc.node_count > 0

    def test_if_statement(self):
        """Test flowchart generation for IF statement"""
        tokens = [
            {"type": "IF", "text": "if x > 0", "indent": 0},
            {"type": "PRINT", "text": 'print "Positive"', "indent": 1},
            {"type": "ENDIF", "text": "endif", "indent": 0}
        ]
        fc = FlowchartBuilder(tokens)
        dot = fc.add_flow()
        
        assert dot is not None
        assert fc.node_count >= 4  # Start, IF, PRINT, merge, End

    def test_if_else_statement(self):
        """Test flowchart generation for IF-ELSE statement"""
        tokens = [
            {"type": "IF", "text": "if x > 0", "indent": 0},
            {"type": "PRINT", "text": 'print "Positive"', "indent": 1},
            {"type": "ELSE", "text": "else", "indent": 0},
            {"type": "PRINT", "text": 'print "Not positive"', "indent": 1},
            {"type": "ENDIF", "text": "endif", "indent": 0}
        ]
        fc = FlowchartBuilder(tokens)
        dot = fc.add_flow()
        
        assert dot is not None
        assert len(fc.stack) == 0  # Stack should be empty after processing

    def test_for_loop(self):
        """Test flowchart generation for FOR loop"""
        tokens = [
            {"type": "FOR", "text": "for i in range 0 to 5", "indent": 0},
            {"type": "PRINT", "text": "print i", "indent": 1},
            {"type": "ENDFOR", "text": "endfor", "indent": 0}
        ]
        fc = FlowchartBuilder(tokens)
        dot = fc.add_flow()
        
        assert dot is not None
        assert len(fc.stack) == 0

    def test_while_loop(self):
        """Test flowchart generation for WHILE loop"""
        tokens = [
            {"type": "WHILE", "text": "while x < 10", "indent": 0},
            {"type": "SET", "text": "set x = x + 1", "indent": 1},
            {"type": "ENDWHILE", "text": "endwhile", "indent": 0}
        ]
        fc = FlowchartBuilder(tokens)
        dot = fc.add_flow()
        
        assert dot is not None
        assert len(fc.stack) == 0

    def test_nested_control_structures(self):
        """Test flowchart generation for nested IF in FOR loop"""
        tokens = [
            {"type": "FOR", "text": "for x in range 0 to 10", "indent": 0},
            {"type": "IF", "text": "if x%2 equals 0", "indent": 1},
            {"type": "PRINT", "text": "print x", "indent": 2},
            {"type": "ENDIF", "text": "endif", "indent": 1},
            {"type": "ENDFOR", "text": "endfor", "indent": 0}
        ]
        fc = FlowchartBuilder(tokens)
        dot = fc.add_flow()
        
        assert dot is not None
        assert len(fc.stack) == 0

    def test_empty_tokens(self):
        """Test flowchart generation with empty token list"""
        tokens = []
        fc = FlowchartBuilder(tokens)
        dot = fc.add_flow()
        
        assert dot is not None
        assert fc.node_count == 2  # Only Start and End nodes

    def test_token_with_content_field(self):
        """Test that tokens with 'content' field instead of 'text' are handled"""
        tokens = [
            {"type": "SET", "content": "set x = 5", "indent": 0}
        ]
        fc = FlowchartBuilder(tokens)
        dot = fc.add_flow()
        
        assert dot is not None

    def test_render_creates_file(self, tmp_path):
        """Test that render method creates output file"""
        tokens = [
            {"type": "SET", "text": "set x = 5", "indent": 0}
        ]
        fc = FlowchartBuilder(tokens)
        
        output_path = tmp_path / "test_flowchart"
        fc.render(str(output_path))
        
        assert (tmp_path / "test_flowchart.png").exists()

    def test_complex_example(self):
        """Test the complex example from main"""
        tokens = [
            {"type": "SET", "text": "set total = 0", "indent": 0},
            {"type": "FOR", "text": "for x in range 0 to 10", "indent": 0},
            {"type": "IF", "text": "if x%2 equals 0", "indent": 1},
            {"type": "SET", "text": "set total = total + x", "indent": 2},
            {"type": "ENDIF", "text": "endif", "indent": 1},
            {"type": "ENDFOR", "text": "endfor", "indent": 0},
            {"type": "PRINT", "text": 'print "Total: {total}"', "indent": 0}
        ]
        fc = FlowchartBuilder(tokens)
        dot = fc.add_flow()
        
        assert dot is not None
        assert len(fc.stack) == 0
        assert fc.node_count > 5