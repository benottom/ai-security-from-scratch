# Pattern: Permission-Aware RAG

> **Pattern ID:** PAT-RAG-001 | **Category:** Data Security | **Maturity:** Proven

---

## Problem

Retrieval-Augmented Generation (RAG) systems retrieve documents from a knowledge base and inject them into the model's context window to ground responses in factual data. The standard RAG pipeline retrieves documents based solely on semantic relevance to the user's query, with no regard for the user's authorization level. This creates a critical security gap: a user with restricted access can craft queries that retrieve and expose documents they are not authorized to see.

The problem is a missing control: the retrieval pipeline acts as an unconstrained information pump, with no controller enforcing access policies at the retrieval boundary. The RAG retriever optimizes for relevance, not authorization, making it a reliable oracle for privilege escalation.

**Concrete failure scenario:** A junior employee asks the AI assistant, "What are the board's contingency plans for the acquisition?" The RAG pipeline retrieves the confidential board minutes because they are semantically relevant, and the model summarizes them verbatim — despite the employee lacking authorization to view board-level documents.

---

## Threat Model

| Attribute | Value |
|---|---|
| **Threat ID** | T-RAG-001 |
| **Threat Name** | Unauthorized data access via RAG retrieval |
| **Attack Vector** | Semantic queries that exploit relevance-based retrieval without access control |
| **Impact** | Confidential data exposure, regulatory violations (GDPR, HIPAA), competitive intelligence leakage |
| **Likelihood** | High — the default behavior of RAG systems is to retrieve by relevance alone |
| **Risk** | Critical |
| **OWASP LLM Top 10** | LLM06: Sensitive Data Disclosure |
| **NIST AI RMF** | MAP 2.3, MEASURE 2.6 |

**Attack variants:**
1. **Direct probing:** User asks questions targeting specific sensitive documents
2. **Broad net casting:** User asks general questions that retrieve a wide swath of documents, fishing for sensitive ones
3. **Context accumulation:** User asks a series of narrow questions that, combined, reconstruct a sensitive document piece by piece
4. **Metadata exploitation:** User crafts queries that exploit document metadata (titles, summaries) even when full documents are access-controlled
5. **Timing attacks:** User infers document existence from response latency differences between accessible and inaccessible hits

---

## Control-Theoretic View

### Objective

Ensure that RAG-retrieved content is filtered to only include documents the querying user is authorized to access, regardless of semantic relevance.

### Controller

The **Permission Filter** — a component situated between the vector store retrieval results and the context assembly that enforces Access Control Lists (ACLs) on every retrieved document chunk before it enters the model context.

### Observations

| Observation | Source | Type |
|---|---|---|
| Retrieved document IDs and metadata | Vector store query results | Synchronous |
| User identity and group memberships | Authentication system / JWT claims | Synchronous |
| Document ACLs (who can access what) | ACL store / policy engine | Synchronous |
| Document sensitivity classification | Document metadata | Synchronous |
| Retrieval relevance scores | Vector store | Synchronous |

### Actions

| Action | Effect | Preconditions |
|---|---|---|
| Filter out unauthorized documents | Remove documents user cannot access from results | ACL check fails for document + user |
| Redact sensitive portions | Replace unauthorized sections with [REDACTED] | Partial access (field-level ACL) |
| Log access attempt | Record retrieval attempt for audit trail | Any document retrieved (authorized or not) |
| Alert on suspicious pattern | Notify security team | User repeatedly querying across denied documents |
| Return empty results | No documents provided to model | All results unauthorized |

### Feedback

- Access audit logs are analyzed for patterns of unauthorized access attempts
- Red-team exercises test whether sensitive documents can be reconstructed through accumulation
- False-negative rate (unauthorized docs slipping through) measured via periodic sampling

### Disturbances

| Disturbance | Source | Mitigation |
|---|---|---|
| ACL staleness | Document permissions changed but not propagated | Event-driven ACL updates with cache invalidation |
| Embedding leakage | Sensitive info preserved in vector embeddings even after ACL change | Re-embed on ACL change; consider per-chunk ACLs |
| Accumulation attacks | User reconstructs sensitive content from many partial results | Rate limiting + cross-query analysis + output validation |
| Group explosion | User has many group memberships causing slow ACL evaluation | Cache resolved permissions; pre-compute access sets |

### Unsafe States

| Unsafe State | Condition | Consequence |
|---|---|---|
| Unauthorized document in context | ACL check bypassed or fails open | Confidential data exposure via model output |
| Stale ACL applied | Permission revocation not propagated | Formerly authorized user retains access |
| Partial document leakage | Field-level ACLs not enforced | Sensitive fields within accessible documents exposed |
| Metadata exposure | Document titles/summaries leak even when body is filtered | Information leakage through metadata |

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                        User Query                             │
└─────────────────────────┬────────────────────────────────────┘
                          │
                          ▼
               ┌─────────────────────┐
               │   RAG Retriever      │──── Standard semantic retrieval
               │   (Vector Store)     │
               └─────────┬───────────┘
                         │ Retrieved documents (unfiltered)
                         ▼
               ┌─────────────────────────────────┐
               │      Permission Filter            │
               │                                   │
               │  ┌─────────────────────────────┐ │
               │  │  ACL Resolution Engine      │ │
               │  │  (User → Groups → Perms)    │ │
               │  └─────────────────────────────┘ │
               │  ┌─────────────────────────────┐ │
               │  │  Document Access Check       │ │
               │  │  (Doc ACL vs User Perms)    │ │
               │  └─────────────────────────────┘ │
               │  ┌─────────────────────────────┐ │
               │  │  Field-Level Redaction       │ │
               │  │  (Partial access support)   │ │
               │  └─────────────────────────────┘ │
               │  ┌─────────────────────────────┐ │
               │  │  Access Audit Logger         │ │
               │  └─────────────────────────────┘ │
               └─────────┬─────────────────────────┘
                         │ Filtered documents (authorized only)
                         ▼
               ┌─────────────────────┐
               │   Context Assembler  │──── Build model context
               └─────────┬───────────┘
                         │
                         ▼
               ┌─────────────────────┐
               │   LLM Inference      │
               └─────────┬───────────┘
                         │
                         ▼
               ┌─────────────────────┐
               │   Output Validation  │──── Verify no unauthorized data in output
               └─────────────────────┘
```

---

## Implementation

### Permission Filter

```python
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class AccessLevel(Enum):
    NONE = "none"            # No access
    METADATA = "metadata"    # Can see title/summary only
    READ = "read"            # Can read full document
    READ_REDACTED = "read_redacted"  # Can read with sensitive fields redacted


@dataclass
class DocumentACL:
    """Access control list for a single document."""
    document_id: str
    allowed_groups: set[str]
    denied_groups: set[str]
    sensitivity_level: str          # PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED
    redacted_fields: dict[str, str] = field(default_factory=dict)  # field_name → redaction_reason
    owner: str = ""


@dataclass
class UserContext:
    """User identity and resolved permissions."""
    user_id: str
    groups: set[str]
    clearance_level: str   # PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED
    roles: set[str] = field(default_factory=set)


@dataclass
class RetrievedDocument:
    """A document retrieved from the vector store."""
    document_id: str
    content: str
    metadata: dict
    relevance_score: float
    acl: Optional[DocumentACL] = None


@dataclass
class FilteredResult:
    """A document after permission filtering."""
    document_id: str
    content: str
    access_level: AccessLevel
    redacted_fields: list[str]
    was_modified: bool


class PermissionAwareRAG:
    """RAG pipeline that enforces document-level access control.

    Control objective: Users may only retrieve and receive content
    from documents they are authorized to access.
    """

    CLEARANCE_HIERARCHY = {
        "PUBLIC": 0,
        "INTERNAL": 1,
        "CONFIDENTIAL": 2,
        "RESTRICTED": 3,
    }

    def __init__(self, retriever, acl_store, audit_logger=None):
        self.retriever = retriever
        self.acl_store = acl_store
        self.audit_logger = audit_logger

    def retrieve_and_filter(
        self,
        query: str,
        user: UserContext,
        top_k: int = 5,
    ) -> list[FilteredResult]:
        """Retrieve documents and filter by user permissions."""
        # Step 1: Retrieve candidates (unfiltered by permission)
        candidates = self.retriever.retrieve(query, top_k=top_k * 3)

        # Step 2: Enrich with ACLs
        for doc in candidates:
            doc.acl = self.acl_store.get_acl(doc.document_id)

        # Step 3: Filter by permissions
        results = []
        for doc in candidates:
            filtered = self._apply_permissions(doc, user)
            if filtered.access_level != AccessLevel.NONE:
                results.append(filtered)
            else:
                # Log denied access attempt
                if self.audit_logger:
                    self.audit_logger.log_access_denied(
                        user_id=user.user_id,
                        document_id=doc.document_id,
                        reason="ACL denied",
                    )

            if len(results) >= top_k:
                break

        # Step 4: Log successful accesses
        if self.audit_logger:
            for result in results:
                self.audit_logger.log_access_granted(
                    user_id=user.user_id,
                    document_id=result.document_id,
                    access_level=result.access_level.value,
                )

        return results[:top_k]

    def _apply_permissions(self, doc: RetrievedDocument, user: UserContext) -> FilteredResult:
        """Determine user access to a document and apply filtering."""
        if doc.acl is None:
            # No ACL → deny by default
            return FilteredResult(
                document_id=doc.document_id,
                content="",
                access_level=AccessLevel.NONE,
                redacted_fields=[],
                was_modified=False,
            )

        # Check clearance level
        if not self._clearance_sufficient(user.clearance_level, doc.acl.sensitivity_level):
            # May still have metadata access
            if self._has_group_access(user.groups, doc.acl, require_clearance=False):
                return FilteredResult(
                    document_id=doc.document_id,
                    content=doc.metadata.get("title", "[Access Restricted]"),
                    access_level=AccessLevel.METADATA,
                    redacted_fields=["content"],
                    was_modified=True,
                )
            return FilteredResult(
                document_id=doc.document_id,
                content="",
                access_level=AccessLevel.NONE,
                redacted_fields=[],
                was_modified=False,
            )

        # Check group-based access
        if not self._has_group_access(user.groups, doc.acl):
            return FilteredResult(
                document_id=doc.document_id,
                content="",
                access_level=AccessLevel.NONE,
                redacted_fields=[],
                was_modified=False,
            )

        # Apply field-level redaction if needed
        if doc.acl.redacted_fields:
            content, redacted = self._redact_fields(doc.content, doc.acl.redacted_fields, user)
            if redacted:
                return FilteredResult(
                    document_id=doc.document_id,
                    content=content,
                    access_level=AccessLevel.READ_REDACTED,
                    redacted_fields=redacted,
                    was_modified=True,
                )

        return FilteredResult(
            document_id=doc.document_id,
            content=doc.content,
            access_level=AccessLevel.READ,
            redacted_fields=[],
            was_modified=False,
        )

    def _clearance_sufficient(self, user_clearance: str, doc_sensitivity: str) -> bool:
        """Check if user clearance meets document sensitivity level."""
        return self.CLEARANCE_HIERARCHY.get(user_clearance, 0) >= self.CLEARANCE_HIERARCHY.get(doc_sensitivity, 999)

    def _has_group_access(self, user_groups: set[str], acl: DocumentACL, require_clearance: bool = True) -> bool:
        """Check if any user group is in the allowed groups."""
        if acl.allowed_groups and not (user_groups & acl.allowed_groups):
            return False
        if acl.denied_groups and (user_groups & acl.denied_groups):
            return False
        return True

    def _redact_fields(self, content: str, redacted_fields: dict, user: UserContext) -> tuple[str, list[str]]:
        """Redact specified fields from document content."""
        import re
        redacted = []
        result = content
        for field_name, reason in redacted_fields.items():
            pattern = rf"{field_name}\s*[:=]\s*[^\n]+"
            if re.search(pattern, result, re.IGNORECASE):
                result = re.sub(pattern, f"{field_name}: [REDACTED — {reason}]", result, flags=re.IGNORECASE)
                redacted.append(field_name)
        return result, redacted
```

---

## Tests

```python
import pytest
from permission_aware_rag import (
    PermissionAwareRAG, UserContext, DocumentACL, RetrievedDocument, AccessLevel
)


class TestPermissionAwareRAG:
    """Security regression tests for Permission-Aware RAG."""

    @pytest.fixture
    def mock_retriever(self):
        """Mock retriever that returns documents with known ACLs."""
        ...

    @pytest.fixture
    def pipeline(self, mock_retriever):
        return PermissionAwareRAG(
            retriever=mock_retriever,
            acl_store=MockACLStore(),
        )

    @pytest.fixture
    def restricted_user(self):
        return UserContext(
            user_id="u-junior-001",
            groups={"employees", "engineering"},
            clearance_level="INTERNAL",
        )

    @pytest.fixture
    def executive_user(self):
        return UserContext(
            user_id="u-exec-001",
            groups={"employees", "executives", "board"},
            clearance_level="RESTRICTED",
        )

    def test_restricted_user_cannot_access_confidential_doc(self, pipeline, restricted_user):
        results = pipeline.retrieve_and_filter("acquisition contingency plans", restricted_user)
        confidential_ids = {r.document_id for r in results if r.access_level == AccessLevel.READ and "board-minutes" in r.document_id}
        assert len(confidential_ids) == 0, "Restricted user accessed confidential documents"

    def test_executive_user_can_access_confidential_doc(self, pipeline, executive_user):
        results = pipeline.retrieve_and_filter("acquisition contingency plans", executive_user)
        assert any(r.access_level == AccessLevel.READ for r in results), "Executive could not access authorized documents"

    def test_redacted_fields_are_removed(self, pipeline, restricted_user):
        """Verify that redacted fields do not appear in output content."""
        results = pipeline.retrieve_and_filter("employee salary data", restricted_user)
        for result in results:
            assert "salary" not in result.content.lower() or "[REDACTED" in result.content

    def test_denied_access_is_logged(self, pipeline, restricted_user):
        """Verify that denied access attempts are audit-logged."""
        pipeline.retrieve_and_filter("confidential board strategy", restricted_user)
        assert pipeline.audit_logger.denied_count > 0

    def test_no_documents_leaked_through_metadata(self, pipeline, restricted_user):
        """Verify that metadata-only documents don't leak content."""
        results = pipeline.retrieve_and_filter("confidential project details", restricted_user)
        for result in results:
            if result.access_level == AccessLevel.METADATA:
                assert "CONFIDENTIAL" not in result.content or result.content == result.content.split("\n")[0]

    def test_accumulation_attack_detected(self, pipeline, restricted_user):
        """Verify that repeated queries targeting the same denied document trigger an alert."""
        for _ in range(10):
            pipeline.retrieve_and_filter("project xavier details", restricted_user)
        assert pipeline.audit_logger.suspicious_pattern_detected
```

---

## Monitoring

| Metric | Collection | Warning | Critical | Alert Channel |
|---|---|---|---|---|
| Unauthorized retrieval attempts | Per-request | > 5/minute per user | > 20/minute per user | Security SIEM |
| ACL cache miss rate | Per-request | > 10% | > 30% | Infrastructure |
| Retrieval latency (with filtering) | Per-request | > 200ms p95 | > 500ms p95 | Performance |
| Field redaction rate | Per-request | > 20% of results | > 50% of results | Data governance |
| Accumulation attack indicators | Rolling window | > 3 denied docs in 5 min | > 10 denied docs in 5 min | Incident response |

---

## Failure Modes

| Failure Mode | Cause | Detection | Mitigation |
|---|---|---|---|
| **ACL cache staleness** | Permissions revoked but cache not invalidated | User accesses newly-restricted document | Event-driven cache invalidation; short TTL |
| **Embedding side-channel** | Sensitive info in embeddings persists after ACL change | Red-team reconstruction attack | Re-embed documents on ACL change; consider encryption at rest |
| **Accumulation bypass** | User reconstructs doc from many partial, authorized snippets | Cross-query correlation analysis | Rate-limit per-document queries; output validation |
| **Metadata leakage** | Document title/summary reveals sensitive info | Audit log review | Apply same ACLs to metadata as to content |
| **Latency regression** | ACL evaluation on large result sets is slow | P95 latency threshold breach | Pre-compute access sets; parallelize ACL checks |

---

## When Not To Use

1. **Single-tenancy systems with one user class:** If every user has the same access level and all documents are equally accessible, permission filtering adds unnecessary complexity and latency.

2. **Fully public knowledge bases:** When all documents are public (e.g., public documentation), there are no authorization boundaries to enforce.

3. **Systems with application-level access control already in place:** If your application already restricts the retriever's search space to only documents the user can access (e.g., per-user vector store collections), an additional filter layer is redundant.

4. **Non-RAG architectures:** If your system does not use retrieval augmentation, this pattern does not apply. Use the AI Security Gateway pattern for general input/output security.

5. **Extremely high-query-volume systems where per-request ACL resolution is infeasible:** In these cases, consider pre-computing user-document access matrices that are updated on permission changes rather than resolved per-request.

---

## Assurance Evidence

| Artifact | Description | Format | Retention |
|---|---|---|---|
| Access audit log | Every retrieve + filter decision with outcome | Structured JSON | 1 year |
| ACL configuration snapshot | Current state of document access controls | JSON export | Permanent (versioned) |
| Permission regression test results | Pass/fail for all access control test cases | JUnit XML | Permanent |
| Accumulation attack test results | Reconstruction attempt outcomes | Markdown report | Permanent |
| Latency benchmarks | Retrieval + filtering latency percentiles | Performance report | 90 days |

---

*Pattern version: 1.0.0 | AI Security from Scratch*
