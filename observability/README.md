# Observability extension point

The Python package provides the application logging seam. Add Prometheus/Grafana configuration here only when the project has metrics worth operating.

At minimum consider request rate/error/latency, dependency latency, AI provider latency and failures, token/cost metrics where available, queue depth, background job outcomes, and data-path saturation.
