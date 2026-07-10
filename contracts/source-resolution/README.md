# Source Resolution — Contracts

Verbindliche **Auflösungssequenz** für Wissensabfragen: SQL-first bei CRM-/Stammdaten, danach KP → Graph → Chroma → Web.

**ADR:** [ADR-0013](../../adr/ADR-0013-source-resolution-and-sql-first-policy.md)  
**Context Assembly:** [ADR-0011](../../adr/ADR-0011-context-builder-combines-context-layers.md) · [context_assembly.schema.json](context_assembly.schema.json)  
**Doku:** [docs/13_source_resolution.md](../../docs/13_source_resolution.md) · [docs/12_context_assembly_pipeline.md](../../docs/12_context_assembly_pipeline.md)

## Artefakte

| Datei | Status | Beschreibung |
|-------|--------|--------------|
| `source_resolution_policy.yaml` | ✅ Contract v1 | Domänen, Sequenz, Konfliktregeln (ADR-0013) |
| `field_source_policy.yaml` | ✅ Contract v1 | Kanonische Quelle je `field_id`, erlaubte Ergänzungen, verbotene Ersatzquellen, Redaction-Metadaten |
| `context_assembly.schema.json` | ✅ Contract v1 | Context-Array, Pflichtfelder, Assembly (ADR-0011) |
| `../retrieval/merge_policy.yaml` | ⏳ geplant | Merge Graph↔RAG **nach** Source Resolution |

## Abgrenzung

| Ordner | Verantwortung |
|--------|---------------|
| **`source-resolution/`** | **Welche Quelle zuerst?** SQL-first, Klassifikation, Konflikt SQL vs. Index |
| **`retrieval/`** | **Wie mergen?** Token-Limits, Passagen-Priorität Graph↔RAG (wenn Schritt 3–4) |
| **`graph/`** | Deklarative Graph-Abfragen (Stufe E) |

## App (Digiwiz, geplant)

- `source_resolution_router` — Klassifikation Schritt 0 (ADR-0013)
- `context_assembly_pipeline` — Context-Array vor Antwort (ADR-0011)
- `crm/sql_query_adapter` — read-only SQL/CRM (App)
- `context_builder` — Provider-Messages aus Assembly-Output

**Keine SQL-Implementierung in der Knowledge Platform.**
