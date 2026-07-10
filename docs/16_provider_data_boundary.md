---
title: Provider Data Boundary (Phase 7E)
slug: provider-data-boundary
category: Architektur
audience: developers
version: "2026-07-10"
order: 16
---

# Provider Data Boundary

**KP-Version:** 1.5.3  
**Contract:** `contracts/provider/provider_data_policy.yaml`  
**ADR:** [ADR-0015](../adr/ADR-0015-provider-data-boundary.md)

## Zweck

Definiert, welche Kontextfelder an **externe LLM-Provider** übertragen werden dürfen — getrennt von der Field Source Policy (welche Quelle ein Feld füllt).

## Pipeline-Position

```
Context Assembly (vollständig, lokal)
        │
        ▼
Provider Gate (Schema, Pflichtfelder, Konflikte)
        │
        ▼
Context Builder (Messages mit Assembly)
        │
        ▼
sanitize_context_for_provider()   ← Phase 7E
        │
        ▼
externer Provider (nur sanitisierte Messages)
```

## Standardregeln

| Kategorie | Provider-Übertragung |
|-----------|---------------------|
| Operative SQL-/CRM-Felder | **Nein** (maskiert/blockiert) |
| Kundennummern, interne IDs | **Nein** (blockiert/pseudonymisiert) |
| Ansprechpartner-/Personendaten | **Nein** |
| Interne Notizen | **Nein** |
| Governance-/Playbook-Regeln | **Ja** |
| Semantische RAG-Inhalte | **Ja** (max. summary) |
| Graph-/Provenienz-Inhalte | **Nein** (maskiert) |
| Unbekannte Felder | **Blockiert** |

## Feldklassen (Auszug)

Siehe Contract für vollständige Liste:

- `operative_sql` — CRM-Status, Segmentierung, Umsatzklasse, …
- `crm_identifier` — Kundennummern
- `contact_personal` — Ansprechpartner
- `internal_notes` — Interne Notizen
- `governance_playbook` — Regeln, No-Auto-Publish
- `semantic_rag` — Abgeleiteter Kontext
- `structural_graph` — Beziehungen, Provenienz

## Local-only SQL Test Mode

**Flag:** `DAR_KP_SQL_LOCAL_ONLY=1`

| Aspekt | Verhalten |
|--------|-----------|
| SQL-Ausführung | Read-only, lokal |
| Context Assembly | Validiert SQL-Ergebnisse |
| Provider-Kontext | Keine SQL-Rohwerte; neutrale `[LOCAL_VALIDATED:field_present]`-Struktur |
| Telemetrie/Memory/Inbox | Keine sensiblen Rohdaten |

Vorbereitung für kontrollierten Test mit echter SQL-Datenbank und ausdrücklich gewählter unkritischer Testfirma — **keine produktive Aktivierung**.

## TLS-Sicherheit

- `verify=False` ist technisch verboten (`provider_tls.py`)
- Zertifikatsfehler → kontrollierter Abbruch (`kp_provider_tls_failed`)
- Kein SSL-Bypass in Test- oder Produktionspfad

## Audit

Die Policy definiert `audit.log_*` Flags. Runtime protokolliert in `kp_meta.provider_sanitization`:

- Anzahl blockierter/maskierter Felder
- Entscheidung (`allow`, `local_only_neutral`, `block_all`)
- Policy-Referenz

## Tests

| Repo | Suite |
|------|-------|
| KP | `tests/test_contract.py` — `test_provider_data_policy_contract` |
| Digiwiz | `tests/test_dar_kp_phase7e_provider_boundary.py` |

## Verwandte Dokumente

- [10_contracts.md](10_contracts.md) — Contract-Übersicht
- [15_dar_app_integration_plan.md](15_dar_app_integration_plan.md) — Phase 7E
- [13_source_resolution.md](13_source_resolution.md) — SQL-first (ADR-0013)
- [12_context_assembly_pipeline.md](12_context_assembly_pipeline.md) — Assembly (ADR-0011)
