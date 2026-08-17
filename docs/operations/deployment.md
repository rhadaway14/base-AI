# Deployment

The starter includes only the shared Terraform network baseline. A new project must document its actual deployables, ingress, secrets, data services, autoscaling, and rollback before claiming production readiness.

## Required deployment properties

- immutable application artifacts;
- environment configuration external to source;
- secrets from a managed secret store;
- private application/data networking where appropriate;
- TLS for external and data-service traffic;
- health/readiness probes;
- centralized logs and metrics;
- repeatable infrastructure definition;
- rollback or forward-fix procedure;
- backup/restore procedure for persistent state.
