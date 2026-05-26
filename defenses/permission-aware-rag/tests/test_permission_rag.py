"""Tests for Permission-Aware RAG."""

import pytest
from permission_rag import (
    AccessLevel,
    Document,
    PermissionRAG,
    Role,
    RetrievalResult,
    User,
    can_access,
)


class TestAccessHierarchy:
    def test_guest_can_access_public(self):
        assert can_access(Role.GUEST, AccessLevel.PUBLIC) is True

    def test_guest_cannot_access_internal(self):
        assert can_access(Role.GUEST, AccessLevel.INTERNAL) is False

    def test_guest_cannot_access_confidential(self):
        assert can_access(Role.GUEST, AccessLevel.CONFIDENTIAL) is False

    def test_employee_can_access_internal(self):
        assert can_access(Role.EMPLOYEE, AccessLevel.INTERNAL) is True

    def test_employee_cannot_access_confidential(self):
        assert can_access(Role.EMPLOYEE, AccessLevel.CONFIDENTIAL) is False

    def test_manager_can_access_confidential(self):
        assert can_access(Role.MANAGER, AccessLevel.CONFIDENTIAL) is True

    def test_manager_cannot_access_restricted(self):
        assert can_access(Role.MANAGER, AccessLevel.RESTRICTED) is False

    def test_admin_can_access_everything(self):
        for level in AccessLevel:
            assert can_access(Role.ADMIN, level) is True


class TestUser:
    def test_user_can_access_within_role(self):
        user = User(user_id="u1", role=Role.EMPLOYEE)
        assert user.can_access(AccessLevel.PUBLIC) is True
        assert user.can_access(AccessLevel.INTERNAL) is True

    def test_user_cannot_access_beyond_role(self):
        user = User(user_id="u1", role=Role.EMPLOYEE)
        assert user.can_access(AccessLevel.CONFIDENTIAL) is False

    def test_user_with_additional_access(self):
        user = User(user_id="u1", role=Role.GUEST, additional_access={AccessLevel.INTERNAL})
        assert user.can_access(AccessLevel.INTERNAL) is True
        assert user.can_access(AccessLevel.CONFIDENTIAL) is False


class TestDocument:
    def test_document_creation(self):
        doc = Document(doc_id="d1", content="Hello", access_level=AccessLevel.PUBLIC)
        assert doc.doc_id == "d1"
        assert doc.content == "Hello"
        assert doc.access_level == AccessLevel.PUBLIC
        assert doc.title == "d1"  # Falls back to doc_id

    def test_document_with_title(self):
        doc = Document(doc_id="d1", content="Hello", access_level=AccessLevel.PUBLIC, title="My Doc")
        assert doc.title == "My Doc"


class TestPermissionRAG:
    def setup_method(self):
        self.rag = PermissionRAG()
        self.rag.add_document(Document(
            doc_id="public-doc",
            content="Public company information and FAQ",
            access_level=AccessLevel.PUBLIC,
            tags=["faq", "company"],
        ))
        self.rag.add_document(Document(
            doc_id="internal-doc",
            content="Internal employee handbook and policies",
            access_level=AccessLevel.INTERNAL,
            tags=["handbook", "policies"],
        ))
        self.rag.add_document(Document(
            doc_id="confidential-doc",
            content="Confidential salary data and financial reports",
            access_level=AccessLevel.CONFIDENTIAL,
            tags=["salary", "financial"],
        ))
        self.rag.add_document(Document(
            doc_id="restricted-doc",
            content="Restricted API keys and production secrets",
            access_level=AccessLevel.RESTRICTED,
            tags=["api", "secrets"],
        ))

    def test_guest_retrieves_only_public(self):
        user = User(user_id="guest1", role=Role.GUEST)
        results = self.rag.retrieve(user, "company information")
        assert all(r.access_granted for r in results)
        doc_ids = {r.document.doc_id for r in results}
        assert "public-doc" in doc_ids
        assert "internal-doc" not in doc_ids
        assert "confidential-doc" not in doc_ids
        assert "restricted-doc" not in doc_ids

    def test_employee_retrieves_public_and_internal(self):
        user = User(user_id="emp1", role=Role.EMPLOYEE)
        results = self.rag.retrieve(user, "information policies")
        doc_ids = {r.document.doc_id for r in results}
        assert "public-doc" in doc_ids
        assert "internal-doc" in doc_ids
        assert "confidential-doc" not in doc_ids

    def test_admin_retrieves_everything(self):
        user = User(user_id="admin1", role=Role.ADMIN)
        results = self.rag.retrieve(user, "information data secrets")
        doc_ids = {r.document.doc_id for r in results}
        assert len(doc_ids) == 4

    def test_check_access_granted(self):
        user = User(user_id="emp1", role=Role.EMPLOYEE)
        result = self.rag.check_access(user, "public-doc")
        assert result.access_granted is True

    def test_check_access_denied(self):
        user = User(user_id="guest1", role=Role.GUEST)
        result = self.rag.check_access(user, "confidential-doc")
        assert result.access_granted is False
        assert "cannot access" in result.reason.lower() or "insufficient" in result.reason.lower()

    def test_check_access_nonexistent_doc(self):
        user = User(user_id="guest1", role=Role.GUEST)
        result = self.rag.check_access(user, "nonexistent")
        assert result.access_granted is False

    def test_retrieve_with_denied(self):
        user = User(user_id="guest1", role=Role.GUEST)
        debug = self.rag.retrieve_with_denied(user, "data")
        assert len(debug["granted"]) >= 1
        assert len(debug["denied"]) >= 1
        assert debug["total_documents"] == 4

    def test_add_and_remove_document(self):
        rag = PermissionRAG()
        doc = Document(doc_id="temp", content="Temporary", access_level=AccessLevel.PUBLIC)
        rag.add_document(doc)
        assert len(rag.documents) == 1
        assert rag.remove_document("temp") is True
        assert len(rag.documents) == 0
        assert rag.remove_document("nonexistent") is False

    def test_get_documents_by_level(self):
        public_docs = self.rag.get_documents_by_level(AccessLevel.PUBLIC)
        assert len(public_docs) == 1
        assert public_docs[0].doc_id == "public-doc"

    def test_get_user_accessible_docs(self):
        guest = User(user_id="g1", role=Role.GUEST)
        accessible = self.rag.get_user_accessible_docs(guest)
        assert len(accessible) == 1
        assert accessible[0].access_level == AccessLevel.PUBLIC

    def test_audit_log_records_retrieval(self):
        user = User(user_id="emp1", role=Role.EMPLOYEE)
        self.rag.retrieve(user, "information")
        log = self.rag.audit_log
        assert any(entry["action"] == "retrieve" for entry in log)

    def test_audit_log_records_denied_access(self):
        user = User(user_id="guest1", role=Role.GUEST)
        self.rag.check_access(user, "restricted-doc")
        log = self.rag.audit_log
        denied_entries = [e for e in log if e.get("granted") is False]
        assert len(denied_entries) >= 1

    def test_top_k_limits_results(self):
        user = User(user_id="admin1", role=Role.ADMIN)
        results = self.rag.retrieve(user, "information data secrets", top_k=2)
        assert len(results) <= 2

    def test_get_summary(self):
        summary = self.rag.get_summary()
        assert summary["total_documents"] == 4
        assert summary["by_access_level"]["public"] == 1
        assert summary["by_access_level"]["restricted"] == 1

    def test_retrieve_no_matching_docs(self):
        user = User(user_id="guest1", role=Role.GUEST)
        results = self.rag.retrieve(user, "quantum physics astrophysics")
        # May return empty results if no keyword match
        assert isinstance(results, list)
