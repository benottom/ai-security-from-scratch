# Security Policy

## Reporting Security Vulnerabilities

We take security seriously — both in the AI systems this curriculum teaches you to protect and in the project itself. If you find a security issue, we want to hear about it.

### Vulnerabilities in Course Content

If you discover an error in the curriculum that could lead to insecure practices — for example, a defense that does not actually stop the attack it claims to stop, or a recommended configuration that introduces a vulnerability — please report it so we can correct the content.

- **Email**: security@ai-security-from-scratch.dev
- **Subject line**: [Content Security] Brief description of the issue
- **Include**: The class number, the specific section, and a description of why the content is incorrect or misleading. If possible, include a corrected version or a proof that the defense fails.

Content security issues are treated as high priority because incorrect security guidance is worse than no guidance.

### Vulnerabilities in Lab Code

If you discover a security vulnerability in the lab code that goes beyond the intentionally vulnerable design — for example, a path traversal in the lab server, a dependency with a known CVE, or a way to escape the lab environment — please report it.

- **Email**: security@ai-security-from-scratch.dev
- **Subject line**: [Lab Security] Brief description of the issue
- **Include**: The affected component, steps to reproduce, and the impact of the vulnerability. Do not include proof-of-concept exploits in the initial report; we will request them if needed.

### Vulnerabilities Not in This Project

If you discover a vulnerability in an AI system that is not part of this project, follow that system's responsible disclosure process. Do not report third-party vulnerabilities to us unless they directly affect this project's code or infrastructure.

---

## Safe Harbor for Security Researchers

We support responsible security research. If you act in good faith to identify and report a vulnerability in this project, we consider your research to be authorized conduct.

Specifically:

- We will not pursue legal action against researchers who follow this policy and act in good faith.
- We will not seek law enforcement action or file legal complaints against researchers who discover and report vulnerabilities through the channels described in this document.
- We ask that you avoid accessing or modifying data that does not belong to you, degrading the availability of our services, or causing harm to other users.
- We ask that you give us a reasonable amount of time to address the issue before any public disclosure.

This safe harbor applies only to research conducted on this project's code and infrastructure. It does not extend to third-party systems, services, or organizations referenced in the curriculum.

---

## Response Timeline

When you report a security issue, we commit to the following timeline:

| Milestone | Target |
|-----------|--------|
| Acknowledgment of receipt | Within 48 hours |
| Initial assessment and triage | Within 5 business days |
| Status update to reporter | Within 10 business days |
| Resolution or mitigation plan | Within 30 calendar days |
| Public disclosure (if applicable) | After fix is released and reporter is notified |

If we need more time — for example, because the fix requires significant changes or coordination with dependencies — we will communicate the delay and provide a revised timeline.

We ask that reporters give us 90 days from the initial report before publicly disclosing the vulnerability. If we have not addressed the issue within 90 days, the reporter is free to disclose publicly. We prefer coordinated disclosure and will make every effort to meet this timeline.

---

## What We Consider Security Issues

**We want to hear about:**
- Defenses in the curriculum that fail to stop their documented attacks
- Security guidance that is factually incorrect or misleading
- Vulnerabilities in lab code beyond the intentional weaknesses
- Dependency vulnerabilities with known CVEs
- Path traversal, injection, or escape vulnerabilities in lab infrastructure
- Credentials, API keys, or secrets accidentally committed to the repository

**We do not consider security issues:**
- The intentionally vulnerable lab systems (that is the point of the curriculum)
- Attacks that are already documented in the curriculum as learning exercises
- Theoretical attacks without a working proof of concept
- Feature requests for new attack or defense content (open a discussion instead)
- Denial of service against our GitHub infrastructure

---

## Contact

- **General security inquiries**: security@ai-security-from-scratch.dev
- **Encrypted communication**: PGP key available at https://ai-security-from-scratch.dev/.well-known/pgp-key.txt
- **Project maintainers**: Listed in the CODEOWNERS file in the repository

---

Thank you for helping keep this project and its learners secure. Every report makes the curriculum more accurate and the AI systems built by our learners more robust.
