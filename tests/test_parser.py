"""
test_parser.py

Pytest unit tests for the pseudocode parser.
These tests exercise AST generation, statement parsing,
and error handling for various pseudocode constructs.

Author: Phasin Noomkan(Nine)  
Date: 10/09/2025
"""

import pytest
import os
import sys

# Ensure `src` is on sys.path so tests can import the parser module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from tokenizer import PseudocodeTokenizer, Token, Type
from parser import (
    PseudocodeParser, Program, SetStatement, PrintStatement, GetStatement,
    DoStatement, IfStatement, ForStatement, WhileStatement, GenericStatement,
    Block, ParseError
)


class TestPseudocodeParser:
    """Test suite for PseudocodeParser class"""

    def setup_method(self):
        """Set up test fixtures before each test method"""
        self.parser = PseudocodeParser()
        self.tokenizer = PseudocodeTokenizer()

    def test_empty_program(self):
        """Test parsing an empty program"""
        tokens = []
        ast = self.parser.parse(tokens)

        assert isinstance(ast, Program)
        assert len(ast.statements) == 0

    def test_set_statement_parsing(self):
        """Test parsing SET statements"""
        code = "set total = 0"
        tokens = self.tokenizer.tokenize_text(code)
        ast = self.parser.parse(tokens)

        assert isinstance(ast, Program)
        assert len(ast.statements) == 1

        stmt = ast.statements[0]
        assert isinstance(stmt, SetStatement)
        assert stmt.variable == "total"
        assert stmt.value == "0"
        assert stmt.line_number == 1

    def test_set_statement_with_complex_value(self):
        """Test parsing SET statement with complex value"""
        code = "set result = total + count * 2"
        tokens = self.tokenizer.tokenize_text(code)
        ast = self.parser.parse(tokens)

        stmt = ast.statements[0]
        assert isinstance(stmt, SetStatement)
        assert stmt.variable == "result"
        assert stmt.value == "total + count * 2"
        assert stmt.line_number == 1

    def test_print_statement_parsing(self):
        """Test parsing PRINT statements"""
        code = 'print "Hello World"'
        tokens = self.tokenizer.tokenize_text(code)
        ast = self.parser.parse(tokens)

        stmt = ast.statements[0]
        assert isinstance(stmt, PrintStatement)
        assert stmt.message == '"Hello World"'
        assert stmt.line_number == 1

    def test_get_statement_parsing(self):
        """Test parsing GET statements"""
        code = "get user_input"
        tokens = self.tokenizer.tokenize_text(code)
        ast = self.parser.parse(tokens)

        stmt = ast.statements[0]
        assert isinstance(stmt, GetStatement)
        assert stmt.variable == "user_input"
        assert stmt.line_number == 1

    def test_do_statement_parsing(self):
        """Test parsing DO statements"""
        code = "do calculate_sum"
        tokens = self.tokenizer.tokenize_text(code)
        ast = self.parser.parse(tokens)

        stmt = ast.statements[0]
        assert isinstance(stmt, DoStatement)
        assert stmt.function_name == "calculate_sum"
        assert stmt.line_number == 1

    def test_if_statement_parsing(self):
        """Test parsing IF-ENDIF statements"""
        code = """
if x > 0
    print "Positive"
endif
"""
        tokens = self.tokenizer.tokenize_text(code)
        ast = self.parser.parse(tokens)

        stmt = ast.statements[0]
        assert isinstance(stmt, IfStatement)
        assert stmt.condition == "x > 0"
        assert stmt.else_block is None
        assert len(stmt.if_block.statements) == 1

        inner_stmt = stmt.if_block.statements[0]
        assert isinstance(inner_stmt, PrintStatement)
        assert inner_stmt.message == '"Positive"'
        assert inner_stmt.line_number == 2

    def test_if_else_statement_parsing(self):
        """Test parsing IF-ELSE-ENDIF statements"""
        code = """
if x > 0
    print "Positive"
else
    print "Not positive"
endif
"""
        tokens = self.tokenizer.tokenize_text(code)
        ast = self.parser.parse(tokens)

        stmt = ast.statements[0]
        assert isinstance(stmt, IfStatement)
        assert stmt.condition == "x > 0"
        assert stmt.else_block is not None
        assert len(stmt.if_block.statements) == 1
        assert len(stmt.else_block.statements) == 1

        if_stmt = stmt.if_block.statements[0]
        else_stmt = stmt.else_block.statements[0]
        assert isinstance(if_stmt, PrintStatement)
        assert isinstance(else_stmt, PrintStatement)
        assert if_stmt.message == '"Positive"'
        assert else_stmt.message == '"Not positive"'

    def test_for_statement_parsing(self):
        """Test parsing FOR-ENDFOR statements"""
        code = """
for i in range 1 to 10
    print i
endfor
"""
        tokens = self.tokenizer.tokenize_text(code)
        ast = self.parser.parse(tokens)

        stmt = ast.statements[0]
        assert isinstance(stmt, ForStatement)
        assert stmt.iterator == "i"
        assert stmt.iterable == "range 1 to 10"
        assert len(stmt.body.statements) == 1

        inner_stmt = stmt.body.statements[0]
        assert isinstance(inner_stmt, PrintStatement)
        assert inner_stmt.message == "i"

    def test_while_statement_parsing(self):
        """Test parsing WHILE-ENDWHILE statements"""
        code = """
while count < 10
    set count = count + 1
endwhile
"""
        tokens = self.tokenizer.tokenize_text(code)
        ast = self.parser.parse(tokens)

        stmt = ast.statements[0]
        assert isinstance(stmt, WhileStatement)
        assert stmt.condition == "count < 10"
        assert len(stmt.body.statements) == 1

        inner_stmt = stmt.body.statements[0]
        assert isinstance(inner_stmt, SetStatement)
        assert inner_stmt.variable == "count"
        assert inner_stmt.value == "count + 1"

    def test_nested_structures(self):
        """Test parsing nested control structures"""
        code = """
for i in range 1 to 10
    if i % 2 equals 0
        print "Even number"
    else
        print "Odd number"
    endif
endfor
"""
        tokens = self.tokenizer.tokenize_text(code)
        ast = self.parser.parse(tokens)

        for_stmt = ast.statements[0]
        assert isinstance(for_stmt, ForStatement)
        assert len(for_stmt.body.statements) == 1

        if_stmt = for_stmt.body.statements[0]
        assert isinstance(if_stmt, IfStatement)
        assert if_stmt.condition == "i % 2 equals 0"
        assert len(if_stmt.if_block.statements) == 1
        assert if_stmt.else_block is not None
        assert len(if_stmt.else_block.statements) == 1

    def test_multiple_statements(self):
        """Test parsing multiple statements in sequence"""
        code = """
set total = 0
set count = 5
print "Starting calculation"
get user_input
do process_data
"""
        tokens = self.tokenizer.tokenize_text(code)
        ast = self.parser.parse(tokens)

        assert len(ast.statements) == 5
        assert isinstance(ast.statements[0], SetStatement)
        assert isinstance(ast.statements[1], SetStatement)
        assert isinstance(ast.statements[2], PrintStatement)
        assert isinstance(ast.statements[3], GetStatement)
        assert isinstance(ast.statements[4], DoStatement)

    def test_generic_statement_parsing(self):
        """Test parsing generic statements that don't match specific keywords"""
        code = "return value"
        tokens = self.tokenizer.tokenize_text(code)
        ast = self.parser.parse(tokens)

        stmt = ast.statements[0]
        assert isinstance(stmt, GenericStatement)
        assert stmt.content == "return value"

    def test_invalid_set_statement(self):
        """Test error handling for invalid SET statement"""
        # Create a mock token that would cause parsing error
        token = Token(Type.SET, "set invalid", 1, 0)
        tokens = [token]

        with pytest.raises(ParseError) as exc_info:
            self.parser.parse(tokens)

        assert "Invalid SET statement format" in str(exc_info.value)
        assert exc_info.value.line_number == 1

    def test_missing_endif(self):
        """Test error handling for missing ENDIF"""
        code = """
if x > 0
    print "Positive"
"""
        tokens = self.tokenizer.tokenize_text(code)

        with pytest.raises(ParseError) as exc_info:
            self.parser.parse(tokens)

        assert "Expected ENDIF" in str(exc_info.value)

    def test_missing_endfor(self):
        """Test error handling for missing ENDFOR"""
        code = """
for i in range 1 to 10
    print i
"""
        tokens = self.tokenizer.tokenize_text(code)

        with pytest.raises(ParseError) as exc_info:
            self.parser.parse(tokens)

        assert "Expected ENDFOR" in str(exc_info.value)

    def test_missing_endwhile(self):
        """Test error handling for missing ENDWHILE"""
        code = """
while count < 10
    set count = count + 1
"""
        tokens = self.tokenizer.tokenize_text(code)

        with pytest.raises(ParseError) as exc_info:
            self.parser.parse(tokens)

        assert "Expected ENDWHILE" in str(exc_info.value)

    def test_invalid_for_statement(self):
        """Test error handling for invalid FOR statement format"""
        # Create a mock token with invalid FOR format
        token = Token(Type.FOR, "for invalid format", 1, 0)
        tokens = [token, Token(Type.ENDFOR, "endfor", 2, 0)]

        with pytest.raises(ParseError) as exc_info:
            self.parser.parse(tokens)

        assert "Invalid FOR statement format" in str(exc_info.value)

    def test_line_numbers_preserved(self):
        """Test that line numbers are correctly preserved in AST nodes"""
        code = """
set x = 1

print "Hello"

if x > 0
    get input
endif
"""
        tokens = self.tokenizer.tokenize_text(code)
        ast = self.parser.parse(tokens)

        # Check that line numbers are preserved
        assert ast.statements[0].line_number == 1  # set x = 1
        assert ast.statements[1].line_number == 3  # print "Hello"
        assert ast.statements[2].line_number == 5  # if x > 0

        # Cast to IfStatement to access if_block
        if_stmt = ast.statements[2]
        assert isinstance(if_stmt, IfStatement)
        assert if_stmt.if_block.statements[0].line_number == 6  # get input

    def test_complex_program(self):
        """Test parsing a complex program with multiple constructs"""
        code = """
set total = 0
set count = 0
for x in range 0 to 10
    if x % 2 equals 0
        set total = total + x
        set count = count + 1
    endif
endfor
print "Total: {total}"
print "Count: {count}"
"""
        tokens = self.tokenizer.tokenize_text(code)
        ast = self.parser.parse(tokens)

        # Verify overall structure
        assert len(ast.statements) == 5  # 2 sets, 1 for, 2 prints

        # Verify FOR loop structure
        for_stmt = ast.statements[2]
        assert isinstance(for_stmt, ForStatement)
        assert len(for_stmt.body.statements) == 1

        # Verify nested IF structure
        if_stmt = for_stmt.body.statements[0]
        assert isinstance(if_stmt, IfStatement)
        assert len(if_stmt.if_block.statements) == 2


class TestASTNodeClasses:
    """Test suite for AST node classes"""

    def test_set_statement_creation(self):
        """Test SetStatement node creation"""
        stmt = SetStatement(1, "variable", "value")
        assert stmt.line_number == 1
        assert stmt.variable == "variable"
        assert stmt.value == "value"

    def test_print_statement_creation(self):
        """Test PrintStatement node creation"""
        stmt = PrintStatement(2, "Hello World")
        assert stmt.line_number == 2
        assert stmt.message == "Hello World"

    def test_get_statement_creation(self):
        """Test GetStatement node creation"""
        stmt = GetStatement(3, "input_var")
        assert stmt.line_number == 3
        assert stmt.variable == "input_var"

    def test_do_statement_creation(self):
        """Test DoStatement node creation"""
        stmt = DoStatement(4, "function_name")
        assert stmt.line_number == 4
        assert stmt.function_name == "function_name"

    def test_if_statement_creation(self):
        """Test IfStatement node creation"""
        if_block = Block([])
        else_block = Block([])
        stmt = IfStatement(5, "x > 0", if_block, else_block)
        assert stmt.line_number == 5
        assert stmt.condition == "x > 0"
        assert stmt.if_block == if_block
        assert stmt.else_block == else_block

    def test_for_statement_creation(self):
        """Test ForStatement node creation"""
        body = Block([])
        stmt = ForStatement(6, "i", "range 1 to 10", body)
        assert stmt.line_number == 6
        assert stmt.iterator == "i"
        assert stmt.iterable == "range 1 to 10"
        assert stmt.body == body

    def test_while_statement_creation(self):
        """Test WhileStatement node creation"""
        body = Block([])
        stmt = WhileStatement(7, "count < 10", body)
        assert stmt.line_number == 7
        assert stmt.condition == "count < 10"
        assert stmt.body == body

    def test_generic_statement_creation(self):
        """Test GenericStatement node creation"""
        stmt = GenericStatement(8, "return value")
        assert stmt.line_number == 8
        assert stmt.content == "return value"

    def test_block_creation(self):
        """Test Block node creation"""
        statements = [SetStatement(1, "x", "1"), PrintStatement(2, "test")]
        block = Block(statements)
        assert len(block.statements) == 2
        assert block.statements == statements

    def test_program_creation(self):
        """Test Program node creation"""
        statements = [SetStatement(1, "x", "1"), PrintStatement(2, "test")]
        program = Program(statements)
        assert len(program.statements) == 2
        assert program.statements == statements


class TestParseError:
    """Test suite for ParseError exception"""

    def test_parse_error_with_line_number(self):
        """Test ParseError with line number"""
        error = ParseError("Test error", 5)
        assert error.message == "Test error"
        assert error.line_number == 5
        assert "Parse error at line 5: Test error" in str(error)

    def test_parse_error_without_line_number(self):
        """Test ParseError without line number"""
        error = ParseError("Test error")
        assert error.message == "Test error"
        assert error.line_number is None
        assert str(error) == "Test error"


if __name__ == "__main__":
    # Run tests if script is executed directly
    pytest.main([__file__])
