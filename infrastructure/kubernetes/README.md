# Optional Kubernetes deployment

Do not add Kubernetes manifests just because the template has a directory for them. Use Kubernetes only when the project has a reason to own cluster scheduling/operations rather than a simpler managed container runtime.

If selected, keep Helm charts here and add CI that runs `helm lint` plus schema/render validation. Record the deployment choice in an ADR.
