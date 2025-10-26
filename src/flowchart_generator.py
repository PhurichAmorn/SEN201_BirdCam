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
        
        # Graph settings for better readability
        self.dot.attr(rankdir="TB")  # Top to bottom layout
        self.dot.attr(splines="ortho")  # Orthogonal edges
        self.dot.attr(nodesep="0.8")  # Horizontal spacing between nodes
        self.dot.attr(ranksep="0.8")  # Vertical spacing between ranks
        
        # Font settings
        self.dot.attr(fontname="Arial")
        self.dot.attr(fontsize="12")
        
        # Node default styling
        self.dot.attr('node', 
                      style='filled',
                      fontname="Arial",
                      fontsize="11",
                      margin="0.2,0.1")
        
        # Edge default styling
        self.dot.attr('edge',
                      fontname="Arial",
                      fontsize="10",
                      fontcolor="blue")
        
        self.node_count = 0  # int - counter for unique node naming
        self.stack = []  # list - stack to track nested control structures
        self.last_node = None  # str - name of the most recently created node

    def new_node(self, label, shape="box", color="lightgrey"):
        """
        Create a new Graphviz node
        Arg:
            label - str, the text to display in the node
            shape - str, the shape of the node (default: "box")
            color - str, the fill color of the node (default: "lightgrey")
        Return:
            str - the unique name identifier of the created node
        """
        self.node_count += 1
        name = f"n{self.node_count}"  # str - unique node identifier
        
        # Customize node appearance based on shape
        if shape == "diamond":
            self.dot.node(name, label, 
                         shape=shape, 
                         fillcolor=color,
                         width="2.0",
                         height="1.2")
        elif shape == "circle":
            self.dot.node(name, label, 
                         shape="circle", 
                         fillcolor=color,
                         width="0.8",
                         height="0.8",
                         fixedsize="true")
        else:
            self.dot.node(name, label, 
                         shape=shape, 
                         fillcolor=color,
                         style="rounded,filled")
        
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
            if label:
                self.dot.edge(src, dst, xlabel=label, fontcolor="blue", fontsize="10")
            else:
                self.dot.edge(src, dst)

    def add_flow(self):
        """
        Main builder logic to connect tokens and create flowchart structure
        Return:
            Digraph - the complete flowchart diagram object
        """
        start_node = self.new_node("Start", shape="circle", color="#90EE90")
        self.last_node = start_node

        # For IF blocks we'll store: {'type':'IF','node':node,'indent':indent,'else_seen':False,'merge':None}
        for i, token in enumerate(self.tokens):
            ttype = token["type"].upper().strip()
            text = token.get("text", token.get("content", "")).strip()
            indent = token.get("indent", 0)

            # CONTROL-STRUCTURES
            if ttype in {"IF", "WHILE", "FOR"}:
                node = self.new_node(text, shape="diamond", color="#87CEEB")
                # connect from last node to this control node
                self.connect(self.last_node, node)

                if ttype == "IF":
                    self.stack.append({
                        "type": "IF",
                        "node": node,
                        "indent": indent,
                        "else_seen": False,
                        "merge": None
                    })
                else:
                    # loops: simpler entry
                    self.stack.append({
                        "type": ttype,
                        "node": node,
                        "indent": indent
                    })
                self.last_node = node
                continue

            # ENDINGS BLOCKS
            elif ttype.startswith("END"):
                if not self.stack:
                    continue
                block = self.stack.pop()
                btype = block["type"]
                start_node = block["node"]

                if btype == "IF":
                    # create merge point (if not already created at ELSE)
                    merge_node = block.get("merge")
                    if merge_node is None:
                        merge_node = self.new_node("", shape="circle", color="white")
                    # connect whatever the last action was to the merge
                    self.connect(self.last_node, merge_node)
                    if not block.get("else_seen", False):
                        self.connect(start_node, merge_node, label="No")
                    # Set last_node to merge so next nodes continue from merge point
                    self.last_node = merge_node
                elif btype in {"FOR", "WHILE"}:
                    # loop: connect last action back to loop start (Loop) and create an exit
                    self.connect(self.last_node, start_node, label="Loop")
                    exit_node = self.new_node("", shape="circle", color="white")
                    self.connect(start_node, exit_node, label="Exit")
                    self.last_node = exit_node
                continue

            # ELSE handling
            elif ttype == "ELSE":
                if self.stack and self.stack[-1]["type"] == "IF":
                    block = self.stack[-1]
                    if_node = block["node"]

                    # Create merge node now
                    merge_node = block.get("merge")
                    if merge_node is None:
                        merge_node = self.new_node("", shape="circle", color="white")
                        block["merge"] = merge_node

                    # Connect current last action to merge
                    self.connect(self.last_node, merge_node)

                    block["else_seen"] = True
                    self.last_node = if_node
                continue

            # REGULAR OPERATIONS (SET, PRINT, etc.)
            else:
                if ttype == "PRINT":
                    node = self.new_node(text, shape="box", color="#FFD700")
                elif ttype == "SET":
                    node = self.new_node(text, shape="box", color="#F0E68C")
                else:
                    node = self.new_node(text, shape="box", color="#D3D3D3")

                # Special-case: if the last token was an IF, this node is the first statement of the Yes branch
                if self.stack and self.stack[-1]["type"] == "IF" and i > 0:
                    prev_token = self.tokens[i-1]
                    if prev_token["type"].upper().strip() == "IF":
                        if_node = self.stack[-1]["node"]
                        self.connect(if_node, node, label="Yes")
                    elif prev_token["type"].upper().strip() == "ELSE":
                        if_node = self.stack[-1]["node"]
                        self.connect(if_node, node, label="No")
                    else:
                        self.connect(self.last_node, node)
                else:
                    self.connect(self.last_node, node)
                self.last_node = node
                continue

        # Add End node
        end_node = self.new_node("End", shape="circle", color="#FFB6C1")
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
    tokens = [# list - sample tokenized pseudocode
        # 1st test case
        # {"type": "SET", "text": "set total = 0", "indent": 0},
        # {"type": "FOR", "text": "for x in range 0 to 10", "indent": 0},
        # {"type": "IF", "text": "if x%2 equals 0", "indent": 1},
        # {"type": "SET", "text": "set total = total + x", "indent": 2},
        # {"type": "ENDIF", "text": "endif", "indent": 1},
        # {"type": "ENDFOR", "text": "endfor", "indent": 0},
        # {"type": "PRINT", "text": 'print "Total: {total}"', "indent": 0},
    
        # 2nd testcase with nested FOR and WHILE loops
        # {"type": "SET", "text": "set sum = 0", "indent": 0},
        # {"type": "FOR", "text": "for i in range 1 to 5", "indent": 0},
        # {"type": "FOR", "text": "for j in range 1 to 3", "indent": 1},
        # {"type": "SET", "text": "set sum = sum + (i * j)", "indent": 2},
        # {"type": "PRINT", "text": 'print "i={i}, j={j}, sum={sum}"', "indent": 2},
        # {"type": "ENDFOR", "text": "endfor", "indent": 1},
        # {"type": "ENDFOR", "text": "endfor", "indent": 0},
        # {"type": "PRINT", "text": 'print "Final sum: {sum}"', "indent": 0},

        # 3rd testcase with nested FOR loops and IF condition
        # {"type": "SET", "text": "set count = 0", "indent": 0},
        # {"type": "FOR", "text": "for row in range 1 to 10", "indent": 0},
        # {"type": "FOR", "text": "for col in range 1 to 10", "indent": 1},
        # {"type": "IF", "text": "if row equals col", "indent": 2},
        # {"type": "SET", "text": "set count = count + 1", "indent": 3},
        # {"type": "PRINT", "text": 'print "Diagonal: ({row},{col})"', "indent": 3},
        # {"type": "ENDIF", "text": "endif", "indent": 2},
        # {"type": "ENDFOR", "text": "endfor", "indent": 1},
        # {"type": "ENDFOR", "text": "endfor", "indent": 0},
        # {"type": "PRINT", "text": 'print "Total diagonal elements: {count}"', "indent": 0},

        # 4th testcase nested if
        {"type": "SET", "text": "set score = 85", "indent": 0},
        {"type": "IF", "text": "if score >= 90", "indent": 0},
        {"type": "PRINT", "text": 'print "Grade: A"', "indent": 1},
        {"type": "ELSE", "text": "else", "indent": 0},
        {"type": "IF", "text": "if score >= 80", "indent": 1},
        {"type": "PRINT", "text": 'print "Grade: B"', "indent": 2},
        {"type": "ELSE", "text": "else", "indent": 1},
        {"type": "PRINT", "text": 'print "Grade: C or below"', "indent": 2},
        {"type": "ENDIF", "text": "endif", "indent": 1},
        {"type": "ENDIF", "text": "endif", "indent": 0},

    ]

    fc = FlowchartBuilder(tokens)  # FlowchartBuilder - flowchart builder instance
    fc.render("flowchart_general")

# output
"""
flowchart_general.png file
"""