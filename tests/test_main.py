import pytest
import pathlib
import io
from grep.main import main


@pytest.mark.parametrize(
        "content, expected",
        [
        ("abc123", "abc123\n"),
        ("", "\n"),
        ("line1\nline2\nline3", "line1\nline2\nline3\n"),
        ],
)
def test_main(tmp_path: pathlib.Path, content, expected):
    file_path = tmp_path / "test.txt"
    file_path.write_text(content)

    out = io.StringIO()
    main(input=file_path, grep="", output=out)

    assert out.getvalue() == expected

@pytest.mark.parametrize(
    "content, expected",
    [
        ("Judas Priest\nBon Jovi\nJunkyard", "Judas Priest\nBon Jovi\nJunkyard\n"),
        ("Ja\nJo\nJoker\nApple", "Ja\nJo\nJoker\n"),
    ]
)
def test_letter_in_line(tmp_path: pathlib.Path, content, expected):
    file_path = tmp_path / "test.txt"
    file_path.write_text(content)

    out = io.StringIO()
    main(input=file_path, grep="J", output=out)
    assert out.getvalue() == expected