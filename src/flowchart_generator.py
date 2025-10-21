"""
flowchart_generator.py
Generates flowcharts from tokenized pseudocode using Graphviz

Author: Thanakit Thanasuwanditee(Wave)
Date: 07/10/2025
"""

from graphviz import Digraph

class FlowchartBuilder:
    """
    Class to build flowcharts from tokenized pseudocode
    """
    def __init__(self, tokens):
        """
        Initialize the flowchart builder with tokens
        Arg:
            tokens - list of token dictionaries containing type, text, and indent information
        """
        self.tokens = tokens  # list - tokenized pseudocode input
        self.dot = Digraph("Flowchart", format="png")  # Digraph - graphviz diagram object
        self.dot.attr(splines="ortho")
        self.dot.attr(rankdir="TB", fontname="Arial", size="8,10")
        self.dot.attr('node', style='rounded,filled', fillcolor='white')
        self.node_count = 0  # int - counter for unique node naming
        self.stack = []  # list - stack to track nested control structures
        self.last_node = None  # str - name of the most recently created node

    def new_node(self, label, shape="rectangle", color="lightgrey"):
        """
        Create a new Graphviz node
        Arg:
            label - str, the text to display in the node
            shape - str, the shape of the node (default: "rectangle")
            color - str, the fill color of the node (default: "lightgrey")
        Return:
            str - the unique name identifier of the created node
        """
        self.node_count += 1
        name = f"n{self.node_count}"  # str - unique node identifier
        self.dot.node(name, label, shape=shape, fillcolor=color)
        return name

    def connect(self, src, dst, label=""):
        """
        Create a directional edge between two nodes
        Arg:
            src - str, the source node identifier
            dst - str, the destination node identifier
            label - str, optional label for the edge (default: "")
        """
        if src and dst:
            self.dot.edge(src, dst, label=label)

    def add_flow(self):
        """
        Main builder logic to connect tokens and create flowchart structure
        Return:
            Digraph - the complete flowchart diagram object
        """
        start_node = self.new_node("Start", shape="circle", color="lightyellow")  # str - starting node identifier
        self.last_node = start_node

        for i, token in enumerate(self.tokens):
            ttype = token["type"].upper().strip()  # str - token type in uppercase
            text = token.get("text", token.get("content", "")).strip()  # str - token text content
            indent = token.get("indent", 0)  # int - indentation level of the token

            # Determine node shape and color by type
            if ttype in {"IF", "WHILE", "FOR"}:
                node = self.new_node(text, shape="diamond", color="lightblue")  # str - control structure node
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
                    block_info = self.stack.pop()  # tuple - information about the control block
                    block_type = block_info[0]  # str - type of control structure
                    start_node = block_info[1]  # str - starting node of the control block
                    
                    if block_type == "IF":
                        # For IF blocks, create a merge point after ENDIF
                        merge_node = self.new_node("", shape="circle", color="white")  # str - merge point node
                        self.connect(self.last_node, merge_node)
                        
                        # Connect the IF node's "No" branch to the merge point
                        self.connect(start_node, merge_node, label="No")
                        
                        self.last_node = merge_node
                    elif block_type in {"FOR", "WHILE"}:
                        # Connect last action to block start to form a loop
                        self.connect(self.last_node, start_node, label="Next")
                        
                        # Create exit point for loop
                        exit_node = self.new_node("", shape="circle", color="white")  # str - loop exit node
                        self.connect(start_node, exit_node, label="Exit")
                        self.last_node = exit_node
                continue

            elif ttype == "ELSE":
                # Handle else branch
                if self.stack and self.stack[-1][0] == "IF":
                    if_node = self.stack[-1][1]  # str - IF statement node identifier
                    # Mark that we're in else branch
                    self.last_node = if_node
                continue

            else:
                # Regular operation (SET, PRINT, RETURN, CALL, etc.)
                node = self.new_node(text, shape="rectangle", color="lightgrey")  # str - operation node
                
                # Check if we're right after an IF statement
                if self.stack and self.stack[-1][0] == "IF" and i > 0:
                    prev_token = self.tokens[i-1]  # dict - previous token in the list
                    if prev_token["type"].upper() == "IF":
                        # This is the first statement in the IF block (Yes branch)
                        if_node = self.stack[-1][1]  # str - IF statement node identifier
                        self.connect(if_node, node, label="Yes")
                    else:
                        self.connect(self.last_node, node)
                else:
                    self.connect(self.last_node, node)
                
                self.last_node = node

        # Add End node
        end_node = self.new_node("End", shape="circle", color="lightyellow")  # str - ending node identifier
        self.connect(self.last_node, end_node)

        return self.dot

    def render(self, filename="flowchart"):
        """
        Render and save the flowchart to a file
        Arg:
            filename - str, the output filename without extension (default: "flowchart")
        """
        dot = self.add_flow()  # Digraph - complete flowchart diagram
        dot.render(filename, cleanup=True)
        print(f"Flowchart generated: {filename}.png")

if __name__ == "__main__":
    # Example test tokens to demonstrate flowchart generation
    tokens = [  # list - sample tokenized pseudocode
        {"type": "SET", "text": "set total = 0", "indent": 0},
        {"type": "FOR", "text": "for x in range 0 to 10", "indent": 0},
        {"type": "IF", "text": "if x%2 equals 0", "indent": 1},
        {"type": "SET", "text": "set total = total + x", "indent": 2},
        {"type": "ENDIF", "text": "endif", "indent": 1},
        {"type": "ENDFOR", "text": "endfor", "indent": 0},
        {"type": "PRINT", "text": 'print "Total: {total}"', "indent": 0},
    ]

    fc = FlowchartBuilder(tokens)  # FlowchartBuilder - flowchart builder instance
    fc.render("flowchart_general")

# output
"""
flowchart_general.png file
"""
