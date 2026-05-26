# Changelog

All notable changes to AI Security from Scratch will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Complete directory structure for all 12 phases (76 classes)
- Phase 1: Foundations — 6 classes with lesson content, control-loop analysis, threat models, labs, and assignments
- Phase 2: Prompt Injection — 6 classes with lesson content, control-loop analysis, threat models, labs, and assignments
- 5 vulnerable lab applications: chatbot, RAG, agent, memory assistant, enterprise capstone
- 7 defense implementations with Python code and pytest tests: context firewall, permission-aware RAG, secure tool gateway, policy engine, output validation, memory quarantine, AI security gateway
- AI security eval harness with YAML attack suites (prompt injection, RAG poisoning, tool abuse, data leakage)
- Control ledger implementation with hash-chained append-only event store
- Observability event schema and sample JSONL events
- Assurance mappings: ISO 27001, NIST AI RMF, OWASP LLM Top 10
- 9 secure architecture pattern documents (context firewall through circuit breaker)
- 7 professional templates (class, lab, threat model, control loop, red-team report, security test, assurance case)
- 10 AI content agent prompt specifications
- Lab validator, report generator, and diagram generator tools
- GitHub Actions workflows for security testing and lesson validation
- GitHub issue templates (new class proposal, bug report) and PR template

### Changed
- Redesigned README with badges, banner, Mermaid diagrams, and collapsible curriculum sections
- Rewrote ROADMAP with visual progress tracker and consistent class tables

## [0.1.0] - 2026-05-27

### Added
- Initial repository structure
- Project manifesto and core philosophy
- Framework documents (6 control-theoretic AI security theory documents)
- Responsible use policy
- Contributing guide with quality gates
- Code of conduct
- MIT License
- Security policy
- Makefile with standard commands
- requirements.txt
