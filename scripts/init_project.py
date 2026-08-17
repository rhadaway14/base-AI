from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
METADATA = ROOT / ".project.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialize a new repository from the starter")
    parser.add_argument("--name", required=True, help="Human-readable project name")
    parser.add_argument(
        "--slug",
        required=True,
        help="lowercase kebab-case repository/project slug",
    )
    parser.add_argument("--description", required=True, help="one-sentence project description")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", args.slug):
        raise SystemExit("--slug must be lowercase kebab-case (example: matter-intelligence)")

    previous = json.loads(METADATA.read_text(encoding="utf-8"))
    replacements = {
        previous["name"]: args.name,
        previous["slug"]: args.slug,
        previous["description"]: args.description,
    }

    text_suffixes = {
        ".md", ".toml", ".yml", ".yaml", ".json", ".py", ".tf",
        ".example", ".mjs", ".tsx", ".ts", ".css",
    }
    explicit_names = {"Makefile", "Dockerfile", ".env.example", ".gitleaks.toml"}
    skip_parts = {".git", ".venv", "node_modules", ".next"}

    changed = 0
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in skip_parts for part in path.parts):
            continue
        if path.resolve() == Path(__file__).resolve():
            continue
        if path == METADATA or (
            path.suffix not in text_suffixes and path.name not in explicit_names
        ):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        updated = text
        for old, new in replacements.items():
            updated = updated.replace(old, new)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed += 1

    package = ROOT / "apps/web/package.json"
    if package.exists():
        data = json.loads(package.read_text(encoding="utf-8"))
        data["name"] = f"{args.slug}-web"
        package.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    pyproject = ROOT / "pyproject.toml"
    text = pyproject.read_text(encoding="utf-8")
    text = re.sub(r'^name = ".*?"$', f'name = "{args.slug}"', text, count=1, flags=re.MULTILINE)
    safe_description = args.description.replace(chr(34), chr(39))
    text = re.sub(
        r'^description = ".*?"$',
        f'description = "{safe_description}"',
        text,
        count=1,
        flags=re.MULTILINE,
    )
    pyproject.write_text(text, encoding="utf-8")

    metadata = {"name": args.name, "slug": args.slug, "description": args.description}
    METADATA.write_text(
        json.dumps(metadata, indent=2) + "\n",
        encoding="utf-8",
    )

    handoff = ROOT / "docs/ai/session-handoff.md"
    handoff_text = f"""# Session Handoff

## Current objective

Define and build {args.name}.

## Current state

Repository initialized from the reusable starter template. Product and architecture
details still need to be completed.

## Verified

Run `make install`, `make check`, and `make web-check`; record actual results here.

## Next concrete step

Complete `docs/product/project-brief.md`, then amend or supersede `ADR-001`.
"""
    handoff.write_text(handoff_text, encoding="utf-8")

    print(f"Initialized {args.name} ({args.slug}); updated {changed} files.")
    print("Next: complete docs/product/project-brief.md, then run make install && make check.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
