"""One-off script to write exit ticket response grid files."""
from pathlib import Path

BASE = Path(r"c:/Users/chase/Documents/Programs/School Scrips/Macro App/renderer/src")

FILES: dict[str, str] = {}


def main() -> None:
    for rel, content in FILES.items():
        path = BASE / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"wrote {rel}")


if __name__ == "__main__":
    main()
