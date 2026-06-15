# Local/Simple Dashboard Evidence

Use this lightweight dashboard plan when the lab environment does not provide Grafana or Prometheus. The source of truth is the FastAPI `/metrics` endpoint.

## Data source

Start the app:

```bash
uvicorn app.main:app --reload
```

Generate traffic:

```bash
python scripts/load_test.py --concurrency 5
```

Open or refresh:

```text
http://127.0.0.1:8000/metrics
```

## Required 6 panels

| Panel | Metric fields from `/metrics` | Unit | Suggested SLO/threshold |
|---|---|---|---|
| Latency P50/P95/P99 | `latency_p50`, `latency_p95`, `latency_p99` | ms | P95 < 3000 ms |
| Traffic | `traffic` | requests | should increase during load test |
| Error rate/breakdown | `error_breakdown` | count by error type | error rate < 2% |
| Cost over time | `avg_cost_usd`, `total_cost_usd` | USD | daily budget < $2.50 |
| Tokens in/out | `tokens_in_total`, `tokens_out_total` | tokens | watch for cost spikes |
| Quality proxy | `quality_avg` | score 0-1 | average >= 0.75 |

## Screenshot checklist

Capture one screenshot that shows all 6 panels/values, or one screenshot of `/metrics` plus a rendered table using the fields above. Add the screenshot path to `docs/blueprint-template.md` under `[DASHBOARD_6_PANELS_SCREENSHOT]`.

Recommended evidence filename:

```text
docs/evidence/dashboard-6-panels.png
```

## Incident demo flow

For `rag_slow`:

1. Run baseline load test and screenshot `/metrics`.
2. Enable incident:

   ```bash
   python scripts/inject_incident.py --scenario rag_slow
   ```

3. Run load test again.
4. Observe increased `latency_p95`/`latency_p99`.
5. Use Langfuse trace waterfall + JSON logs with matching `correlation_id` to prove root cause.
6. Disable incident:

   ```bash
   python scripts/inject_incident.py --scenario rag_slow --disable
   ```

Audit records for incident toggles are written to `data/audit.jsonl`.
