from pathlib import Path
import sys
import io
import re


def main(
    *,
    input: Path,
    grep: str,
    recursive: bool = False,
    invert: bool = False,
    output: io.StringIO = sys.stdout,
) -> None:

    if input.is_file():
        lines = input.read_text().splitlines()

        if grep == "":
            output.write("\n".join(lines) + "\n")
        else:
            output.write(f"{"\n".join([line for line in lines if grep in line])}\n")
        
        output.flush()
        
    elif input.is_dir():
        if recursive:
            all_files = [
                f for f in input.rglob("*")
                if f.is_file() and not any(part in f.parts for part in ["tests", ".pytest_cache"])
            ]
        else:
            all_files = [f for f in input.iterdir() if f.is_file()]

        grep_regex = re.compile(grep) if grep else None

        for file in all_files:
            with file.open("r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    line = line.rstrip("\n")

                    match = re.search(grep_regex, line) if grep_regex else grep in line

                    if invert:
                        if any(word in line for word in invert):
                            continue

                    match = re.search(grep_regex, line) if grep_regex else grep in line

                    if match:
                        output.write(f"{file}:{line}\n")
                        output.flush()

    else:
        sys.exit(1)


def _cli() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", type=Path, nargs="?", default=Path("."))
    parser.add_argument("-g", "--grep", type=str, default="")
    parser.add_argument("-r", "--recursive", action="store_true")
    parser.add_argument("-v", "--invert", type=str, nargs="*", help="Palabras a excluir")

    args = parser.parse_args()
    main(
        input=args.filepath,
        grep=args.grep,
        recursive=args.recursive,
        invert=args.invert,
    )


if __name__ == "__main__":
    _cli()
