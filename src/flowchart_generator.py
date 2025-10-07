"""
flowchart_generator.py

This module generates flowcharts from tokenized pseudocode using Graphviz.

Author: Thanakit Thanasuwanditee(Wave)
Date: 07/10/2025
"""

from graphviz import Digraph

class FlowchartBuilder:
    def __init__(self, tokens):
        self.tokens = tokens
        self.dot = Digraph("Flowchart", format="png")
        self.dot.attr(rankdir="TB", fontname="Arial", size="8,10")
        self.dot.attr('node', style='rounded,filled', fillcolor='white')
        self.node_count = 0
        self.stack = []
        self.last_node = None

    def new_node(self, label, shape="rectangle", color="lightgrey"):
        """Create a new Graphviz node."""
        self.node_count += 1
        name = f"n{self.node_count}"
        self.dot.node(name, label, shape=shape, fillcolor=color)
        return name

    def connect(self, src, dst, label=""):
        """Create a directional edge between two nodes."""
        if src and dst:
            self.dot.edge(src, dst, label=label)

    def add_flow(self):
        """Main builder logic to connect tokens."""
        start_node = self.new_node("Start", shape="circle", color="lightyellow")
        self.last_node = start_node

        for i, token in enumerate(self.tokens):
            ttype = token["type"].upper().strip()
            text = token.get("text", token.get("content", "")).strip()
            indent = token.get("indent", 0)

            # Determine node shape and color by type
            if ttype in {"IF", "WHILE", "FOR"}:
                node = self.new_node(text, shape="diamond", color="lightblue")
                self.connect(self.last_node, node)
                
                if ttype == "IF":
                    # For IF statements, we need to handle the Yes/No branches
                    self.stack.append((ttype, node, indent, self.last_node))
                else:
                    self.stack.append((ttype, node, indent))
                self.last_node = node

            elif ttype.startswith("END"):
                # Match block ending (ENDIF, ENDFOR, ENDWHILE, etc.)
                if self.stack:
                    block_info = self.stack.pop()
                    block_type = block_info[0]
                    start_node = block_info[1]
                    
                    if block_type == "IF":
                        # For IF blocks, create a merge point after ENDIF
                        merge_node = self.new_node("", shape="circle", color="white")
                        self.connect(self.last_node, merge_node)
                        
                        # Connect the IF node's "No" branch to the merge point
                        self.connect(start_node, merge_node, label="No")
                        
                        self.last_node = merge_node
                    elif block_type in {"FOR", "WHILE"}:
                        # Connect last action to block start to form a loop
                        self.connect(self.last_node, start_node, label="Next")
                        
                        # Create exit point for loop
                        exit_node = self.new_node("", shape="circle", color="white")
                        self.connect(start_node, exit_node, label="Exit")
                        self.last_node = exit_node
                continue

            elif ttype == "ELSE":
                # Handle else branch
                if self.stack and self.stack[-1][0] == "IF":
                    if_node = self.stack[-1][1]
                    # Mark that we're in else branch
                    self.last_node = if_node
                continue

            else:
                # Regular operation (SET, PRINT, RETURN, CALL, etc.)
                node = self.new_node(text, shape="rectangle", color="lightgrey")
                
                # Check if we're right after an IF statement
                if self.stack and self.stack[-1][0] == "IF" and i > 0:
                    prev_token = self.tokens[i-1]
                    if prev_token["type"].upper() == "IF":
                        # This is the first statement in the IF block (Yes branch)
                        if_node = self.stack[-1][1]
                        self.connect(if_node, node, label="Yes")
                    else:
                        self.connect(self.last_node, node)
                else:
                    self.connect(self.last_node, node)
                
                self.last_node = node

        # Add End node
        end_node = self.new_node("End", shape="circle", color="lightyellow")
        self.connect(self.last_node, end_node)

        return self.dot

    def render(self, filename="flowchart"):
        """Render and save the flowchart."""
        dot = self.add_flow()
        dot.render(filename, cleanup=True)
        print(f"✅ Flowchart generated: {filename}.png")

if __name__ == "__main__":
    tokens = [
        {"type": "SET", "text": "set total = 0", "indent": 0},
        {"type": "FOR", "text": "for x in range 0 to 10", "indent": 0},
        {"type": "IF", "text": "if x%2 equals 0", "indent": 1},
        {"type": "SET", "text": "set total = total + x", "indent": 2},
        {"type": "ENDIF", "text": "endif", "indent": 1},
        {"type": "ENDFOR", "text": "endfor", "indent": 0},
        {"type": "PRINT", "text": 'print "Total: {total}"', "indent": 0},
    ]

    fc = FlowchartBuilder(tokens)
    fc.render("flowchart_general")
