# SECURITY.md — Security Architecture

> Last updated: 2026-09-25
> Status: Draft — threat model not validated

---

## 1. Security Principles

1. Defense in depth — multiple security layers
2. Least privilege — minimal permissions by default
3. Secrets never in code — environment variables only
4. Fail secure — deny by default on errors
5. Audit everything — log all security-relevant events

---

## 2. Threat Model

`[ASSUMPTION]` Preliminary threats based on system nature.

### 2.1 Attack Surface

| Surface | Threats | Status |
|---|---|---|
| REST API | Injection, DoS, unauthorized access | `[RISK]` |
| LLM prompts | Prompt injection, data exfiltration via LLM | `[RISK]` |
| External API keys | Credential theft, abuse of provider APIs | `[RISK]` |
| Downloaded data | Malicious payloads in raster files | `[RISK]` |
| User queries | PII in queries sent to external LLMs | `[RISK]` |
| Dependencies | Supply chain attacks via PyPI packages | `[RISK]` |

### 2.2 STRIDE Analysis

`[OPEN QUESTION]` Full STRIDE analysis needed.

| Threat | Category | Component | Mitigation |
|---|---|---|---|
| User impersonation | Spoofing | API | Auth `[OPEN QUESTION]` |
| Query logs modified | Tampering | Storage | Immutable audit log |
| Deny data access | Repudiation | API | Request logging |
| Leaked API keys | Info Disclosure | Config | Secret management |
| Crash via bad GeoTIFF | DoS | Processing | Input validation |
| Admin access to all data | Elev. of Privilege | API | RBAC `[OPEN QUESTION]` |

---

## 3. Authentication & Authorization

`[OPEN QUESTION]` Strategy not decided.

| Aspect | Options | Status |
|---|---|---|
| Authentication method | API key / OAuth2 / None | `[OPEN QUESTION]` |
| User model | Anonymous / registered / both | `[OPEN QUESTION]` |
| Authorization model | None / RBAC / ABAC | `[OPEN QUESTION]` |
| Session management | Stateless JWT / server sessions | `[OPEN QUESTION]` |

---

## 4. LLM Security

| Concern | Mitigation | Status |
|---|---|---|
| Prompt injection | Input sanitization + system prompt hardening | `[ASSUMPTION]` |
| Data exfiltration | Don't include sensitive data in LLM context | `[ASSUMPTION]` |
| PII in queries | Redact PII before sending to external LLM | `[OPEN QUESTION]` |
| Output validation | Validate LLM responses against schema | `[ASSUMPTION]` |
| Model poisoning | Use trusted model providers only | `[ASSUMPTION]` |

---

## 5. Data Security

| Concern | Approach | Status |
|---|---|---|
| Data at rest | Disk encryption `[OPEN QUESTION]` | Not specified |
| Data in transit | TLS 1.3 for all connections | `[ASSUMPTION]` |
| API key storage | Encrypted secrets store | `[ASSUMPTION]` |
| User query storage | Retention policy `[OPEN QUESTION]` | Not specified |
| Downloaded imagery | Integrity verification via checksums | `[ASSUMPTION]` |

---

## 6. Dependency Security

- Pin all dependency versions
- Use `pip-audit` or `safety` for vulnerability scanning
- Renovate / Dependabot for automated updates
- Minimal dependency surface — avoid unnecessary packages

---

## 7. Input Validation

| Input | Validation | Status |
|---|---|---|
| Natural language queries | Max length, character filtering | `[ASSUMPTION]` |
| Bounding boxes | Valid coordinate ranges | `[ASSUMPTION]` |
| Date ranges | Valid ISO 8601, reasonable range | `[ASSUMPTION]` |
| File uploads | `[OPEN QUESTION]` — are file uploads in scope? | Not specified |
| GeoTIFF files | GDAL validation before processing | `[ASSUMPTION]` |

---

## 8. Security Testing

See also `TESTING.md`.

| Test Type | Tool | Frequency | Status |
|---|---|---|---|
| SAST | Bandit, Semgrep | Every PR | `[ASSUMPTION]` |
| Dependency audit | pip-audit | Every PR | `[ASSUMPTION]` |
| API fuzzing | `[OPEN QUESTION]` | `[OPEN QUESTION]` | Not specified |
| Penetration testing | `[OPEN QUESTION]` | Pre-release | Not specified |
| Prompt injection tests | Custom test suite | Every AI change | `[ASSUMPTION]` |

---

## 9. Incident Response

`[OPEN QUESTION]` No incident response plan defined.

Minimum needed:
- Security contact / reporting method
- Vulnerability disclosure policy
- Response timeline commitments

---

## Related Documents

- Architecture → [ARCHITECTURE.md](ARCHITECTURE.md)
- AI security concerns → [AI_SYSTEM.md](AI_SYSTEM.md)
- Testing → [TESTING.md](TESTING.md)
