# Responsible Use Policy

## Purpose

AI Security from Scratch teaches offensive security techniques in a controlled, educational context. The purpose of this curriculum is threefold:

1. **Defensive education** — To train engineers, researchers, and practitioners to understand AI security threats so they can build more secure systems.
2. **Secure engineering** — To equip practitioners with the skills to design, implement, test, and verify security controls for AI systems.
3. **Controlled research** — To advance the state of AI security knowledge through reproducible, ethically conducted experimentation in isolated lab environments.

This project exists to make AI systems safer. Any use of this material that makes AI systems less safe is a misuse of this project.

---

## Explicit Prohibitions

The following uses of this curriculum and its materials are strictly prohibited:

### No Attacking Real Systems
You must not use the techniques taught in this curriculum against any system you do not own or do not have explicit, documented authorization to test. This includes production AI services, third-party APIs, public-facing chatbots, and any system operated by another organization or individual.

### No Credential Theft or Fraud
You must not use techniques from this curriculum to extract credentials, personal information, financial data, or any other sensitive information from systems or users. This includes techniques that bypass access controls to obtain unauthorized data.

### No Malware or Weaponized Tools
You must not use the code or techniques in this curriculum to create malware, ransomware, or automated attack tools designed for use against third-party systems. Lab code is for learning and testing, not for deployment as attack infrastructure.

### No Evasion of Security Controls
You must not use techniques from this curriculum to evade security controls on systems you do not own. Learning how controls fail is the purpose; bypassing controls you do not maintain is not.

### No Harassment or Targeting
You must not use the techniques in this curriculum to harass, intimidate, or target individuals. This includes social engineering attacks, impersonation, or any technique used to cause harm to a person rather than to improve a system.

---

## Lab Safety Requirements

All exercises in this curriculum must be performed in the provided lab environments or in environments you fully control. The lab environments are designed to be:

- **Isolated** — No connection to production systems or external services without explicit configuration.
- **Containable** — All changes are local to the lab and can be reset.
- **Observable** — All activity is logged for learning and review purposes.

Before running any attack exercise:

1. Verify you are in the lab environment. Attack code includes environment checks that will refuse to run outside the lab.
2. Ensure no network connections route to production systems or external APIs you do not control.
3. Do not modify lab code to remove safety checks or environment validation.
4. If you discover that a lab exercise can affect external systems, stop immediately and report it as a security issue.

---

## Responsible Disclosure

If you discover a new vulnerability while studying this curriculum:

1. **Do not exploit it.** Document what you found without expanding the attack surface.
2. **Report it to the vendor** through their responsible disclosure program or security contact. Give them a reasonable timeframe (typically 90 days) to respond before any public discussion.
3. **Report it to this project** by emailing security@ai-security-from-scratch.dev so we can update the curriculum if appropriate.
4. **Do not publish zero-day exploits** as part of this curriculum or in project discussions. We include only publicly known vulnerabilities that vendors have had time to address.
5. **Coordinate disclosure timing** with the vendor. Public discussion should follow, not precede, the vendor's patch release.

We commit to acknowledging responsible disclosures in the curriculum and recognizing the contribution publicly if the reporter wishes.

---

## Dual-Use Acknowledgment

We recognize that security knowledge is dual-use: the same techniques that help defenders understand threats can help attackers exploit them. We have made the following decisions to manage this tension:

- **Open by default.** We do not rely on secrecy for security. The attacks we teach are already publicly known. Obscurity is not a security control.
- **Defensive framing.** Every attack is paired with a defense. The curriculum structure ensures you cannot study an attack without also studying how to prevent it.
- **Engineering rigor.** We emphasize the engineering discipline of building, testing, and verifying controls — not the spectacle of breaking things.
- **No novel exploits.** We do not include zero-day exploits or previously undisclosed vulnerabilities. Our contribution is pedagogical, not adversarial.

We believe that informed defenders are more effective than uninformed ones. The risk of teaching offensive techniques is real, but the risk of leaving defenders unprepared is greater.

---

## Legal Considerations

- **Computer fraud laws** — Many jurisdictions have laws (e.g., the U.S. Computer Fraud and Abuse Act, the UK Computer Misuse Act) that criminalize unauthorized access to computer systems. Ensure your testing activities comply with all applicable laws.
- **Authorized testing** — Always obtain written authorization before testing any system you do not own. Verbal permission is insufficient.
- **Scope boundaries** — Stay within the scope of any authorization you receive. Finding a vulnerability is not license to explore further.
- **Data handling** — If you inadvertently access data you are not authorized to see during testing, stop immediately, do not copy or retain the data, and report the incident.
- **Export controls** — Some jurisdictions restrict the export of security tools or techniques. Be aware of the regulations that apply to your location and the locations of anyone you share materials with.

This policy does not constitute legal advice. Consult a qualified attorney for legal questions related to your specific circumstances.

---

## Reporting Violations

If you become aware of someone misusing the materials in this curriculum:

1. **Report it** to security@ai-security-from-scratch.dev with as much detail as you can provide.
2. **Do not confront the individual.** Let the project maintainers and, if necessary, law enforcement handle the situation.
3. **Document what you observed** — dates, platforms, specific misuse, and any available evidence.
4. **Maintain confidentiality** — Do not publicize the violation until the maintainers have had time to assess and respond.

The project maintainers will investigate all reports and take appropriate action, which may include:

- Contacting the individual and requesting they cease the misuse.
- Removing the individual from project community spaces.
- Reporting the violation to relevant authorities if the misuse involves illegal activity.
- Updating the curriculum or lab environments to prevent similar misuse.

We take misuse of this project seriously. The purpose is defensive education. Any use that undermines that purpose harms the project and the community it serves.

---

*This policy is a living document. If you have suggestions for improvement, open a discussion or submit a PR. We welcome input from security researchers, legal experts, educators, and the broader community.*
