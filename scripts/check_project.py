from __future__ import annotations

import subprocess
from pathlib import Path

REQUIRED = [
    "AGENTS.md",
    "CLAUDE.md",
    ".env.example",
    "docs/product/project-brief.md",
    "docs/architecture/system-architecture.md",
    "docs/security/security-model.md",
    "docs/ai/session-handoff.md",
]


def main() -> int:
    missing = [path for path in REQUIRED if not Path(path).exists()]
    if missing:
        print("Missing required project files:", *missing, sep="\n  - ")
        return 1

    if Path(".env").exists():
        try:
            tracked = subprocess.run(
                ["git", "ls-files", "--error-unmatch", ".env"],  # noqa: S603,S607
                capture_output=True,
                check=False,
                text=True,
            ).returncode == 0
        except FileNotFoundError:
            tracked = False
        if tracked:
            print("ERROR: .env is tracked by git")
            return 1

    print("Repository policy checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
