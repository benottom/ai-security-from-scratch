"""
Permission-Aware RAG — Retrieval-Augmented Generation with document-level access control.

Control-Theoretic View:
    In the AI control loop, RAG retrieval acts as a feedforward controller — it injects
    external information into the model's context. Without permission filtering, a
    disturbance (malicious query or misconfigured retrieval) can cause the plant (LLM)
    to produce outputs based on information the user should not access.

    The permission-aware RAG layer acts as an authorization filter on the feedforward
    path, ensuring only authorized documents reach the model context for a given user.

Key Properties:
    1. Role-based access control (RBAC) on documents
    2. Document-level access labels (public, internal, confidential, restricted)
    3. Retrieval-time filtering: only documents the user can access are returned
    4. Audit logging of access decisions
    5. Deny-by-default: if a document has no ACL entry, it is inaccessible
"""

from __future__ import annotations

import enum
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


class AccessLevel(enum.Enum):
    """Document access classification levels (increasingly restrictive)."""
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"


class Role(enum.Enum):
    """User roles with associated maximum access levels."""
    GUEST = "guest"
    EMPLOYEE = "employee"
    MANAGER = "manager"
    ADMIN = "admin"


# Role -> maximum AccessLevel mapping
ROLE_ACCESS_MAP: dict[Role, AccessLevel] = {
    Role.GUEST: AccessLevel.PUBLIC,
    Role.EMPLOYEE: AccessLevel.INTERNAL,
    Role.MANAGER: AccessLevel.CONFIDENTIAL,
    Role.ADMIN: AccessLevel.RESTRICTED,
}

# AccessLevel hierarchy (higher index = more restrictive)
_ACCESS_HIERARCHY = [
    AccessLevel.PUBLIC,
    AccessLevel.INTERNAL,
    AccessLevel.CONFIDENTIAL,
    AccessLevel.RESTRICTED,
]


def can_access(role: Role, required_level: AccessLevel) -> bool:
    """
    Check if a role has sufficient clearance for a given access level.

    Uses a hierarchical model: ADMIN can access everything, GUEST can only
    access PUBLIC documents.
    """
    max_level = ROLE_ACCESS_MAP[role]
    max_idx = _ACCESS_HIERARCHY.index(max_level)
    required_idx = _ACCESS_HIERARCHY.index(required_level)
    return required_idx <= max_idx


@dataclass
class Document:
    """A document in the RAG knowledge base with access control metadata."""
    doc_id: str
    content: str
    access_level: AccessLevel
    title: str = ""
    tags: list[str] = field(default_factory=list)
    embedding: Optional[list[float]] = None  # Placeholder for vector embedding
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        if not self.title:
            self.title = self.doc_id


@dataclass
class User:
    """A user with a role and associated permissions."""
    user_id: str
    role: Role
    name: str = ""
    additional_access: set[AccessLevel] = field(default_factory=set)

    def can_access(self, required_level: AccessLevel) -> bool:
        """Check if this user can access a document at the given level."""
        if can_access(self.role, required_level):
            return True
        return required_level in self.additional_access


@dataclass
class RetrievalResult:
    """A single retrieval result with access decision."""
    document: Document
    score: float
    access_granted: bool
    reason: str = ""


class PermissionRAG:
    """
    Permission-Aware RAG system that filters retrieval results by user authorization.

    Usage:
        rag = PermissionRAG()
        rag.add_document(Document(doc_id="doc1", content="Public info", access_level=AccessLevel.PUBLIC))
        rag.add_document(Document(doc_id="doc2", content="Secret info", access_level=AccessLevel.RESTRICTED))

        user = User(user_id="u1", role=Role.GUEST)
        results = rag.retrieve(user, "info")
        # Only doc1 is returned (GUEST cannot access RESTRICTED)
    """

    def __init__(self):
        self._documents: dict[str, Document] = {}
        self._audit_log: list[dict] = []

    @property
    def documents(self) -> list[Document]:
        return list(self._documents.values())

    @property
    def audit_log(self) -> list[dict]:
        return list(self._audit_log)

    def add_document(self, document: Document) -> None:
        """Add a document to the knowledge base."""
        self._documents[document.doc_id] = document
        self._log_action("add_document", user_id=None, doc_id=document.doc_id,
                         access_level=document.access_level.value, granted=True)

    def remove_document(self, doc_id: str) -> bool:
        """Remove a document from the knowledge base. Returns True if found."""
        if doc_id in self._documents:
            del self._documents[doc_id]
            self._log_action("remove_document", user_id=None, doc_id=doc_id, granted=True)
            return True
        return False

    def retrieve(
        self,
        user: User,
        query: str,
        top_k: int = 5,
        min_score: float = 0.0,
    ) -> list[RetrievalResult]:
        """
        Retrieve documents matching a query, filtered by user permissions.

        In a production system, this would use vector similarity search.
        This implementation uses simple keyword matching as a stand-in.

        Args:
            user: The user making the query.
            query: The search query string.
            top_k: Maximum number of results to return.
            min_score: Minimum relevance score threshold.

        Returns:
            A list of RetrievalResult objects, only including documents the user can access.
        """
        all_results = self._search_all(user, query)

        # Filter by access
        accessible_results = []
        denied_count = 0
        for result in all_results:
            if result.access_granted:
                accessible_results.append(result)
            else:
                denied_count += 1

        # Sort by score and limit to top_k
        accessible_results.sort(key=lambda r: r.score, reverse=True)
        final_results = accessible_results[:top_k]

        self._log_action(
            "retrieve",
            user_id=user.user_id,
            user_role=user.role.value,
            query=query[:200],
            results_returned=len(final_results),
            results_denied=denied_count,
            granted=True,
        )

        return final_results

    def retrieve_with_denied(
        self,
        user: User,
        query: str,
        top_k: int = 5,
    ) -> dict:
        """
        Retrieve documents including denied results for audit/debugging.

        Returns:
            A dict with 'granted' and 'denied' lists of RetrievalResult.
        """
        all_results = self._search_all(user, query)
        granted = [r for r in all_results if r.access_granted]
        denied = [r for r in all_results if not r.access_granted]
        granted.sort(key=lambda r: r.score, reverse=True)

        return {
            "granted": granted[:top_k],
            "denied": denied,
            "total_documents": len(self._documents),
            "total_granted": len(granted),
            "total_denied": len(denied),
        }

    def check_access(self, user: User, doc_id: str) -> RetrievalResult:
        """
        Check if a user can access a specific document.

        Returns:
            A RetrievalResult indicating access decision.
        """
        doc = self._documents.get(doc_id)
        if doc is None:
            self._log_action("check_access", user_id=user.user_id, doc_id=doc_id,
                             granted=False, reason="Document not found")
            return RetrievalResult(
                document=Document(doc_id=doc_id, content="", access_level=AccessLevel.RESTRICTED),
                score=0.0,
                access_granted=False,
                reason="Document not found",
            )

        has_access = user.can_access(doc.access_level)
        reason = "" if has_access else f"Role {user.role.value} cannot access {doc.access_level.value} documents"

        self._log_action(
            "check_access",
            user_id=user.user_id,
            user_role=user.role.value,
            doc_id=doc_id,
            doc_access_level=doc.access_level.value,
            granted=has_access,
            reason=reason,
        )

        return RetrievalResult(
            document=doc,
            score=1.0,
            access_granted=has_access,
            reason=reason,
        )

    def _search_all(self, user: User, query: str) -> list[RetrievalResult]:
        """
        Search all documents with keyword matching and access checking.

        This is a simplified implementation. In production, replace with
        vector similarity search (e.g., cosine similarity over embeddings).
        """
        query_terms = set(query.lower().split())
        results: list[RetrievalResult] = []

        for doc in self._documents.values():
            # Simple keyword-based scoring
            doc_terms = set(doc.content.lower().split()) | set(t.lower() for t in doc.tags)
            if doc.title:
                doc_terms |= set(doc.title.lower().split())

            common = query_terms & doc_terms
            if not common and query_terms:
                score = 0.0
            else:
                # TF-inspired scoring: fraction of query terms found
                score = len(common) / len(query_terms) if query_terms else 0.0

            has_access = user.can_access(doc.access_level)
            reason = "" if has_access else f"Insufficient clearance (need {doc.access_level.value})"

            results.append(RetrievalResult(
                document=doc,
                score=round(score, 3),
                access_granted=has_access,
                reason=reason,
            ))

        return results

    def get_documents_by_level(self, access_level: AccessLevel) -> list[Document]:
        """Get all documents at a given access level."""
        return [d for d in self._documents.values() if d.access_level == access_level]

    def get_user_accessible_docs(self, user: User) -> list[Document]:
        """Get all documents a user can access."""
        return [d for d in self._documents.values() if user.can_access(d.access_level)]

    def _log_action(self, action: str, **kwargs) -> None:
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": action,
            **kwargs,
        }
        self._audit_log.append(entry)

    def get_summary(self) -> dict:
        """Return a summary of the RAG knowledge base."""
        level_counts = {}
        for level in AccessLevel:
            level_counts[level.value] = sum(
                1 for d in self._documents.values() if d.access_level == level
            )
        return {
            "total_documents": len(self._documents),
            "by_access_level": level_counts,
            "audit_log_entries": len(self._audit_log),
        }
