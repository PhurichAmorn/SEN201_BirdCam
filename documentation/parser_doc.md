# Parser.py Documentation

## Overview

The `parser.py` module parses tokenized pseudocode into an Abstract Syntax Tree (AST). It builds upon the tokenizer to create a structured, hierarchical representation of code that can be analyzed, interpreted, or compiled.

**Author:** Phasin Noomkan (Nine)  
**Date:** 28/09/2025

## AST Node Hierarchy

```
ASTNode (abstract base)
 ├── Statement (base for all statements)
 │    ├── SetStatement
 │    ├── PrintStatement
 │    ├── GetStatement
 │    ├── DoStatement
 │    ├── GenericStatement
 │    ├── IfStatement
 │    ├── ForStatement
 │    └── WhileStatement
 │
 ├── Block (container for multiple statements)
 └── Program (root node of the AST)
```

## AST Node Classes

### Base Classes

#### ASTNode

Abstract base class for all AST nodes.

```python
class ASTNode(ABC):
    pass
```

#### Statement

Base class for all statement nodes. All statements track their line number in the source code.

**Attributes:**
- `line_number` (int): Line number in the original source code

```python
class Statement(ASTNode):
    def __init__(self, line_number: int)
```

### Container Classes

#### Block

Represents a block of statements (used inside loops, conditionals, etc.).

**Attributes:**
- `statements` (List[Statement]): List of statements in this block

```python
class Block(ASTNode):
    def __init__(self, statements: List[Statement])
```

#### Program

Root node representing the entire program.

**Attributes:**
- `statements` (List[Statement]): Top-level statements in the program

```python
class Program(ASTNode):
    def __init__(self, statements: List[Statement])
```

### Statement Classes

#### SetStatement

Represents a variable assignment: `set variable = value`

**Attributes:**
- `line_number` (int): Line number in source
- `variable` (str): Variable name being assigned
- `value` (str): Value being assigned

```python
class SetStatement(Statement):
    def __init__(self, line_number: int, variable: str, value: str)
```

**Example:**
```python
# Parses: set total = 0
SetStatement(line_number=1, variable="total", value="0")
```

#### PrintStatement

Represents an output statement: `print message`

**Attributes:**
- `line_number` (int): Line number in source
- `message` (str): Message to print

```python
class PrintStatement(Statement):
    def __init__(self, line_number: int, message: str)
```

#### GetStatement

Represents an input statement: `get variable`

**Attributes:**
- `line_number` (int): Line number in source
- `variable` (str): Variable name to store input

```python
class GetStatement(Statement):
    def __init__(self, line_number: int, variable: str)
```

#### DoStatement

Represents a function call: `do function_name`

**Attributes:**
- `line_number` (int): Line number in source
- `function_name` (str): Name of function to call

```python
class DoStatement(Statement):
    def __init__(self, line_number: int, function_name: str)
```

#### GenericStatement

Represents any statement not specifically handled by other node types.

**Attributes:**
- `line_number` (int): Line number in source
- `content` (str): Full content of the statement

```python
class GenericStatement(Statement):
    def __init__(self, line_number: int, content: str)
```

#### IfStatement

Represents an IF-ELSE-ENDIF conditional block.

**Attributes:**
- `line_number` (int): Line number in source
- `condition` (str): Conditional expression
- `if_block` (Block): Block of statements to execute if condition is true
- `else_block` (Optional[Block]): Block of statements to execute if condition is false (None if no else clause)

```python
class IfStatement(Statement):
    def __init__(self, line_number: int, condition: str, 
                 if_block: Block, else_block: Optional[Block] = None)
```

#### ForStatement

Represents a FOR-ENDFOR loop.

**Attributes:**
- `line_number` (int): Line number in source
- `iterator` (str): Loop variable name
- `iterable` (str): Collection or range being iterated
- `body` (Block): Block of statements in loop body

```python
class ForStatement(Statement):
    def __init__(self, line_number: int, iterator: str, 
                 iterable: str, body: Block)
```

**Example:**
```python
# Parses: for x in range 0 to 10
ForStatement(line_number=2, iterator="x", iterable="range 0 to 10", body=...)
```

#### WhileStatement

Represents a WHILE-ENDWHILE loop.

**Attributes:**
- `line_number` (int): Line number in source
- `condition` (str): Loop condition
- `body` (Block): Block of statements in loop body

```python
class WhileStatement(Statement):
    def __init__(self, line_number: int, condition: str, body: Block)
```

## Exception Classes

### ParseError

Exception raised when parsing fails.

**Attributes:**
- `message` (str): Error description
- `line_number` (Optional[int]): Line number where error occurred

```python
class ParseError(Exception):
    def __init__(self, message: str, line_number: Optional[int] = None)
```

**Example:**
```python
raise ParseError("Expected ENDIF", line_number=5)
# Output: Parse error at line 5: Expected ENDIF
```

## PseudocodeParser Class

The main parser class that converts tokens into an AST.

### Constructor

```python
PseudocodeParser()
```

No parameters required. Initializes internal state for tracking tokens.

**Attributes:**
- `tokens` (List[Token]): List of tokens being parsed
- `current` (int): Current position in token list

### Public Methods

#### parse()

```python
parse(tokens: List[Token]) -> Program
```

Parses a list of tokens into a complete AST.

**Parameters:**
- `tokens` (List[Token]): List of tokens from the tokenizer

**Returns:**
- `Program`: Root AST node containing all parsed statements

**Raises:**
- `ParseError`: If the code has syntax errors

**Example:**
```python
tokenizer = PseudocodeTokenizer()
tokens = tokenizer.tokenize_text(code)

parser = PseudocodeParser()
ast = parser.parse(tokens)
```

#### print_ast()

```python
print_ast(node: ASTNode, indent: int = 0) -> None
```

Prints the AST in a human-readable, indented format for debugging.

**Parameters:**
- `node` (ASTNode): AST node to print
- `indent` (int, optional): Current indentation level. Default is 0.

**Example Output:**
```
Program:
  Set: total = 0 (line 1)
  For: x in range 0 to 10 (line 2)
    If: x%2 equals 0 (line 3)
      Then:
        Set: total = total + x (line 4)
```

### Private Methods

#### _parse_statement()

```python
_parse_statement() -> Optional[Statement]
```

Parses a single statement based on token type.

**Returns:**
- `Optional[Statement]`: Parsed statement or None if at end of tokens

#### _parse_set_statement()

Parses SET statements. Expects format: `set variable = value`

**Returns:**
- `SetStatement`: Parsed assignment statement

**Raises:**
- `ParseError`: If statement doesn't contain '=' or has invalid format

#### _parse_print_statement()

Parses PRINT statements.

**Returns:**
- `PrintStatement`: Parsed print statement

#### _parse_get_statement()

Parses GET statements.

**Returns:**
- `GetStatement`: Parsed input statement

#### _parse_do_statement()

Parses DO statements.

**Returns:**
- `DoStatement`: Parsed function call statement

#### _parse_if_statement()

Parses complete IF-ELSE-ENDIF blocks.

**Returns:**
- `IfStatement`: Parsed conditional statement

**Raises:**
- `ParseError`: If ENDIF is missing

#### _parse_for_statement()

Parses FOR-ENDFOR loops. Expects format: `for iterator in iterable`

**Returns:**
- `ForStatement`: Parsed for loop

**Raises:**
- `ParseError`: If ' in ' is missing or ENDFOR is missing

#### _parse_while_statement()

Parses WHILE-ENDWHILE loops.

**Returns:**
- `WhileStatement`: Parsed while loop

**Raises:**
- `ParseError`: If ENDWHILE is missing

#### _parse_generic_statement()

Parses any unrecognized statement.

**Returns:**
- `GenericStatement`: Generic statement node

#### _peek()

```python
_peek() -> Token
```

Returns the current token without advancing the parser.

#### _advance()

```python
_advance() -> Token
```

Returns the current token and advances to the next one.

#### _is_at_end()

```python
_is_at_end() -> bool
```

Checks if the parser has reached the end of the token list.

## Usage Examples

### Basic Usage

```python
from tokenizer import PseudocodeTokenizer
from parser import PseudocodeParser

# Sample pseudocode
code = """
set total = 0
for x in range 0 to 10
    if x%2 equals 0
        set total = total + x
    endif
endfor
print "Total: {total}"
"""

# Tokenize
tokenizer = PseudocodeTokenizer()
tokens = tokenizer.tokenize_text(code)

# Parse into AST
parser = PseudocodeParser()
ast = parser.parse(tokens)

# Print AST for debugging
parser.print_ast(ast)
```

### Traversing the AST

```python
def count_loops(node):
    """Count total number of loops in the program"""
    count = 0
    
    if isinstance(node, Program):
        for stmt in node.statements:
            count += count_loops(stmt)
    
    elif isinstance(node, (ForStatement, WhileStatement)):
        count += 1
        for stmt in node.body.statements:
            count += count_loops(stmt)
    
    elif isinstance(node, IfStatement):
        for stmt in node.if_block.statements:
            count += count_loops(stmt)
        if node.else_block:
            for stmt in node.else_block.statements:
                count += count_loops(stmt)
    
    return count

total_loops = count_loops(ast)
print(f"Total loops: {total_loops}")
```

### Error Handling

```python
try:
    ast = parser.parse(tokens)
except ParseError as e:
    print(f"Parsing failed: {e}")
    if e.line_number:
        print(f"Check line {e.line_number} in your code")
```

### Accessing Statement Details

```python
for stmt in ast.statements:
    if isinstance(stmt, SetStatement):
        print(f"Assignment: {stmt.variable} = {stmt.value}")
    
    elif isinstance(stmt, IfStatement):
        print(f"Condition: {stmt.condition}")
        print(f"Has else: {stmt.else_block is not None}")
    
    elif isinstance(stmt, ForStatement):
        print(f"Loop: {stmt.iterator} in {stmt.iterable}")
```

## Parsing Rules

### Control Flow Structures

1. **IF Statements**: Must be terminated with ENDIF
   - Optional ELSE clause between IF and ENDIF
   - Supports nested IF statements

2. **FOR Loops**: Must be terminated with ENDFOR
   - Requires ' in ' keyword to separate iterator and iterable
   - Supports nested loops

3. **WHILE Loops**: Must be terminated with ENDWHILE
   - Supports nested loops

### Statement Parsing

- **SET statements**: Must contain '=' for assignment
- **Keywords**: Extracted by removing the keyword prefix and trimming whitespace
- **Generic statements**: Any line not matching known patterns becomes a GenericStatement

### Error Detection

The parser validates:
- Proper termination of control structures (ENDIF, ENDFOR, ENDWHILE)
- Valid SET statement format (contains '=')
- Valid FOR statement format (contains ' in ')

## Integration with Tokenizer

The parser depends on the tokenizer module:

```python
from tokenizer import Token, Type, PseudocodeTokenizer
```

**Required Token Types:**
- `Type.IF`, `Type.ELSE`, `Type.ENDIF`
- `Type.FOR`, `Type.ENDFOR`
- `Type.WHILE`, `Type.ENDWHILE`
- `Type.SET`, `Type.PRINT`, `Type.GET`, `Type.DO`
- `Type.STATEMENT`

## Notes

- The parser maintains line numbers for all statements to help with error reporting and debugging
- Empty blocks are allowed (e.g., an IF with no statements)
- The parser is fault-tolerant for generic statements but strict about control flow structure
- Indentation from tokens is not used in parsing; structure is determined by keywords only
- All string content (conditions, values, messages) is preserved as-is from the tokens