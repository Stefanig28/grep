import pytest
from grep.main import main

def test_correct_output():
    file_content = "abc123"
    pattern = ""
    result = main(file_content, pattern)
    assert result == file_content