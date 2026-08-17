"""Provider SDKs must not leak into domain/API code.

The starter does not yet implement Bedrock. When a provider SDK is added, keep it behind
`app_llm`. This test protects that seam from convenient imports spreading outward.
"""
from pathlib import Path


FORBIDDEN_PROVIDER_IMPORTS = ("boto3", "botocore", "anthropic", "openai")
CHECK_ROOTS = (Path("apps/api"), Path("packages/domain-models"))


def test_provider_sdks_do_not_leak_across_the_boundary() -> None:
    offenders: list[str] = []
    for root in CHECK_ROOTS:
        for path in root.rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            leaked = any(
                f"import {name}" in text or f"from {name}" in text
                for name in FORBIDDEN_PROVIDER_IMPORTS
            )
            if leaked:
                offenders.append(str(path))
    assert not offenders, f"provider SDK leaked outside app_llm: {offenders}"
