# Verträge (Contracts) — Übersicht

Die Knowledge Platform ist **kein reines Dokumentations-Repository**, sondern die verbindliche Quelle für **Regeln und Schnittstellen** (ADR-0007).

## Statusmodell

| Begriff | Bedeutung |
|---------|-----------|
| **contract_active** | Schema/Policy in KP vorhanden, versioniert, getestet |
| **app_planned** | Digiwiz App nutzt den Contract noch nicht vollständig |
| **app_active** | Contract wird in der App produktiv konsumiert |

`meta/manifest.yaml` trennt **Contract-Status** und **App-Status** — „Contract aktiv“ heißt nicht „Feature in App fertig“.

## Contract-Katalog

| Typ | Pfad | Maschinenlesbar | Beschreibung |
|-----|------|-----------------|--------------|
| Playbooks | `playbooks/`, `content/playbooks/` | YAML, Markdown | Inhaltsregeln, Brandvoice, Quellen |
| JSON-Schemas | `schemas/` | JSON Schema | Lieferungs-Envelope, Datenmodelle |
| Prompt-Schemas | `schemas/prompts/` | JSON/YAML (geplant) | Kontext- und Prompt-Struktur für DAR |
| API-Verträge | `contracts/api/` | OpenAPI/JSON (geplant) | `/api/v1/*`, `/api/v1/runtime/*` |
| Knowledge Graph | `schemas/knowledge_graph_*.schema.json`, `contracts/graph/` | JSON Schema | Node/Edge + deklarative Queries (ADR-0008) |
| Retrieval-Policy | `contracts/retrieval/` | YAML | Merge Graph↔RAG nach Source Resolution (ADR-0009) |
| Source Resolution | `contracts/source-resolution/` | YAML, JSON Schema | SQL-first, Context Assembly (ADR-0013, ADR-0011) |
| Decision Engine | `contracts/decision-engine/` | YAML, JSON Schema | Orchestrierung Quellen + Schritte (ADR-0014, E4) |
| Runtime | `runtime/` | JSON | Routing, Task→Agent→Modell |
| ADRs | `adr/` | Markdown | Architekturentscheidungen |
| Beispiele | `examples/` | JSON | Gültige und fehlerhafte Instanzen |

## Status v1.5.1

- ✅ Playbooks, Runtime, ADRs, `agent-lieferung.v3.json` — **contract_active / app_active**
- ✅ Source Resolution + Context Assembly (ADR-0013, ADR-0011) — **contract_active / app_planned** (D4/D5)
- ✅ **Decision Engine** (ADR-0014, E4) — **contract_active / app_planned**
- ✅ Graph Query Contract + Beispiele — **contract_active / app_planned** (Stufe E App)
- ✅ Retrieval Merge Policy v1 — **contract_active / app_planned** (Context Builder Merge)
- ✅ Verfahrensdoku in `docs/verfahren/` (menschenlesbar, verweist auf Contracts)
- ⏳ Prompt-Schemas, API-Verträge (OpenAPI) — inkrementell nach Stufe C/D
- ⏳ Graph-Store / Chroma-Rebuild in App — **app_planned** (Contracts in KP ✅)

## Prüfung

```bash
python -m unittest tests.test_contract -v
python -m unittest tests.test_governance -v
```

Details: [docs/10_contracts.md](../docs/10_contracts.md)
