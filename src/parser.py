"""
Parser.py

This module parses tokenized pseudocode into an Abstract Syntax Tree (AST).
It builds upon the tokenizer to create a structured representation of the code.

Author: Phasin Noomkan(Nine)  
Date: 28/09/2025
"""

from typing import List, Optional
from abc import ABC
from tokenizer import Token, Type, PseudocodeTokenizer 


"""
ASTNode Structure:
 ├── Statement (base for all statements, adds line_number)
 │    ├── SetStatement
 │    ├── PrintStatement
 │    ├── GetStatement
 │    ├── DoStatement
 │    ├── GenericStatement
 │    ├── IfStatement
 │    ├── ForStatement
 │    └── WhileStatement
 │
 ├── Block (list of statements, used inside loops/ifs)
 └── Program (root of the AST, holds top-level statements)
"""

# AST Node Classes
class ASTNode(ABC):
    """Base class for all AST nodes"""
    pass


class Statement(ASTNode):
    """Base class for all statement nodes"""

    def __init__(self, line_number: int):
        self.line_number = line_number


class Block(ASTNode):
    """Represents a block of statements"""

    def __init__(self, statements: List[Statement]):
        self.statements = statements


class Program(ASTNode):
    """Root node representing the entire program"""

    def __init__(self, statements: List[Statement]):
        self.statements = statements


class SetStatement(Statement):
    """Represents a SET statement: set variable = value"""

    def __init__(self, line_number: int, variable: str, value: str):
        super().__init__(line_number)
        self.variable = variable
        self.value = value


class PrintStatement(Statement):
    """Represents a PRINT statement: print message"""

    def __init__(self, line_number: int, message: str):
        super().__init__(line_number)
        self.message = message


class GetStatement(Statement):
    """Represents a GET statement: get variable"""

    def __init__(self, line_number: int, variable: str):
        super().__init__(line_number)
        self.variable = variable


class DoStatement(Statement):
    """Represents a DO statement: do function_name"""

    def __init__(self, line_number: int, function_name: str):
        super().__init__(line_number)
        self.function_name = function_name


class GenericStatement(Statement):
    """Represents any other statement not specifically handled"""

    def __init__(self, line_number: int, content: str):
        super().__init__(line_number)
        self.content = content


class IfStatement(Statement):
    """Represents an IF-ELSE-ENDIF block"""

    def __init__(self, line_number: int, condition: str, if_block: Block, else_block: Optional[Block] = None):
        super().__init__(line_number)
        self.condition = condition
        self.if_block = if_block
        self.else_block = else_block


class ForStatement(Statement):
    """Represents a FOR-ENDFOR loop"""

    def __init__(self, line_number: int, iterator: str, iterable: str, body: Block):
        super().__init__(line_number)
        self.iterator = iterator
        self.iterable = iterable
        self.body = body


class WhileStatement(Statement):
    """Represents a WHILE-ENDWHILE loop"""

    def __init__(self, line_number: int, condition: str, body: Block):
        super().__init__(line_number)
        self.condition = condition
        self.body = body


class ParseError(Exception):
    """Exception raised when parsing fails"""

    def __init__(self, message: str, line_number: Optional[int] = None):
        self.message = message
        self.line_number = line_number
        super().__init__(
            f"Parse error at line {line_number}: {message}" if line_number else message)


class PseudocodeParser:
    """
    Parses tokenized pseudocode into an Abstract Syntax Tree (AST)
    """

    def __init__(self):
        self.tokens: List[Token] = []
        self.current = 0

    def parse(self, tokens: List[Token]) -> Program:
        """
        Parse tokens into an AST

        Args:
            tokens: List of tokens from tokenizer

        Returns:
            Program AST node containing all statements
        """
        self.tokens = tokens
        self.current = 0

        statements = []
        while not self._is_at_end():
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)

        return Program(statements)

    def _parse_statement(self) -> Optional[Statement]:
        """
        Parse a single statement
        ARGS:
            None
        RETURNS:
            A Statement AST node or None if end of tokens

        """
        if self._is_at_end():
            return None

        token = self._peek()

        if token.type == Type.SET:
            return self._parse_set_statement()
        elif token.type == Type.PRINT:
            return self._parse_print_statement()
        elif token.type == Type.GET:
            return self._parse_get_statement()
        elif token.type == Type.DO:
            return self._parse_do_statement()
        elif token.type == Type.IF:
            return self._parse_if_statement()
        elif token.type == Type.FOR:
            return self._parse_for_statement()
        elif token.type == Type.WHILE:
            return self._parse_while_statement()
        elif token.type in [Type.ELSE, Type.ENDIF, Type.ENDFOR, Type.ENDWHILE]:
            # These are handled by their parent constructs
            return None
        else:
            return self._parse_generic_statement()

    def _parse_set_statement(self) -> SetStatement:
        """Parse SET statement: set variable = value"""
        token = self._advance()
        content = token.value

        # Extract variable and value from "set variable = value"
        if '=' in content:
            parts = content.split('=', 1)
            if len(parts) == 2:
                variable = parts[0].replace('set', '').strip()
                value = parts[1].strip()
                return SetStatement(token.line_number, variable, value)

        raise ParseError(
            f"Invalid SET statement format: {content}", token.line_number)

    def _parse_print_statement(self) -> PrintStatement:
        """Parse PRINT statement: print message"""
        token = self._advance()
        message = token.value.replace('print', '').strip()
        return PrintStatement(token.line_number, message)

    def _parse_get_statement(self) -> GetStatement:
        """Parse GET statement: get variable"""
        token = self._advance()
        variable = token.value.replace('get', '').strip()
        return GetStatement(token.line_number, variable)

    def _parse_do_statement(self) -> DoStatement:
        """Parse DO statement: do function_name"""
        token = self._advance()
        function_name = token.value.replace('do', '').strip()
        return DoStatement(token.line_number, function_name)

    def _parse_if_statement(self) -> IfStatement:
        """Parse IF-ELSE-ENDIF block"""
        if_token = self._advance()
        condition = if_token.value.replace('if', '').strip()

        # Parse IF block
        if_statements = []
        while not self._is_at_end():
            next_token = self._peek()
            if next_token.type in [Type.ELSE, Type.ENDIF]:
                break
            stmt = self._parse_statement()
            if stmt:
                if_statements.append(stmt)

        if_block = Block(if_statements)

        # Check for ELSE
        else_block = None
        if not self._is_at_end() and self._peek().type == Type.ELSE:
            self._advance()  # consume ELSE
            else_statements = []
            while not self._is_at_end():
                next_token = self._peek()
                if next_token.type == Type.ENDIF:
                    break
                stmt = self._parse_statement()
                if stmt:
                    else_statements.append(stmt)
            else_block = Block(else_statements)

        # Consume ENDIF
        if self._is_at_end() or self._peek().type != Type.ENDIF:
            raise ParseError("Expected ENDIF", if_token.line_number)
        self._advance()

        return IfStatement(if_token.line_number, condition, if_block, else_block)

    def _parse_for_statement(self) -> ForStatement:
        """Parse FOR-ENDFOR loop"""
        for_token = self._advance()
        for_line = for_token.value.replace('for', '').strip()

        # Extract iterator and iterable from "item in collection"
        if ' in ' in for_line:
            parts = for_line.split(' in ', 1) 
            iterator = parts[0].strip()
            iterable = parts[1].strip()
        else:
            raise ParseError(
                f"Invalid FOR statement format: {for_line}", for_token.line_number)

        # Parse body
        body_statements = []
        while not self._is_at_end():
            next_token = self._peek()
            if next_token.type == Type.ENDFOR:
                break
            stmt = self._parse_statement()
            if stmt:
                body_statements.append(stmt)

        # Consume ENDFOR
        if self._is_at_end() or self._peek().type != Type.ENDFOR:
            raise ParseError("Expected ENDFOR", for_token.line_number)
        self._advance()

        body = Block(body_statements)
        return ForStatement(for_token.line_number, iterator, iterable, body)

    def _parse_while_statement(self) -> WhileStatement:
        """Parse WHILE-ENDWHILE loop"""
        while_token = self._advance()
        condition = while_token.value.replace('while', '').strip()

        # Parse body
        body_statements = []
        while not self._is_at_end():
            next_token = self._peek()
            if next_token.type == Type.ENDWHILE:
                break
            stmt = self._parse_statement()
            if stmt:
                body_statements.append(stmt)

        # Consume ENDWHILE
        if self._is_at_end() or self._peek().type != Type.ENDWHILE:
            raise ParseError("Expected ENDWHILE", while_token.line_number)
        self._advance()

        body = Block(body_statements)
        return WhileStatement(while_token.line_number, condition, body)

    def _parse_generic_statement(self) -> GenericStatement:
        """Parse any other statement"""
        token = self._advance()
        return GenericStatement(token.line_number, token.value)

    def _peek(self) -> Token:
        """
        Get current token without advancing
        ARGS:
            None
        RETURNS:
            Current Token object
        """
        if self._is_at_end():
            return self.tokens[-1]  # Return last token if at end
        return self.tokens[self.current]

    def _advance(self) -> Token:
        """Get current token and advance to next"""
        if not self._is_at_end():
            self.current += 1
        return self.tokens[self.current - 1]

    def _is_at_end(self) -> bool:
        """Check if we've reached the end of tokens"""
        return self.current >= len(self.tokens)

    def print_ast(self, node: ASTNode, indent: int = 0) -> None:
        """
        Print AST in a readable format (for debugging)

        Args:
            node: AST node to print
            indent: Current indentation level
        """
        prefix = "  " * indent

        if isinstance(node, Program):
            print(f"{prefix}Program:")
            for stmt in node.statements:
                self.print_ast(stmt, indent + 1)

        elif isinstance(node, SetStatement):
            print(
                f"{prefix}Set: {node.variable} = {node.value} (line {node.line_number})")

        elif isinstance(node, PrintStatement):
            print(f"{prefix}Print: {node.message} (line {node.line_number})")

        elif isinstance(node, GetStatement):
            print(f"{prefix}Get: {node.variable} (line {node.line_number})")

        elif isinstance(node, DoStatement):
            print(f"{prefix}Do: {node.function_name} (line {node.line_number})")

        elif isinstance(node, IfStatement):
            print(f"{prefix}If: {node.condition} (line {node.line_number})")
            print(f"{prefix}  Then:")
            for stmt in node.if_block.statements:
                self.print_ast(stmt, indent + 2)
            if node.else_block:
                print(f"{prefix}  Else:")
                for stmt in node.else_block.statements:
                    self.print_ast(stmt, indent + 2)

        elif isinstance(node, ForStatement):
            print(
                f"{prefix}For: {node.iterator} in {node.iterable} (line {node.line_number})")
            for stmt in node.body.statements:
                self.print_ast(stmt, indent + 1)

        elif isinstance(node, WhileStatement):
            print(f"{prefix}While: {node.condition} (line {node.line_number})")
            for stmt in node.body.statements:
                self.print_ast(stmt, indent + 1)

        elif isinstance(node, GenericStatement):
            print(f"{prefix}Statement: {node.content} (line {node.line_number})")


if __name__ == "__main__":
    # Test the parser with sample code
    sample_code = """
set total = 0
for x in range 0 to 10
    if x%2 equals 0
        set total = total + x
    endif
endfor
print "Total of even numbers from 0 to 10: {total}"
    """

    # Tokenize first
    tokenizer = PseudocodeTokenizer()
    tokens = tokenizer.tokenize_text(sample_code)

    # Parse tokens into AST
    parser = PseudocodeParser()
    ast = parser.parse(tokens)

    # Print the AST
    print("Abstract Syntax Tree:")
    print("=" * 50)
    parser.print_ast(ast)
    print("=" * 50)

# Output:
"""
Abstract Syntax Tree:
==================================================
Program:
  Set: total = 0 (line 1)
  For: x in range 0 to 10 (line 2)
    If: x%2 equals 0 (line 3)
      Then:
        Set: total = total + x (line 4)
  Print: "Total of even numbers from 0 to 10: {total}" (line 7)
==================================================

"""