# Pattern: AI Circuit Breaker

> **Pattern ID:** PAT-CB-001 | **Category:** Resilience | **Maturity:** Proven

---

## Problem

AI systems can enter runaway states — generating harmful content at volume, executing tool calls in loops, consuming excessive resources, or responding to attacks in ways that amplify rather than contain them. Without a mechanism to detect and halt these runaway behaviors, a single incident can cascade: one successful prompt injection triggers a chain of tool calls, each of which creates more context that feeds further unwanted behavior, spiraling until human intervention or system failure stops it.

The root cause is a missing supervisory control: the system has no kill switch or breaker mechanism that can interrupt the control loop when it enters an unsafe state. The loop runs open, with no observer checking whether the system's aggregate behavior has crossed from normal operation into runaway.

**Concrete failure scenario:** A prompt injection attack causes an AI agent to enter a loop: it calls the email-sending tool repeatedly, each time including more of the injected payload in the email body. Over 30 minutes, the agent sends 2,000 emails before a human notices and manually shuts down the service. There was no circuit breaker to detect the anomalous tool call volume and halt execution.

---

## Threat Model

| Attribute | Value |
|---|---|
| **Threat ID** | T-CB-001 |
| **Threat Name** | Runaway AI behavior without automatic containment |
| **Attack Vector** | Prompt injection, model error, or feedback loop causing escalating unwanted behavior |
| **Impact** | Resource exhaustion, mass harmful output, cascading tool calls, reputational damage, service outage |
| **Likelihood** | Medium — requires a trigger, but runaway dynamics are inherent to autonomous systems |
| **Risk** | High |
| **OWASP LLM Top 10** | LLM04: Model Denial of Service, LLM08: Excessive Agency |
| **NIST AI RMF** | MANAGE 2.2, MANAGE 2.3 |

**Attack variants:**
1. **Tool call loops:** Agent calls the same tool repeatedly in an escalating pattern
2. **Output amplification:** Each model response contains more harmful content than the last
3. **Resource exhaustion:** Agent generates extremely long outputs or makes many concurrent requests
4. **Feedback loop:** Agent's own output feeds back as input, creating self-reinforcing behavior
5. **Denial of service via legitimate-seeming volume:** Attacker triggers high-volume but individually legitimate-seeming interactions that collectively overwhelm the system

---

## Control-Theoretic View

### Objective

Detect when the AI system enters a runaway or degraded state and automatically halt or degrade its operation to prevent harm, with defined recovery procedures for returning to normal operation.

### Controller

The **AI Circuit Breaker** — a supervisory control that monitors aggregate system behavior against safety thresholds and can trip (open the circuit) to halt processing when thresholds are exceeded, with configurable half-open states for testing recovery.

### Observations

| Observation | Source | Type |
|---|---|---|
| Tool call rate (per user, per tool, global) | Tool gateway / API | Continuous |
| Output generation rate | Model inference pipeline | Continuous |
| Error rate (model errors, tool errors, policy violations) | All components | Continuous |
| Resource utilization (CPU, memory, tokens) | Infrastructure metrics | Continuous |
| Anomaly score (composite) | Anomaly detection engine | Continuous |
| Latency trends | API gateway | Continuous |

### Actions

| Action | Effect | Preconditions |
|---|---|---|
| Allow (closed circuit) | Normal processing | All thresholds within bounds |
| Trip (open circuit) | All processing halted; safe error returned | Any critical threshold exceeded |
| Half-open (probe) | Limited requests allowed to test recovery | Cool-down period elapsed after trip |
| Graceful degradation | Non-essential features disabled; rate limits tightened | Warning thresholds exceeded |
| Force close (manual reset) | Resume normal processing after human verification | Human confirms safe state |

### Feedback

- Trip events are logged and analyzed for root cause
- Half-open probe results determine whether the system can safely return to closed state
- Trip frequency drives threshold tuning and system hardening

### Disturbances

| Disturbance | Source | Mitigation |
|---|---|---|
| Legitimate traffic spikes | Marketing event, viral content | Per-user thresholds separate from global thresholds |
| Threshold miscalibration | Operational misconfiguration | Gradual threshold adjustment; anomaly-based detection |
| Distributed attacks | Multiple attacker sources | Global thresholds; aggregate anomaly detection |
| Cascading trips | One tripped breaker causes load on another | Circuit breaker coordination; load shedding |
| False trips | Anomaly detector too sensitive | Confidence thresholds; multi-signal confirmation |

### Unsafe States

| Unsafe State | Condition | Consequence |
|---|---|---|
| Runaway execution | No breaker; system operates indefinitely in degraded state | Mass harmful output; resource exhaustion |
| Stuck open | Breaker trips and never recovers | Permanent service outage |
| Flapping | Breaker rapidly trips and recovers | Unstable service; user frustration |
| Breaker bypassed | Processing continues despite tripped breaker | Same as no breaker |
| Breaker disabled | Configuration or code change removes breaker | No protection against runaway |

---

## Architecture

```
                    ┌────────────────────────────────┐
                    │      AI System (Under Control)   │
                    │                                  │
                    │  ┌──────┐  ┌──────┐  ┌──────┐  │
                    │  │ LLM  │  │ Tools │  │ RAG  │  │
                    │  └──┬───┘  └──┬───┘  └──┬───┘  │
                    └─────┼─────────┼─────────┼──────┘
                          │         │         │
                          ▼         ▼         ▼
┌──────────────────────────────────────────────────────────────┐
│                     AI Circuit Breaker                         │
│                                                              │
│  ┌──────────────────────────────────────────────────────────┐│
│  │  State Machine                                           ││
│  │                                                          ││
│  │   CLOSED ──(threshold exceeded)──▶ OPEN                  ││
│  │     ▲                               │                    ││
│  │     │                        (cool-down elapsed)          ││
│  │     │                               ▼                    ││
│  │     │         ◀──(probe succeeds)── HALF_OPEN            ││
│  │     │                               │                    ││
│  │     │                    (probe fails)                    ││
│  │     │                               ▼                    ││
│  │     │                            OPEN (re-tripped)       ││
│  └──────────────────────────────────────────────────────────┘│
│  ┌──────────────────────────────────────────────────────────┐│
│  │  Threshold Monitors                                      ││
│  │  • Tool call rate           • Error rate                 ││
│  │  • Output volume            • Policy violation rate      ││
│  │  • Resource utilization     • Anomaly score              ││
│  │  • Latency percentiles      • Concurrent request count   ││
│  └──────────────────────────────────────────────────────────┘│
│  ┌──────────────────────────────────────────────────────────┐│
│  │  Graceful Degradation Profiles                           ││
│  │  Level 1: Rate limit tightened                           ││
│  │  Level 2: Non-essential tools disabled                   ││
│  │  Level 3: Read-only mode (no tool calls)                 ││
│  │  Level 4: Full stop (circuit open)                       ││
│  └──────────────────────────────────────────────────────────┘│
│  ┌──────────────────────────────────────────────────────────┐│
│  │  Recovery Procedures                                     ││
│  │  • Cool-down period (configurable)                       ││
│  │  • Half-open probe (limited test traffic)                ││
│  │  • Gradual ramp-up (increase traffic gradually)          ││
│  │  • Manual reset (human verification required)            ││
│  └──────────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────────┘
```

---

## Implementation

```python
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Callable
from datetime import datetime, timedelta
import time


class CircuitState(Enum):
    CLOSED = "closed"          # Normal operation
    OPEN = "open"              # All processing halted
    HALF_OPEN = "half_open"    # Probing for recovery


class DegradationLevel(Enum):
    NORMAL = 0          # Full functionality
    RATE_LIMITED = 1    # Tightened rate limits
    ESSENTIAL_ONLY = 2  # Only essential tools available
    READ_ONLY = 3       # No tool calls; inference only
    FULL_STOP = 4       # Circuit open; no processing


@dataclass
class ThresholdConfig:
    """Thresholds for circuit breaker tripping."""
    # Per-user thresholds
    tool_calls_per_minute: int = 30
    outputs_per_minute: int = 60
    policy_violations_per_hour: int = 5

    # Global thresholds
    global_tool_calls_per_minute: int = 500
    global_error_rate_percent: float = 10.0
    global_concurrent_requests: int = 1000

    # Anomaly thresholds
    anomaly_score_critical: float = 0.9
    anomaly_score_warning: float = 0.7

    # Circuit breaker timing
    cool_down_seconds: int = 60          # Time before half-open probe
    half_open_max_probes: int = 3        # Probes allowed in half-open
    half_open_success_threshold: int = 2  # Successes needed to close


@dataclass
class MetricSnapshot:
    """Current values of monitored metrics."""
    tool_calls_last_minute: int = 0
    outputs_last_minute: int = 0
    policy_violations_last_hour: int = 0
    error_rate_percent: float = 0.0
    concurrent_requests: int = 0
    anomaly_score: float = 0.0
    global_tool_calls_last_minute: int = 0
    timestamp: float = field(default_factory=time.time)


@dataclass
class CircuitBreakerEvent:
    """Record of a circuit breaker state transition."""
    from_state: str
    to_state: str
    reason: str
    degradation_level: int
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class AICircuitBreaker:
    """Detects and stops runaway AI behavior.

    Control objective: The system does not operate indefinitely in
    a runaway or degraded state; automatic containment is triggered.
    """

    def __init__(
        self,
        thresholds: Optional[ThresholdConfig] = None,
        audit_logger: Optional[Callable] = None,
        on_trip: Optional[Callable] = None,
        on_recovery: Optional[Callable] = None,
    ):
        self.thresholds = thresholds or ThresholdConfig()
        self.audit_logger = audit_logger
        self.on_trip = on_trip
        self.on_recovery = on_recovery

        self._state = CircuitState.CLOSED
        self._degradation_level = DegradationLevel.NORMAL
        self._trip_time: Optional[float] = None
        self._half_open_probes_sent = 0
        self._half_open_successes = 0
        self._events: list[CircuitBreakerEvent] = []
        self._user_metrics: dict[str, MetricSnapshot] = {}
        self._global_metrics = MetricSnapshot()

    @property
    def state(self) -> CircuitState:
        return self._state

    @property
    def degradation_level(self) -> DegradationLevel:
        return self._degradation_level

    def check(self, user_id: Optional[str] = None) -> tuple[CircuitState, DegradationLevel, str]:
        """Check whether the circuit allows processing.

        Returns (state, degradation_level, reason).
        """
        # If circuit is open, check if cool-down has elapsed
        if self._state == CircuitState.OPEN:
            if self._trip_time and time.time() - self._trip_time >= self.thresholds.cool_down_seconds:
                self._transition(CircuitState.HALF_OPEN, "Cool-down period elapsed; entering half-open probe")
                return self._state, self._degradation_level, "Half-open: probing for recovery"
            return self._state, self._degradation_level, "Circuit is open; processing halted"

        # Evaluate metrics against thresholds
        reason = self._evaluate_thresholds(user_id)
        if reason:
            self._trip(reason)
            return self._state, self._degradation_level, reason

        return self._state, self._degradation_level, "Circuit is closed; processing allowed"

    def record_success(self):
        """Record a successful operation (for half-open recovery)."""
        if self._state == CircuitState.HALF_OPEN:
            self._half_open_successes += 1
            if self._half_open_successes >= self.thresholds.half_open_success_threshold:
                self._transition(CircuitState.CLOSED, "Half-open probe succeeded; closing circuit")
                self._degradation_level = DegradationLevel.NORMAL
                if self.on_recovery:
                    self.on_recovery()

    def record_failure(self):
        """Record a failed operation (for half-open re-trip)."""
        if self._state == CircuitState.HALF_OPEN:
            self._transition(CircuitState.OPEN, "Half-open probe failed; re-tripping circuit")
            self._trip_time = time.time()

    def update_metrics(self, snapshot: MetricSnapshot, user_id: Optional[str] = None):
        """Update the monitored metrics."""
        if user_id:
            self._user_metrics[user_id] = snapshot
        self._global_metrics = snapshot

    def force_reset(self, operator_id: str, reason: str):
        """Manually reset the circuit breaker (requires human authorization)."""
        self._transition(CircuitState.CLOSED, f"Manual reset by {operator_id}: {reason}")
        self._degradation_level = DegradationLevel.NORMAL
        self._half_open_probes_sent = 0
        self._half_open_successes = 0

    def get_events(self) -> list[CircuitBreakerEvent]:
        """Get the history of circuit breaker state transitions."""
        return list(self._events)

    def _evaluate_thresholds(self, user_id: Optional[str]) -> Optional[str]:
        """Evaluate all thresholds and return a reason if any is exceeded."""
        global_m = self._global_metrics

        # Global checks
        if global_m.global_tool_calls_last_minute > self.thresholds.global_tool_calls_per_minute:
            return f"Global tool call rate exceeded: {global_m.global_tool_calls_last_minute}/{self.thresholds.global_tool_calls_per_minute}/min"

        if global_m.error_rate_percent > self.thresholds.global_error_rate_percent:
            return f"Global error rate exceeded: {global_m.error_rate_percent:.1f}%"

        if global_m.concurrent_requests > self.thresholds.global_concurrent_requests:
            return f"Global concurrent requests exceeded: {global_m.concurrent_requests}"

        if global_m.anomaly_score >= self.thresholds.anomaly_score_critical:
            return f"Critical anomaly score: {global_m.anomaly_score:.2f}"

        # Apply graceful degradation for warning-level anomalies
        if global_m.anomaly_score >= self.thresholds.anomaly_score_warning:
            if self._degradation_level.value < DegradationLevel.RATE_LIMITED.value:
                self._degradation_level = DegradationLevel.RATE_LIMITED

        # Per-user checks
        if user_id and user_id in self._user_metrics:
            user_m = self._user_metrics[user_id]
            if user_m.tool_calls_last_minute > self.thresholds.tool_calls_per_minute:
                return f"User {user_id} tool call rate exceeded: {user_m.tool_calls_last_minute}/{self.thresholds.tool_calls_per_minute}/min"

            if user_m.outputs_last_minute > self.thresholds.outputs_per_minute:
                return f"User {user_id} output rate exceeded: {user_m.outputs_last_minute}/{self.thresholds.outputs_per_minute}/min"

            if user_m.policy_violations_last_hour > self.thresholds.policy_violations_per_hour:
                return f"User {user_id} policy violation rate exceeded: {user_m.policy_violations_last_hour}/{self.thresholds.policy_violations_per_hour}/hr"

        return None

    def _trip(self, reason: str):
        """Trip the circuit breaker open."""
        previous_state = self._state
        self._state = CircuitState.OPEN
        self._trip_time = time.time()
        self._degradation_level = DegradationLevel.FULL_STOP
        self._half_open_probes_sent = 0
        self._half_open_successes = 0

        self._events.append(CircuitBreakerEvent(
            from_state=previous_state.value,
            to_state=CircuitState.OPEN.value,
            reason=reason,
            degradation_level=self._degradation_level.value,
        ))

        if self.audit_logger:
            self.audit_logger(
                event="circuit_breaker_trip",
                reason=reason,
                timestamp=datetime.utcnow().isoformat(),
            )

        if self.on_trip:
            self.on_trip(reason)

    def _transition(self, new_state: CircuitState, reason: str):
        """Transition the circuit breaker to a new state."""
        previous_state = self._state
        self._state = new_state

        self._events.append(CircuitBreakerEvent(
            from_state=previous_state.value,
            to_state=new_state.value,
            reason=reason,
            degradation_level=self._degradation_level.value,
        ))

        if self.audit_logger:
            self.audit_logger(
                event=f"circuit_breaker_transition_{previous_state.value}_to_{new_state.value}",
                reason=reason,
                timestamp=datetime.utcnow().isoformat(),
            )
```

---

## Tests

```python
import pytest
from ai_circuit_breaker import (
    AICircuitBreaker, ThresholdConfig, MetricSnapshot, CircuitState, DegradationLevel
)


class TestAICircuitBreaker:
    """Security regression tests for the AI Circuit Breaker."""

    @pytest.fixture
    def breaker(self):
        return AICircuitBreaker(
            thresholds=ThresholdConfig(
                tool_calls_per_minute=30,
                global_tool_calls_per_minute=500,
                global_error_rate_percent=10.0,
                anomaly_score_critical=0.9,
                anomaly_score_warning=0.7,
                cool_down_seconds=0,  # Immediate for testing
                half_open_success_threshold=2,
            ),
        )

    def test_normal_operation_circuit_closed(self, breaker):
        state, level, reason = breaker.check(user_id="user-1")
        assert state == CircuitState.CLOSED
        assert level == DegradationLevel.NORMAL

    def test_global_tool_rate_trips_breaker(self, breaker):
        breaker.update_metrics(MetricSnapshot(global_tool_calls_last_minute=600))
        state, level, reason = breaker.check()
        assert state == CircuitState.OPEN
        assert level == DegradationLevel.FULL_STOP

    def test_user_tool_rate_trips_breaker(self, breaker):
        breaker.update_metrics(MetricSnapshot(tool_calls_last_minute=35), user_id="user-1")
        state, level, reason = breaker.check(user_id="user-1")
        assert state == CircuitState.OPEN

    def test_error_rate_trips_breaker(self, breaker):
        breaker.update_metrics(MetricSnapshot(error_rate_percent=15.0))
        state, level, reason = breaker.check()
        assert state == CircuitState.OPEN

    def test_anomaly_score_trips_breaker(self, breaker):
        breaker.update_metrics(MetricSnapshot(anomaly_score=0.95))
        state, level, reason = breaker.check()
        assert state == CircuitState.OPEN

    def test_warning_anomaly_triggers_degradation(self, breaker):
        breaker.update_metrics(MetricSnapshot(anomaly_score=0.75))
        state, level, reason = breaker.check()
        assert state == CircuitState.CLOSED
        assert level == DegradationLevel.RATE_LIMITED

    def test_half_open_recovery_on_success(self, breaker):
        # Trip the breaker
        breaker.update_metrics(MetricSnapshot(anomaly_score=0.95))
        breaker.check()

        # Cool-down is 0 for testing, so next check enters half-open
        breaker.update_metrics(MetricSnapshot(anomaly_score=0.1))
        breaker.check()
        assert breaker.state == CircuitState.HALF_OPEN

        # Succeed enough probes to close
        breaker.record_success()
        breaker.record_success()
        assert breaker.state == CircuitState.CLOSED

    def test_half_open_retrip_on_failure(self, breaker):
        breaker.update_metrics(MetricSnapshot(anomaly_score=0.95))
        breaker.check()
        breaker.update_metrics(MetricSnapshot(anomaly_score=0.1))
        breaker.check()  # Half-open

        breaker.record_failure()
        assert breaker.state == CircuitState.OPEN

    def test_manual_reset(self, breaker):
        breaker.update_metrics(MetricSnapshot(anomaly_score=0.95))
        breaker.check()
        assert breaker.state == CircuitState.OPEN

        breaker.force_reset("admin-1", "Root cause identified and fixed")
        assert breaker.state == CircuitState.CLOSED

    def test_policy_violation_rate_trips_breaker(self, breaker):
        breaker.update_metrics(MetricSnapshot(policy_violations_last_hour=10), user_id="user-1")
        state, level, reason = breaker.check(user_id="user-1")
        assert state == CircuitState.OPEN

    def test_event_history_recorded(self, breaker):
        breaker.update_metrics(MetricSnapshot(anomaly_score=0.95))
        breaker.check()
        events = breaker.get_events()
        assert len(events) > 0
        assert events[0].to_state == CircuitState.OPEN.value
```

---

## Monitoring

| Metric | Collection | Warning | Critical | Alert Channel |
|---|---|---|---|---|
| Circuit state | Continuous | Any trip | Trip lasting > 5 min | Incident response |
| Trip frequency | Daily | > 3 trips/day | > 10 trips/day | Operations + security |
| Degradation level | Continuous | Level ≥ 2 | Level ≥ 3 | Operations |
| Half-open probe success rate | Per-probe | < 50% | < 20% | Operations |
| Time to recovery (trip → close) | Per-trip | > 10 minutes | > 60 minutes | Operations + management |
| False trip rate | Weekly | > 20% of trips | > 50% of trips | Engineering |

---

## Failure Modes

| Failure Mode | Cause | Detection | Mitigation |
|---|---|---|---|
| **Breaker never trips** | Thresholds too high; metrics not updated | Runaway detected by external monitoring | Conservative thresholds; anomaly-based detection as supplement |
| **Breaker stuck open** | Recovery conditions never met | Circuit remains OPEN for extended period | Manual reset capability; automatic half-open after cool-down |
| **Flapping** | Thresholds at boundary; rapid trip/recover | Rapid state transitions | Hysteresis; longer cool-down; gradual ramp-up |
| **Breaker bypassed** | Code path doesn't check breaker state | Requests processed while circuit is OPEN | Architectural enforcement: breaker check is mandatory middleware |
| **Breaker disabled** | Configuration change removes breaker | No state transitions logged | Configuration monitoring; breaker-enable check in health endpoint |

---

## When Not To Use

1. **Fully deterministic systems with bounded execution:** If your system always produces exactly one response per request with no tool calls, no loops, and no autonomous behavior, there is no runaway risk to break.

2. **Systems with very low traffic where human response is sufficient:** If your system processes < 1 request per minute and a human operator can respond to incidents in seconds, the circuit breaker adds complexity without proportional benefit.

3. **Systems where stopping is more dangerous than continuing:** In some safety-critical systems (e.g., autonomous medical diagnosis), halting the AI is worse than degraded operation. In these cases, use graceful degradation instead of full-stop tripping.

4. **When the system already has robust rate limiting and resource quotas:** If your infrastructure enforces hard resource limits that effectively prevent runaway (e.g., Kubernetes resource limits, API gateway rate limits), a separate circuit breaker may be redundant. Ensure behavioral runaway (not just resource runaway) is also covered.

5. **Development environments with no real users:** Circuit breakers are primarily a production safety mechanism. In development, they can mask bugs. Consider disabling or making them very lenient in development.

---

## Assurance Evidence

| Artifact | Description | Format | Retention |
|---|---|---|---|
| Circuit breaker event log | All state transitions with reasons | Structured JSON | 2 years |
| Trip analysis reports | Root cause analysis of each trip | Report | 1 year |
| Threshold configuration | Current thresholds with versioning | JSON export | Permanent (versioned) |
| Recovery time metrics | Time from trip to recovery per incident | Metrics | 1 year |
| Flapping detection reports | Incidents of rapid trip/recovery cycling | Report | 1 year |

---

*Pattern version: 1.0.0 | AI Security from Scratch*
