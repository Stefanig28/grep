from pathlib import Path
import sys
import io
import re

def main(*, input: Path, grep: str, recursive: bool = False, invert: bool = False, output: io.StringIO = sys.stdout) -> None:
    if not input.exists():
        sys.exit(1)

    all_files = []
    if input.is_file():
        all_files = [input]
    elif input.is_dir() and recursive:
        all_files = [f for f in input.rglob("*") if f.is_file()]
    else:
        sys.exit(1)

    grep_pattern = grep
    if "\\d" in grep or "\\w" in grep:
        grep_pattern = grep.replace("\\d", r"\d").replace("\\w", r"\w")
        grep_regex = re.compile(grep_pattern)
    else:
        grep_regex = None

    found_match = False
    for file in all_files:
        try:
            with file.open("r", encoding="utf-8", errors="replace") as f: 
                for line in f:
                    line = line.rstrip("\n")
                    
                    match = (
                        re.search(grep_regex, line) if grep_regex else grep in line
                    )

                    if invert:
                        match = not match

                    if match:
                        output.write(f"{line}\n")
                        output.flush()
                        found_match = True
        except Exception as e:
            sys.stderr.write(f"Error al leer {file}: {e}\n")

    output.flush()
    sys.exit(0 if found_match else 1)

def _cli() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", type=Path)
    parser.add_argument("-g", "--grep", type=str, default="")
    parser.add_argument("-r", "--recursive", action="store_true")
    parser.add_argument("-v", "--invert", action="store_true")

    args = parser.parse_args()
    main(input=args.filepath, grep=args.grep, recursive=args.recursive, invert=args.invert)

if __name__ == "__main__":
    _cli()
