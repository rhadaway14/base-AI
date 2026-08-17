from pathlib import Path


def test_env_file_is_not_tracked_policy_source() -> None:
    # This is a filesystem-level guard for local runs. CI also checks git tracking.
    assert Path(".env.example").exists()
    ignore = Path(".gitignore").read_text(encoding="utf-8")
    assert ".env" in ignore


def test_required_architecture_documents_exist() -> None:
    required = [
        "docs/product/project-brief.md",
        "docs/architecture/system-architecture.md",
        "docs/architecture/principles.md",
        "docs/security/security-model.md",
        "docs/implementation-plan.md",
        "docs/ai/session-handoff.md",
    ]
    assert all(Path(path).exists() for path in required)
