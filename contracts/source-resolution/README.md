# Source Resolution — Contracts

Verbindliche **Auflösungssequenz** für Wissensabfragen: SQL-first bei CRM-/Stammdaten, danach KP → Graph → Chroma → Web.

**ADR:** [ADR-0013](../../adr/ADR-0013-source-resolution-and-sql-first-policy.md)  
**Doku:** [docs/13_source_resolution.md](../../docs/13_source_resolution.md)

## Artefakte

| Datei | Status | Beschreibung |
|-------|--------|--------------|
| `source_resolution_policy.yaml` | ✅ Contract v1 | Domänen, Sequenz, Konfliktregeln |
| `../retrieval/merge_policy.yaml` | ⏳ geplant | Merge Graph↔RAG **nach** Source Resolution |

## Abgrenzung

| Ordner | Verantwortung |
|--------|---------------|
| **`source-resolution/`** | **Welche Quelle zuerst?** SQL-first, Klassifikation, Konflikt SQL vs. Index |
| **`retrieval/`** | **Wie mergen?** Token-Limits, Passagen-Priorität Graph↔RAG (wenn Schritt 3–4) |
| **`graph/`** | Deklarative Graph-Abfragen (Stufe E) |

## App (Digiwiz, geplant)

- `source_resolution_router` — Klassifikation Schritt 0
- `crm/sql_query_adapter` — read-only SQL/CRM (kein Contract in KP — App-Implementierung)
- `context_builder` — konsumiert Policy aus KP

**Keine SQL-Implementierung in der Knowledge Platform.**
