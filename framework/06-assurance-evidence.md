# Producing Assurance Evidence for AI Systems

## "Trust Us, It's Secure" Is Not Enough

Every AI system deployed in a security-sensitive context will eventually face the question: "How do you know it's secure?" The answer must be more than a demonstration, a screenshot, or a developer's assurance. It must be structured, traceable, and testable evidence that connects claims about the system's security to the controls that enforce those claims and the data that validates those controls.

This is assurance evidence, and without it, security is opinion. With it, security becomes a defensible, auditable, and continuously validated property of the system.

The stakes are rising. Regulators (the EU AI Act, NIST AI RMF), industry standards (ISO 27001, SOC 2), and customer expectations all increasingly demand that organizations demonstrate — not just claim — the security of their AI systems. The ability to produce assurance evidence is becoming a competitive advantage and a compliance requirement.

## The Assurance Case Structure: Claim → Argument → Evidence

An assurance case is a structured argument that a system satisfies a set of security claims. It has three components:

1. **Claim**: A specific, testable statement about the system's security properties
2. **Argument**: The reasoning that connects the claim to the evidence
3. **Evidence**: The data that supports the argument

### Example Assurance Case

**Claim**: The RAG assistant does not expose PII in its outputs.

**Argument**: PII exposure is prevented by a three-layer defense: (1) retrieval access control ensures that documents containing PII are only retrieved for authorized users; (2) the output validation layer scans all outputs for PII patterns and redacts any matches; (3) a final human-review sampling process validates that the automated controls are effective.

**Evidence**:
- Policy configuration for retrieval access control (policy version, rules, effective dates)
- Control ledger logs showing every retrieval access control decision for the past 90 days
- Automated test results showing 100% detection rate on a PII test suite of 500 examples
- Red-team transcripts showing 0 successful PII exfiltration attempts across 200 adversarial scenarios
- Human review sampling results: 1,000 outputs reviewed, 0 PII exposures found

The assurance case is hierarchical. A top-level claim ("The system is secure") is decomposed into sub-claims ("PII is not exposed," "Unauthorized actions are prevented," "The system prompt is not leaked"), each with its own argument and evidence. This decomposition continues until every sub-claim is directly supported by testable evidence.

## Mapping Security Controls to Governance Frameworks

Governance frameworks define what organizations must do; security controls define what systems must do. The mapping between them is the bridge that turns technical evidence into governance compliance.

### ISO 27001

| ISO 27001 Control | AI Security Control | Evidence |
|---|---|---|
| A.8.1 Asset inventory | AI Bill of Materials (AI-BOM) | AI-BOM document, version history |
| A.8.2 Information classification | Document security classification in RAG | Retrieval access control policy, classification labels |
| A.8.9 Configuration management | Policy-as-code configurations | Policy repository, version control, deployment records |
| A.8.10 Information deletion | Memory retention policies and enforcement | Retention policy, deletion logs |
| A.8.25 Secure development lifecycle | Security regression test suite | Test results, coverage reports |
| A.8.28 Secure coding | Supervisory control implementation | Code review records, control activation logs |

### NIST AI RMF

| NIST AI RMF Function | AI Security Control | Evidence |
|---|---|---|
| GOVERN-1: Policies and procedures | Policy-as-code for AI security | Policy documents, policy-as-code repository |
| MAP-1: Context and risks | Control-loop threat model | Threat model document, STRIDE analysis |
| MAP-2: Categorization of risks | Unsafe state enumeration | Unsafe state registry, test assertions |
| MEASURE-1: Performance metrics | Control effectiveness metrics | Control activation rates, bypass rates, false positive rates |
| MEASURE-2: Evaluation | Red-team and adversarial testing | Red-team transcripts, test results |
| MANAGE-1: Risk treatment | Supervisory control implementation | Control configurations, control ledger logs |
| MANAGE-2: Monitoring | Control ledger and monitoring | Control ledger queries, anomaly detection alerts |

### OWASP LLM Top 10

| OWASP Risk | AI Security Control | Evidence |
|---|---|---|
| LLM01: Prompt Injection | Input validation, context separation | Input classifier accuracy, context separation test results |
| LLM02: Insecure Output Handling | Output validation, redaction | Output scanner detection rate, redaction logs |
| LLM03: Training Data Poisoning | Document provenance, retrieval validation | Provenance records, document validation logs |
| LLM04: Model Denial of Service | Rate limiting, circuit breakers | Rate limit configuration, circuit breaker activation logs |
| LLL05: Supply Chain Vulnerabilities | AI-BOM, dependency scanning | AI-BOM, vulnerability scan results |
| LLM06: Sensitive Information Disclosure | PII detection, access control | PII scanner test results, access control logs |
| LLM07: Insecure Plugin Design | Tool call mediation, approval gates | Tool call policy, gate decision logs |
| LLM08: Excessive Agency | Principle of least privilege, tool scoping | Tool access matrix, scope enforcement logs |
| LLM09: Overreliance | Hallucination detection, confidence scoring | Hallucination test results, confidence calibration data |
| LLM10: Model Theft | Access control, usage monitoring | Access logs, anomaly detection alerts |

## Types of Evidence

### Test Results

Automated security regression tests are the most reliable form of evidence. They are:

- **Repeatable**: They can be run at any time to verify that controls are still effective
- **Versioned**: They are tied to specific system versions, so you can track security over time
- **Objective**: They produce pass/fail results, not subjective assessments

Test evidence should include:
- Test suite version and date
- Number of tests, number passed, number failed
- Specific test cases that demonstrate each unsafe state is prevented
- Coverage analysis showing which controls and unsafe states are tested

### Control Ledger Logs

The control ledger (described in the observability document) is a rich source of assurance evidence. For each control, you can extract:

- Total number of evaluations
- Number of activations (how often the control was triggered)
- Number of blocks, modifications, and escalations
- Activation rate over time (to detect degradation)
- Zero bypass confirmations (the most important evidence — no unsafe state was reached despite the control being tested)

### Policy Configurations

Policy-as-code files are evidence that the security controls are defined, versioned, and deployed. For each policy:

- The policy definition (rules, conditions, actions)
- The deployment history (when was the policy activated, modified, or retired)
- The test coverage (which test cases exercise this policy)
- The approval record (who approved the policy, when, and under what change management process)

### Red-Team Transcripts

Red-team exercises are evidence that the system can withstand adversarial attack. For each exercise:

- The attack scenarios that were tested
- The techniques that were used (prompt injection, RAG poisoning, tool abuse, etc.)
- The results (which attacks were blocked, which succeeded)
- The remediation actions taken for any successful attacks
- The re-test results after remediation

Red-team evidence is particularly compelling because it demonstrates security under realistic adversarial conditions, not just under the happy path.

## Security Regression Tests as Living Evidence

Security regression tests are not just a one-time verification — they are living evidence that the system remains secure as it evolves. Every time the system is updated (new model version, new tool, new document in the knowledge base, new policy), the regression test suite is re-run. If all tests pass, the update is safe to deploy. If any test fails, the update is blocked until the failure is investigated and resolved.

This creates a continuous assurance loop:

1. **Define unsafe states** → Write test assertions
2. **Implement supervisory controls** → Write control implementation
3. **Run tests** → Generate test results (evidence)
4. **Deploy** → System is live with verified controls
5. **System evolves** → New model, new tools, new policies
6. **Re-run tests** → Verify that controls still work (updated evidence)
7. **If tests fail** → Block deployment, investigate, fix, re-test

This loop ensures that assurance evidence is always current. The test results from six months ago are not evidence that the system is secure today; the test results from the last deployment are.

## Building an AI Bill of Materials (AI-BOM)

An AI-BOM is a comprehensive inventory of all components that contribute to the AI system's behavior. It is the foundation for supply chain security and a key piece of assurance evidence.

### AI-BOM Contents

1. **Model Information**
   - Model name, version, and provider
   - Model architecture and parameters
   - Training data summary (datasets, collection dates, filtering criteria)
   - Fine-tuning data and methodology
   - Known limitations and biases
   - Evaluation results (benchmarks, red-team findings)

2. **Orchestration Components**
   - System prompt (version, hash)
   - Reasoning framework (chain-of-thought, ReAct, etc.)
   - Tool definitions (names, descriptions, parameter schemas)
   - Conversation management logic (context window strategy, history handling)

3. **Data Sources**
   - Knowledge base contents (document IDs, hashes, classification levels, last validation dates)
   - External APIs (endpoints, authentication methods, data sensitivity)
   - Memory stores (retention policies, access controls, storage location)

4. **Security Controls**
   - Supervisory control inventory (control IDs, types, deployment versions)
   - Policy-as-code files (versions, hashes, deployment dates)
   - Input/output filter configurations
   - Tool call mediation rules
   - Circuit breaker thresholds

5. **Infrastructure**
   - Hosting environment (cloud provider, region, compliance certifications)
   - Network architecture (trust boundaries, encryption)
   - Access control (identity provider, roles, permissions)
   - Logging and monitoring infrastructure

The AI-BOM should be maintained in a machine-readable format (JSON or YAML), version-controlled, and updated every time any component changes. It is the single source of truth for what the AI system is and what it depends on.

## Writing an Executive Security Report for AI Systems

Executive reports translate technical evidence into business-relevant assurance. They should be concise (2-4 pages), structured, and written in language that non-technical stakeholders can understand.

### Recommended Structure

1. **Executive Summary** (1 paragraph)
   - What is the system? What is its security posture? Are there any outstanding risks?

2. **Security Claims** (1 page)
   - List the top-level security claims (e.g., "PII is not exposed in outputs," "Unauthorized actions are blocked")
   - For each claim: status (verified/partially verified/unverified), evidence summary, last validation date

3. **Control Effectiveness Summary** (1 page)
   - Key metrics: control activation rate, bypass rate (must be zero), false positive rate
   - Trend: are controls becoming more or less effective over time?
   - Recent incidents: any control activations that required human intervention?

4. **Risk Register** (1 page)
   - Identified risks that are not fully mitigated
   - Risk severity, likelihood, and current mitigation status
   - Planned remediation actions and timelines

5. **Compliance Mapping** (1 page)
   - Status against relevant frameworks (ISO 27001, NIST AI RMF, EU AI Act)
   - Gaps and remediation plans

6. **Appendix: Evidence Index**
   - Links to detailed evidence (test results, control ledger queries, red-team reports, AI-BOM)
   - Evidence last updated date

## The Principle: Security Without Evidence Is Opinion

This entire framework rests on a single principle: **security without evidence is opinion**. An opinion may be correct, but it cannot be verified, audited, or defended. Evidence transforms security from a belief into a fact.

Every claim in this framework — every unsafe state, every supervisory control, every policy decision — should be backed by evidence. The control ledger produces the data, the regression tests verify the controls, the threat model defines the scope, and the assurance case structures the argument. Together, they form a complete, defensible security posture that can withstand scrutiny from auditors, regulators, customers, and adversaries.

The discipline of producing assurance evidence also improves the system itself. Writing test assertions forces you to define unsafe states precisely. Running red-team exercises forces you to confront realistic attacks. Mapping to governance frameworks forces you to think about the full scope of security, not just the technical details. The process of producing evidence is itself a security improvement process.

Build the system. Define the unsafe states. Implement the controls. Log the decisions. Test the controls. Produce the evidence. Repeat. This is the loop that makes AI security real.
