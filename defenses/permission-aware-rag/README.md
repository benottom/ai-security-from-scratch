# Permission-Aware RAG

## Overview

**Permission-Aware RAG** is a control-theoretic defense that enforces document-level access control in Retrieval-Augmented Generation systems. It ensures that users can only retrieve and receive information from documents they are authorized to access, preventing unauthorized data exposure through the AI assistant.

## Control-Theoretic View

```
┌──────────────┐     ┌──────────────────┐     ┌──────────────┐
│  User Query  │────▶│  Permission-Aware│────▶│   LLM        │
│  (Reference +│     │  RAG Filter      │     │  (Plant)     │
│  Disturbance)│     │  (Feedforward    │     │              │
│              │     │   Authorization) │     │              │
└──────────────┘     └──────────────────┘     └──────────────┘
                              ▲
                              │
                     ┌────────┴────────┐
                     │  Document Store  │
                     │  (with ACLs)     │
                     └─────────────────┘
```

In the control-loop model:
- **RAG retrieval** is a *feedforward controller* — it injects external information into the model context
- Without permission filtering, the feedforward path is *unfiltered*, allowing the plant (LLM) to process unauthorized data
- **Permission-Aware RAG** is the *authorization filter* on the feedforward path, ensuring only authorized documents reach the model

### Access Level Hierarchy

| Role      | Max Access Level | Can Access                                      |
|-----------|------------------|-------------------------------------------------|
| GUEST     | PUBLIC           | Public documents only                            |
| EMPLOYEE  | INTERNAL         | Public + Internal documents                      |
| MANAGER   | CONFIDENTIAL     | Public + Internal + Confidential documents       |
| ADMIN     | RESTRICTED       | All documents                                    |

## How It Works

1. **Document ACLs**: Every document in the knowledge base is tagged with an access level (PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED).

2. **User Roles**: Users are assigned roles that determine their maximum clearance level.

3. **Retrieval Filtering**: When a user queries the RAG system, results are filtered at retrieval time — only documents the user can access are returned.

4. **Audit Logging**: Every access decision (granted or denied) is logged with user, document, and reason.

5. **Deny-by-Default**: Documents without an ACL entry or with a higher access level than the user's role are automatically denied.

## Usage Examples

### Basic Setup

```python
from permission_rag import PermissionRAG, Document, User, AccessLevel, Role

rag = PermissionRAG()

# Add documents with access levels
rag.add_document(Document(
    doc_id="public-faq",
    content="Company FAQ: Office hours are 9-5.",
    access_level=AccessLevel.PUBLIC,
))
rag.add_document(Document(
    doc_id="salary-data",
    content="Employee salary ranges: $50k-$200k",
    access_level=AccessLevel.CONFIDENTIAL,
))
rag.add_document(Document(
    doc_id="api-keys",
    content="Production API key: sk-prod-xxxxx",
    access_level=AccessLevel.RESTRICTED,
))

# Guest user can only see public docs
guest = User(user_id="u1", role=Role.GUEST)
results = rag.retrieve(guest, "company info")
# Only "public-faq" is returned

# Admin can see everything
admin = User(user_id="u2", role=Role.ADMIN)
results = rag.retrieve(admin, "info")
# All three documents are returned
```

### Access Checking

```python
result = rag.check_access(guest, "salary-data")
assert not result.access_granted
print(result.reason)  # "Role guest cannot access confidential documents"
```

### Debug Retrieval (Including Denied)

```python
debug = rag.retrieve_with_denied(employee, "salary data")
print(f"Granted: {len(debug['granted'])}, Denied: {len(debug['denied'])}")
for denied_result in debug['denied']:
    print(f"  Denied: {denied_result.document.doc_id} - {denied_result.reason}")
```

## Limitations

- Keyword-based search is a stand-in; production systems should use vector similarity.
- Does not prevent indirect inference (user deduces confidential info from allowed results).
- Role hierarchy is simplified; real systems may need attribute-based access control (ABAC).
- Should be combined with output validation to prevent the model from revealing authorized information in unauthorized contexts.
