# Decizii de arhitectură (ADR)

Un ADR (Architecture Decision Record) documentează pe scurt o decizie importantă:
- contextul;
- opțiunile analizate;
- decizia luată;
- consecințele ei.

**Statusuri posibile:** `Propus` → `Acceptat` (sau `Respins`) → eventual `Înlocuit de ADR-xxx`.

**Reguli:**
- **Un ADR nou** se adaugă prin PR, copiind [ADR-000-template.md](ADR-000-template.md) cu următorul număr liber.
- **M aprobă** ADR-urile. **Proprietarul** deciziei le finalizează: completează analiza și schimbă statusul.
- **Un ADR acceptat nu se rescrie.** Dacă decizia se schimbă, se scrie un ADR nou care îl înlocuiește.

| ADR | Titlu | Status | Proprietar | Termen |
|---|---|---|---|---|
| [ADR-001](ADR-001-bid-concurrency.md) | Concurența la plasarea ofertelor: `FOR UPDATE` vs. `@Version` | Propus | M | S2 (06.12.2026) |
| [ADR-002](ADR-002-gateway-auth-internal-key.md) | Autentificare la gateway + cheie internă între servicii | Propus | D | S1 (22.11.2026) |
| [ADR-003](ADR-003-rest-clients-stub-profile.md) | Clienți REST (`RestClient` / `@HttpExchange`) și profilul `stub` | Propus | M | S1 (22.11.2026) |
| [ADR-004](ADR-004-database-per-service.md) | Database-per-service pe o singură instanță MySQL | Propus | K | S1 (22.11.2026) |
| ADR-005 | Alegerea platformei cloud | de scris | R | S2 (06.12.2026) |
