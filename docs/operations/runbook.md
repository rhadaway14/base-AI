# Operations Runbook

## Service health

Check `/healthz` for process liveness and `/readyz` for ability to serve required work.

## Common incident flow

1. Identify affected environment and user-visible symptom.
2. Check deployment/change history.
3. Check readiness by dependency.
4. Follow the correlation/run id through logs.
5. Check provider/database latency and error class.
6. Mitigate using a documented rollback, feature disable, or failover path.
7. Preserve evidence before destructive recovery steps.
8. Record cause, corrective action, and new regression/invariant test.

## Project-specific procedures

Add deploy, rollback, database restore, credential rotation, queue recovery, index rebuild, model fallback, and degraded-mode procedures as those capabilities are implemented.
