# ray-example

A minimal Ray Serve LLM application, used as a `runtime_env.working_dir`
example.

`demo_app.py` exposes `build_app`, an application builder: Ray hands it the
application's `args` as a single mapping and expects an `Application` back.
It delegates to `ray.serve.llm.build_openai_app`, so the result serves the
OpenAI-compatible routes.

## Use it as a working_dir

Ray fetches a `working_dir` archive inside the cluster, so any https URL to a
`.zip`, `.tar.gz` or `.tgz` works. GitHub publishes one per commit:

```
https://github.com/aylei/ray-example/archive/<commit-sha>.zip
```

Pin a commit rather than a branch — a branch URL changes under a running
deployment.

## Ray Serve config

```yaml
applications:
  - name: llm
    route_prefix: /
    import_path: demo_app:build_app
    runtime_env:
      working_dir: https://github.com/aylei/ray-example/archive/<commit-sha>.zip
    args:
      llm_configs:
        - model_loading_config:
            model_id: Qwen/Qwen2.5-3B-Instruct
            model_source: Qwen/Qwen2.5-3B-Instruct
          deployment_config:
            autoscaling_config:
              min_replicas: 1
              max_replicas: 1
          engine_kwargs:
            max_model_len: 8192
            gpu_memory_utilization: 0.85
          log_engine_metrics: true
```

`import_path: ray.serve.llm:build_openai_app` works the same way and needs no
code from this repository — the `args` above are what it takes.

Set `log_engine_metrics: true` to have the engine's vLLM gauges exported;
Prometheus scrapers and autoscalers generally match on those names.
