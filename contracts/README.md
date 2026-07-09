# Verträge (Contracts) — Übersicht

Die Knowledge Platform ist **kein reines Dokumentations-Repository**, sondern die verbindliche Quelle für **Regeln und Schnittstellen** (ADR-0007).

## Contract-Katalog

| Typ | Pfad | Maschinenlesbar | Beschreibung |
|-----|------|-----------------|--------------|
| Playbooks | `playbooks/`, `content/playbooks/` | YAML, Markdown | Inhaltsregeln, Brandvoice, Quellen |
| JSON-Schemas | `schemas/` | JSON Schema | Lieferungs-Envelope, Datenmodelle |
| Prompt-Schemas | `schemas/prompts/` | JSON/YAML (geplant) | Kontext- und Prompt-Struktur für DAR |
| API-Verträge | `contracts/api/` | OpenAPI/JSON (geplant) | `/api/v1/*`, `/api/v1/runtime/*` |
| Knowledge Graph | `schemas/graph/`, `contracts/graph/` | JSON (geplant) | DAR Context Builder (ADR-0008) |
| Retrieval-Policy | `contracts/retrieval/` | YAML/JSON (geplant) | Merge Graph↔RAG nach Source Resolution (ADR-0009) |
| Source Resolution | `contracts/source-resolution/` | YAML | SQL-first, Auflösungssequenz (ADR-0013) |
| Runtime | `runtime/` | JSON | Routing, Task→Agent→Modell |
| ADRs | `adr/` | Markdown | Architekturentscheidungen |
| Beispiele | `examples/` | JSON | Gültige und fehlerhafte Instanzen |

## Status v1.2.0

- ✅ Playbooks, Runtime, ADRs, `agent-lieferung.v3.json`
- ✅ Source Resolution Policy (ADR-0013) — `contracts/source-resolution/`
- ✅ Verfahrensdoku in `docs/verfahren/` (menschenlesbar, verweist auf Contracts)
- ⏳ Prompt-Schemas, API-Verträge (OpenAPI) — inkrementell nach Stufe C/D
- ⏳ Knowledge Graph (Stufe E) — [ADR-0008](../adr/ADR-0008-knowledge-graph-as-platform-extension.md)
- ⏳ Retrieval Merge Graph↔RAG — [ADR-0009](../adr/ADR-0009-knowledge-graph-and-chroma-rag.md) (kein Chroma in KP)

## Prüfung

```bash
python -m unittest tests.test_contract -v
```

Details: [docs/10_contracts.md](../docs/10_contracts.md)
