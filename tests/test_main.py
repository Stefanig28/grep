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
    ],
)
def test_letter_in_line(tmp_path: pathlib.Path, content, expected):
    file_path = tmp_path / "test.txt"
    file_path.write_text(content)

    out = io.StringIO()
    main(input=file_path, grep="J", output=out)
    assert out.getvalue() == expected

@pytest.mark.parametrize(
    "files_content, grep, expected",
    [
        (
            {
                "file1.txt": "Nirvana\nPearl Jam\n",
                "subdir/file2.txt": "Before Nirvana\nAfter Nirvana\n"
            },
            "Nirvana",
            [
                "file1.txt:Nirvana",
                "subdir/file2.txt:Before Nirvana",
                "subdir/file2.txt:After Nirvana",
            ]
        ),
        (
            {
                "file1.txt": "Nirvana\nRock\n",
                "subdir/file2.txt": "Nothing here\n"
            },
            "Nirvana",
            [
                "file1.txt:Nirvana",
            ]
        ),
        (
            {
                "file1.txt": "Metallica\nPearl Jam\n",
                "subdir/file2.txt": "Foo Fighters\n"
            },
            "Nirvana",
            []
        ),
    ]
)
def test_recursive(tmp_path, files_content, grep, expected):
    for file_name, content in files_content.items():
        file_path = tmp_path / file_name
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")

    output = io.StringIO()
    main(input=tmp_path, grep=grep, recursive=True, output=output)

    result = output.getvalue().strip().split("\n") if output.getvalue().strip() else []
    expected = [f"{tmp_path}/{line}" for line in expected]

    assert result == expected

@pytest.mark.parametrize(
    "files_content, grep, invert, expected",
    [
        (
            {
                "file1.txt": "Nirvana\nPearl Jam\nRock\n",
                "subdir/file2.txt": "Before Nirvana\nMadonna\nMetallica\n",
                "subdir/deep/file3.txt": "Nirvana and Madonna\nIron Maiden\n",
            },
            "Nirvana",
            ["Madonna"],
            [
                "file1.txt:Nirvana",
                "subdir/file2.txt:Before Nirvana",
            ]
        ),
        (
            {
                "file1.txt": "Rock\nPearl Jam\nNirvana\n",
                "subdir/file2.txt": "Rock and Roll\nPearl Jam\n",
                "subdir/deep/file3.txt": "Rock forever\n",
            },
            "Rock",
            ["Pearl Jam"],
            [
                "file1.txt:Rock",
                "subdir/file2.txt:Rock and Roll",
                "subdir/deep/file3.txt:Rock forever",
            ]
        ),
        (
            {
                "file1.txt": "Metallica\nIron Maiden\n",
                "subdir/file2.txt": "Heavy Metal\nIron Works\n",
                "subdir/deep/file3.txt": "Black Metal\n",
            },
            "Metal",
            ["Iron"],
            [
                "file1.txt:Metallica",
                "subdir/file2.txt:Heavy Metal",
                "subdir/deep/file3.txt:Black Metal",
            ]
        ),
    ]
)
def test_invert(tmp_path, files_content, grep, invert, expected):
    for file_name, content in files_content.items():
        file_path = tmp_path / file_name
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")

    output = io.StringIO()
    main(input=tmp_path, grep=grep, recursive=True, invert=invert, output=output)

    result = output.getvalue().strip().split("\n") if output.getvalue().strip() else []
    expected = [f"{str(tmp_path / line.split(':')[0])}:{line.split(':')[1]}" for line in expected]

    assert result == expected
