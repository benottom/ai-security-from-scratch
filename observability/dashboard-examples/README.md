# Dashboard Examples

This directory contains sample data and configurations for building observability dashboards to monitor the AI security control ledger.

## Contents

- **sample-events.jsonl**: 10 sample control ledger events in JSONL format, covering the full lifecycle of a request through the AI security pipeline.

## Dashboard Design

A production AI security dashboard should include the following panels:

### 1. Request Flow Overview
- Total requests per time window
- Breakdown by decision (allow/deny/require_approval)
- Trend over time

### 2. Security Events
- Injection attempts blocked
- Policy violations detected
- Secrets/PII found in output
- Tool calls denied

### 3. Risk Heatmap
- Heatmap of event types × severity
- Color-coded by frequency

### 4. Actor Activity
- Events per actor (context_firewall, policy_engine, tool_gateway, output_validator)
- Decision distribution per actor

### 5. Latency Metrics
- Processing time per pipeline stage
- P50, P95, P99 latencies

### 6. Top Attack Patterns
- Most common injection patterns
- Most targeted tools
- Most violated policies

## Integration

The control ledger JSONL format can be ingested by:
- **Grafana** + **Loki** for log aggregation and dashboarding
- **Elasticsearch** + **Kibana** for search and visualization
- **Datadog** for APM and log management
- **Splunk** for SIEM integration

## Sample Query (Grafana/Loki)

```
{job="ai-security-ledger"} | json | decision="deny" | line_format "{{.event_type}} by {{.actor}}: {{.target}}"
```

## Sample Query (Elasticsearch/Kibana)

```json
{
  "query": {
    "bool": {
      "must": [
        {"match": {"decision": "deny"}},
        {"range": {"timestamp": {"gte": "now-1h"}}}
      ]
    }
  }
}
```
