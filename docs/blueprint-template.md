# Day 13 Observability Lab Report

> **Instruction**: Fill in all sections below. This report is designed to be parsed by an automated grading assistant. Ensure all tags (e.g., `[GROUP_NAME]`) are preserved.

## 1. Team Metadata
- [GROUP_NAME]: Individual Submission - Nguyễn Hải Quân
- [REPO_URL]: TBD
- [MEMBERS]:
  - Member A: Nguyễn Hải Quân | Student ID: 2A202600660 | Role: Full-stack Observability Implementation, Logging & PII, Tracing, SLO/Alerts, Load Test, Dashboard, Demo & Report

---

## 2. Group Performance (Auto-Verified)
- [VALIDATE_LOGS_FINAL_SCORE]: 100/100
- [TOTAL_TRACES_COUNT]: 40+ traces/spans visible in Langfuse Tracing view
- [PII_LEAKS_FOUND]: 0

---

## 3. Technical Evidence (Group)

### 3.1 Logging & Tracing
- [EVIDENCE_CORRELATION_ID_SCREENSHOT]: docs/evidence/json-logs-correlation-id.png
- [EVIDENCE_PII_REDACTION_SCREENSHOT]: docs/evidence/pii-redaction-log.png
- [EVIDENCE_TRACE_LIST_SCREENSHOT]: docs/evidence/langfuse-trace-list-10-traces.png
- [EVIDENCE_TRACE_WATERFALL_SCREENSHOT]: docs/evidence/langfuse-trace-waterfall.png
- [TRACE_WATERFALL_EXPLANATION]: The trace captures the `LabAgent.run` request flow, including sanitized input metadata, hashed user/session context, feature/model tags, token usage, and the generated response. The trace can be correlated back to JSON logs through the request timestamp and request/session context.

### 3.2 Dashboard & SLOs
- [DASHBOARD_6_PANELS_SCREENSHOT]: docs/evidence/dashboard-6-panels-metrics.png
- [DASHBOARD_SPEC]: docs/local-dashboard.md
- [SLO_TABLE]:
| SLI | Target | Window | Current Value |
|---|---:|---|---:|
| Latency P95 | < 3000ms | 28d | 150ms in local validation |
| Error Rate | < 2% | 28d | 0 observed errors in local validation |
| Cost Budget | < $2.5/day | 1d | Under budget in local validation |
| Quality Score Avg | >= 0.75 | 28d | 0.88 in local validation |

### 3.3 Alerts & Runbook
- [ALERT_RULES_SCREENSHOT]: docs/evidence/alert-rules-runbook.png
- [SAMPLE_RUNBOOK_LINK]: docs/alerts.md#1-high-latency-p95
- [ALERT_RULES_CONFIG]: config/alert_rules.yaml

---

## 4. Incident Response (Group)
- [SCENARIO_NAME]: rag_slow
- [SYMPTOMS_OBSERVED]: Latency panels should show elevated P95/P99 after enabling the `rag_slow` incident; affected requests can be inspected in Langfuse traces and correlated with JSON logs through request context.
- [ROOT_CAUSE_PROVED_BY]: `rag_slow` incident toggle in `/health` and trace/log evidence for slow requests. See Langfuse trace waterfall screenshot and JSON logs with `correlation_id`.
- [FIX_ACTION]: Disable the incident with `python scripts/inject_incident.py --scenario rag_slow --disable`; in production, investigate and optimize/fallback the slow retrieval path.
- [PREVENTIVE_MEASURE]: Keep latency P95 alert active, inspect RAG vs LLM spans during incidents, and add runbook steps for fallback retrieval/truncation.

---

## 5. Individual Contributions & Evidence

### Nguyễn Hải Quân - 2A202600660
- [TASKS_COMPLETED]: Implemented end-to-end observability for the lab as an individual submission: correlation ID middleware, structured JSON log enrichment, recursive PII scrubbing, Langfuse tracing with SDK v3 compatibility, local `/metrics` dashboard evidence, SLO/alert/runbook review, load testing, validation evidence, bonus audit logging for incident toggles, and this blueprint report.
- [EVIDENCE_LINK]: Local git commits/PR link TBD

---

## 6. Bonus Items (Optional)
- [BONUS_COST_OPTIMIZATION]: Not claimed yet.
- [BONUS_AUDIT_LOGS]: Incident enable/disable actions are written to `data/audit.jsonl` via `write_audit_event(...)`.
- [BONUS_CUSTOM_METRIC]: Local `/metrics` endpoint exposes traffic, latency percentiles, costs, tokens, errors, and quality proxy for dashboard evidence.
