from pathlib import Path


def main(file_content: str, pattern: str) -> str:
    if pattern == "":
        return file_content


def _cli() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", type=Path)
    parser.add_argument("-g", dest="grep", type=str, default="")
    args = parser.parse_args()

    content = args.filepath.read_text(encoding="utf-8")
    result = main(content, args.grep)
    print(result, end="")


if __name__ == "__main__":
    _cli()