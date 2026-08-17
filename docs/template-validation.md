# Template Validation Record

**Validation date:** 2026-08-17

## Verified in the build environment

- Repository structure and required project-policy files exist.
- `scripts/init_project.py` was executed against a copy of the template and correctly renamed a sample project.
- Python source compiles with Python 3.13.
- Unit and architecture invariant tests passed: **9 passed**.
- `scripts/check_project.py` passed.
- Python source was checked for lines over the configured 100-character Ruff limit.

## Not executable in the build environment

The artifact-building sandbox has no outbound package registry access, so it could not freshly install/resolve PyPI or npm packages. Terraform is also not installed in the sandbox. Therefore these commands still need to be run once in a normal development environment before this repository is promoted as the permanent organization template:

```bash
make install
make check
make web-check
terraform fmt -check -recursive infrastructure/terraform
terraform -chdir=infrastructure/terraform/environments/dev init -backend=false
terraform -chdir=infrastructure/terraform/environments/dev validate
docker compose build
make up
make test-e2e
```

After the first successful `make install`, commit the generated `uv.lock` and change CI/container installs to `uv sync --frozen` for fully reproducible Python dependency resolution.

This limitation is about **validation of third-party dependency installation**, not the source-level tests listed above.
