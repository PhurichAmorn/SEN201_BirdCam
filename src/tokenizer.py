"""
Tokenizer.py

This module handles the basic tokenization of pseudocode text.
It breaks down the pseudocode into lines and identifies basic structure.

Author: Phasin Noomkan(Nine)
Date: 27/09/2025
"""

from typing import List, NamedTuple
from enum import Enum
from upload import FileLoader

class Type(Enum):
    """Enumeration of token types"""
    IF = 1
    ELSE = 2
    ENDIF = 3
    FOR = 4
    ENDFOR = 5
    WHILE = 6
    ENDWHILE = 7
    SET = 8
    PRINT = 9
    GET = 10
    DO = 11
    STATEMENT = 12


class Token(NamedTuple):
    """Represents a single token in pseudocode"""
    type: Type         # Type of token (e.g., 'IF', 'SET', 'FOR', etc.)
    value: str         # The actual text content
    line_number: int   # Line number in source
    indent_level: int  # Indentation level (0, 1, 2, ...)


class PseudocodeTokenizer:
    """
    Tokenizes pseudocode according to the standard.

    """

    # Keywords defined in BIRDCAM standard
    CONTROL_KEYWORDS = {
        'if', 'else', 'endif',
        'for', 'endfor',
        'while', 'repeatwhile', 'endwhile'
    }

    OPERATION_KEYWORDS = {
        'set', 'print', 'get', 'do'
    }

    def __init__(self, tab_size: int = 4):
        """The initializer which initializes tokenizer with tab size for indentation calculation"""
        self.tab_size = tab_size

    def tokenize_file(self, filename: str) -> List[Token]:
        """
        Read and tokenize a pseudocode file
        ARGS:
            filename: Path to the pseudocode file
        RETURNS:
            List of Token objects
        """

        loader = FileLoader()
        code = loader.load_file(filename)
        return self.tokenize_text(code)
    

    def tokenize_text(self, text: str) -> List[Token]:
        """
        Tokenize pseudocode text into a list of tokens
        ARGS:
            text: Raw pseudocode as a string
        RETURNS:
            List of Token objects
        """
        lines = text.strip().split('\n')  # Split into lines
        tokens = []

        for line_num, line in enumerate(lines, 1):
            if not line.strip():  # Skip empty lines
                continue

            indent_level = self._calculate_indent_level(line)
            clean_line = line.strip()
            token_type = self._identify_token_type(clean_line)

            token = Token(
                type=token_type,
                value=clean_line,
                line_number=line_num,
                indent_level=indent_level
            )
            tokens.append(token)

        return tokens

    def _calculate_indent_level(self, line: str) -> int:
        """
        Calculate the indentation level of a line
        ARGS:
            line: A single line of pseudocode
        RETURNS:
            Indentation level as an integer
        """
        leading_whitespace = len(line) - len(line.lstrip())
        return leading_whitespace // self.tab_size

    def _identify_token_type(self, line: str) -> Type:
        """
        Identify the type of token based on the line content
        ARGS:
            line: A single line of pseudocode
        RETURNS:
            Token type as a string
        """
        keyword_map = {
            "if": Type.IF,
            "else": Type.ELSE,
            "endif": Type.ENDIF,
            "for": Type.FOR,
            "endfor": Type.ENDFOR,
            "while": Type.WHILE,
            "endwhile": Type.ENDWHILE,
            "set": Type.SET,
            "print": Type.PRINT,
            "get": Type.GET,
            "do": Type.DO,
        }

        # Convert to lowercase for keyword matching
        line_lower = line.lower()

        for keyword, token_type in keyword_map.items():
            if line_lower.startswith(keyword + ' ') or line_lower == keyword:
                return token_type

        # Default to STATEMENT for anything else
        return Type.STATEMENT

    def print_tokens(self, tokens: List[Token]) -> None:
        """
        Print tokens in a readable format (for debugging)
        ARGS:
            tokens: List of Token objects to print
        RETURNS:
            None
        """
        print("Tokens:")
        print("-" * 50)
        for i, token in enumerate(tokens):
            indent = "  " * token.indent_level
            print(f"{i+1:2d}. {indent}[{token.type:10s}] {token.value}")
            print(
                f"     Line: {token.line_number}, Indent: {token.indent_level}")
        print("-" * 50)


if __name__ == "__main__":
    # Simple test of the tokenizer
    sample_code = """
set total = 0
for x in range 0 to 10
    if x%2 equals 0
        set total = total + x
    endif
endfor
print "Total of even numbers from 0 to 10: {total}" 
    """

    tokenizer = PseudocodeTokenizer()
    tokens = tokenizer.tokenize_text(sample_code)
    tokenizer.print_tokens(tokens)


# Output:
"""
--------------------------------------------------
 1. [Type.SET  ] set total = 0
     Line: 1, Indent: 0
 2. [Type.FOR  ] for x in range 0 to 10
     Line: 2, Indent: 0
 3.   [Type.IF   ] if x%2 equals 0
     Line: 3, Indent: 1
 4.     [Type.SET  ] set total = total + x
     Line: 4, Indent: 2
 5.   [Type.ENDIF] endif
     Line: 5, Indent: 1
 6. [Type.ENDFOR] endfor
     Line: 6, Indent: 0
 7. [Type.PRINT] print "Total of even numbers from 0 to 10: {total}"
     Line: 7, Indent: 0
--------------------------------------------------

"""
