"""
test_tokenizer.py

Pytest unit tests for the pseudocode tokenizer.
These tests exercise basic token recognition, indentation calculation,
and error handling for file tokenization.

Author: Phasin Noomkan(Nine)  
Date: 03/10/2025
"""



import os
import sys

# Ensure `src` is on sys.path so tests can import the tokenizer module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from tokenizer import PseudocodeTokenizer, Type
import pytest

def test_basic_tokenization():
    """Token types should be identified in order for a simple snippet."""

    sample_code = """
set total = 0
for x in range 0 to 10
    if x/2 equals 0
        set total = total + x
    endif
endfor
print "Total of even numbers from 0 to 10: {total}
"""

    tokenizer = PseudocodeTokenizer()
    tokens = tokenizer.tokenize_text(sample_code)

    expected_types = [
        Type.SET,
        Type.FOR,
        Type.IF,
        Type.SET,
        Type.ENDIF,
        Type.ENDFOR,
        Type.PRINT,
    ]

    assert [t.type for t in tokens] == expected_types



def test_tokenize_file_not_found(tmp_path):
    """tokenize_file should raise FileNotFoundError for missing files."""
    tokenizer = PseudocodeTokenizer()
    missing = tmp_path / "no_such_file.psc"

    with pytest.raises(FileNotFoundError):
        tokenizer.tokenize_file(str(missing))


def test_tokenize_file_invalid_extension(tmp_path):
    """tokenize_file should raise ValueError for non-.psc files."""
    tokenizer = PseudocodeTokenizer()
    
    # Create a file with wrong extension
    invalid_file = tmp_path / "test_file.txt"
    invalid_file.write_text("set x = 1")

    with pytest.raises(ValueError, match="Invalid file type.*Only '.psc' files are allowed"):
        tokenizer.tokenize_file(str(invalid_file))


def test_other_token_types():
    """Ensure WHILE, REPEATWHILE, GET, DO and generic STATEMENT are recognized."""
    sample_code = """
while x < 5
    get user_input
    do perform action
    total = total + 1
endwhile
"""

    tokenizer = PseudocodeTokenizer()
    tokens = tokenizer.tokenize_text(sample_code)

    expected_types = [
        Type.WHILE,
        Type.GET,
        Type.DO,
        Type.STATEMENT,
        Type.ENDWHILE,
    ]

    assert [t.type for t in tokens] == expected_types


def test_tokenize_file_reads_attachment():
    """Read pseudocode from the provided test.txt file and tokenize it."""
    

    file_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'test.psc'))

    tokenizer = PseudocodeTokenizer()
    tokens = tokenizer.tokenize_file(file_path)

    expected_types = [
        Type.SET,
        Type.FOR,
        Type.IF,
        Type.SET,
        Type.ENDIF,
        Type.ENDFOR,
        Type.PRINT,
    ]

    assert [t.type for t in tokens] == expected_types
