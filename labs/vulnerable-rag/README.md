# Vulnerable RAG Lab

> **⚠️ FOR EDUCATIONAL USE ONLY** — This application is deliberately insecure. Never deploy it in production or expose it to the public internet.

## Overview

A minimal Retrieval-Augmented Generation (RAG) system designed to be vulnerable to document-poisoning, access-bypass, and indirect-injection attacks. It uses ChromaDB for local vector storage and a simple TF-IDF-style retrieval approach. No API keys required.

## Vulnerabilities

| # | Vulnerability | Description |
|---|--------------|-------------|
| 1 | **No access control** | All documents retrieved regardless of user role. `user_role` is accepted but ignored. |
| 2 | **No source validation** | Retrieved document content is trusted blindly and injected into the LLM prompt. |
| 3 | **No content filtering** | No scanning of retrieved text for injection payloads or sensitive markers. |
| 4 | **Metadata not enforced** | Access-level metadata is stored in ChromaDB but never used for filtering. |
| 5 | **User-controlled result count** | `n_results` is caller-specified, allowing retrieval of the entire database. |
| 6 | **Document count exposed** | `/documents/count` leaks the total number of documents. |
| 7 | **No ingestion validation** | Any document (including poisoned ones) can be ingested without review. |

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Ingest sample documents (including confidential ones)
python ingest.py

# To also add a poisoned document:
python ingest.py --add-poison

# Run the server
python app.py
```

The server starts at `http://localhost:8001`.

## Sample Documents

| File | Access Level | Content |
|------|-------------|---------|
| `public_faq.txt` | Public | Office hours, dress code, IT contact |
| `hr_policy.txt` | Confidential | Salary bands, layoff policy, PIP details |
| `financial_report.txt` | Restricted | Revenue, acquisition plans, layoffs |

## API

### POST /ask

```json
{
  "question": "What are the company office hours?",
  "n_results": 5,
  "user_role": "employee"
}
```

Response:

```json
{
  "answer": "Based on the retrieved documents...",
  "sources": ["public_faq.txt"],
  "total_documents_searched": 3
}
```

### GET /documents/count

Returns `{"count": 3}`.

## Attack Exercises

1. **Confidential data access** — Ask: `"What are the salary bands?"` (retrieves HR policy regardless of your role)
2. **Financial data extraction** — Ask: `"What acquisitions are planned?"` (retrieves restricted financial report)
3. **Poisoned document injection** — Run `python ingest.py --add-poison`, then ask about benefits
4. **Indirect prompt injection** — Craft a document with embedded instructions and ingest it
5. **Database enumeration** — Use `n_results=100` and `/documents/count` to map the knowledge base

## Control-Loop Analysis

```
┌──────────┐  question  ┌───────────┐  query  ┌──────────┐  results  ┌──────┐
│  User    │───────────▶│  Retriever│────────▶│ ChromaDB │─────────▶│ LLM  │
└──────────┘            └───────────┘         └──────────┘          └──────┘
                              │                     ▲                   │
                              │  no access filter   │ poisoned docs     │
                              └─────────────────────┴───────────┐      │
                                                              injected│
                                                              context │
                                                                      ▼
                                                              ┌──────────┐
                                                              │  Output  │──▶ User
                                                              └──────────┘
                                                               no filter
```

Missing controls: access-control filter, source validation, content scanning, result-count limits.

## Learning Objectives

- Explain why RAG systems need access-control enforcement at the retrieval layer
- Demonstrate how poisoned documents can hijack LLM behaviour
- Construct indirect prompt-injection payloads through document content
- Design a retrieval filter that enforces document-level permissions
