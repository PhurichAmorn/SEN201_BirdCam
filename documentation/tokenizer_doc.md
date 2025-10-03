# Tokenizer.py Documentation

## Overview

The `tokenizer.py` module provides functionality for tokenizing pseudocode text according to the BIRDCAM standard. It breaks down pseudocode into structured tokens, identifying control flow statements, operations, and maintaining information about indentation and line numbers.

**Author:** Phasin Noomkan (Nine)  
**Date:** 27/09/2025

## Components

### 1. Type Enumeration

An enumeration defining all supported token types in the pseudocode language.

**Available Types:**
- `IF` - Conditional statement
- `ELSE` - Alternative conditional branch
- `ENDIF` - End of conditional block
- `FOR` - Loop statement
- `ENDFOR` - End of for loop
- `WHILE` - While loop statement
- `ENDWHILE` - End of while loop
- `DO` - Do statement
- `SET` - Variable assignment
- `PRINT` - Output statement
- `GET` - Input statement
- `STATEMENT` - Generic statement (default for unrecognized lines)

### 2. Token Class

A named tuple representing a single token in the pseudocode.

**Attributes:**
- `type` (Type): The token type from the Type enumeration
- `value` (str): The actual text content of the line
- `line_number` (int): The line number in the source code
- `indent_level` (int): The indentation level (0, 1, 2, ...)

**Example:**
```python
Token(type=Type.SET, value="set total = 0", line_number=1, indent_level=0)
```

### 3. PseudocodeTokenizer Class

The main tokenizer class that processes pseudocode text and converts it into a list of tokens.

#### Constructor

```python
PseudocodeTokenizer(tab_size: int = 4)
```

**Parameters:**
- `tab_size` (int, optional): Number of spaces that constitute one indentation level. Default is 4.

#### Class Attributes

- `CONTROL_KEYWORDS`: Set of control flow keywords (`if`, `else`, `endif`, `for`, `endfor`, `while`, `repeatwhile`, `endwhile`)
- `OPERATION_KEYWORDS`: Set of operation keywords (`set`, `print`, `get`, `do`)

#### Methods

##### tokenize_file()

```python
tokenize_file(filename: str) -> List[Token]
```

Reads a pseudocode file and tokenizes its content.

**Parameters:**
- `filename` (str): Path to the pseudocode file

**Returns:**
- `List[Token]`: List of Token objects

**Raises:**
- `FileNotFoundError`: If the specified file doesn't exist

**Example:**
```python
tokenizer = PseudocodeTokenizer()
tokens = tokenizer.tokenize_file("program.pseudo")
```

##### tokenize_text()

```python
tokenize_text(text: str) -> List[Token]
```

Tokenizes pseudocode text directly from a string.

**Parameters:**
- `text` (str): Raw pseudocode as a string

**Returns:**
- `List[Token]`: List of Token objects

**Example:**
```python
code = """
set x = 5
if x > 0
    print x
endif
"""
tokenizer = PseudocodeTokenizer()
tokens = tokenizer.tokenize_text(code)
```

##### print_tokens()

```python
print_tokens(tokens: List[Token]) -> None
```

Prints tokens in a human-readable format for debugging purposes.

**Parameters:**
- `tokens` (List[Token]): List of tokens to display

**Output Format:**
```
Tokens:
--------------------------------------------------
 1. [Type.SET  ] set total = 0
     Line: 1, Indent: 0
--------------------------------------------------
```

#### Private Methods

##### _calculate_indent_level()

Calculates the indentation level of a line based on leading whitespace.

**Parameters:**
- `line` (str): A single line of pseudocode

**Returns:**
- `int`: Indentation level

##### _identify_token_type()

Identifies the token type based on the line's starting keyword.

**Parameters:**
- `line` (str): A single line of pseudocode

**Returns:**
- `Type`: The identified token type (defaults to `Type.STATEMENT` for unrecognized lines)

## Usage Examples

### Basic Usage

```python
from tokenizer import PseudocodeTokenizer

# Create tokenizer instance
tokenizer = PseudocodeTokenizer()

# Tokenize text
code = """
set total = 0
for x in range 0 to 10
    if x%2 equals 0
        set total = total + x
    endif
endfor
print "Total: {total}"
"""

tokens = tokenizer.tokenize_text(code)

# Print tokens for debugging
tokenizer.print_tokens(tokens)
```

### Processing Tokens

```python
# Iterate through tokens
for token in tokens:
    if token.type == Type.IF:
        print(f"Found conditional at line {token.line_number}")
    elif token.type == Type.SET:
        print(f"Found assignment: {token.value}")
```

### Custom Tab Size

```python
# Use 2 spaces for indentation instead of 4
tokenizer = PseudocodeTokenizer(tab_size=2)
tokens = tokenizer.tokenize_text(code)
```

## Token Recognition Rules

1. **Case Insensitive**: Keywords are matched case-insensitively
2. **Keyword Matching**: A line is identified by its starting keyword
3. **Whitespace**: Leading whitespace determines indentation level
4. **Empty Lines**: Empty lines are automatically skipped
5. **Default Type**: Any line not starting with a recognized keyword is classified as `Type.STATEMENT`

## Notes

- The tokenizer handles indentation automatically based on leading whitespace
- Lines are numbered starting from 1
- Indentation levels start from 0
- The tokenizer is designed for the BIRDCAM pseudocode standard
- Token values preserve the original line content (stripped of leading/trailing whitespace)

## Error Handling

The module includes basic error handling:
- `FileNotFoundError` is raised when attempting to tokenize a non-existent file
- Empty lines are silently skipped during tokenization
- Unrecognized lines are classified as generic statements rather than raising errors