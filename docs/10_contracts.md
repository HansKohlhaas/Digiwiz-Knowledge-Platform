# Verträge (Contracts)

Die Knowledge Platform definiert **verbindliche Schnittstellen** zwischen Wissen, App und externen Agenten (ADR-0007).

## Contract-Typen

### 1. Playbooks

- **Format:** YAML (`playbooks/`) + Langtext (`content/playbooks/`)
- **Verbraucher:** `agent_playbooks.py`, `ai_runtime/playbook_loader.py`, externe Agenten
- **Änderung:** Version im Playbook-YAML, Changelog in KP

### 2. JSON-Schemas

- **Format:** JSON Schema Draft 2020-12
- **Beispiel:** `schemas/agent-lieferung.v3.json`
- **Verbraucher:** `agent_lieferung_validierung.py` (Logik in App, Schema in KP)
- **Beispiele:** `examples/presseschau/`

### 3. Prompt-Schemas (geplant)

- **Format:** JSON/YAML unter `schemas/prompts/`
- **Zweck:** Einheitliche Prompt- und Kontext-Struktur für DAR
- **Status:** Stufe D/E

### 4. API-Verträge (geplant)

- **Format:** OpenAPI 3.x unter `contracts/api/`
- **Zweck:** REST-Stufe C/D — Request, Response, Auth, Fehlercodes
- **Status:** Verfahrensdoku existiert; OpenAPI folgt

### 5. Runtime-Konfiguration

- **Format:** JSON (`runtime/routing.json`)
- **Verbraucher:** `ai_runtime/routing_engine.py`
- **Hinweis:** Konfiguration, keine Pipeline-Ausführung

### 6. ADRs

- **Format:** Markdown (`adr/`)
- **Zweck:** Architektur- und Prozessentscheidungen

### 7. Knowledge Graph (Stufe E, geplant)

- **Format:** `schemas/graph/`, `contracts/graph/`, `examples/graph/`
- **Zweck:** Entitäten, Beziehungen, Provenienz — strukturierter Kontext für DAR
- **Status:** [ADR-0008](../adr/ADR-0008-knowledge-graph-as-platform-extension.md) — KP-Erweiterung, keine neue Runtime

### 8. Retrieval-Policy (Stufe E, geplant)

- **Format:** `contracts/retrieval/`
- **Zweck:** Merge-Regeln Graph ↔ Chroma/RAG im Context Builder; Limits, Provenienz
- **Status:** [ADR-0009](../adr/ADR-0009-knowledge-graph-and-chroma-rag.md) — **keine** Chroma-DB in KP; Index bleibt abgeleitet in App

### 9. Runtime- und Context-Contracts (Stufe D/E)

| Schema | Pfad | Zweck |
|--------|------|--------|
| Runtime-Output | `schemas/runtime_output.schema.json` | DAR-Task-Ausgabe (kein `published_url`) |
| API-Fehler | `schemas/api_error.schema.json` | Einheitliches Fehler-Envelope |
| Context Builder Input/Output | `schemas/context_builder_*.schema.json` | Kontext-Merge (ADR-0011) |
| Knowledge Graph Node/Edge | `schemas/knowledge_graph_*.schema.json` | Stufe E Struktur + Provenienz |
| Chroma Manifest / Rebuild | `schemas/chroma_*.schema.json` | Abgeleiteter Index, rebuild-fähig |
| Playbook-Governance | `schemas/playbook.schema.json` | `owner`, `auto_publish: false`, … |
| LinkedIn-Vorschlag | `schemas/linkedin.schema.json` | Beispiel: `examples/linkedin/` |

### 10. Source Resolution & Context Assembly (Stufe D/E, v1.2.0+)

| Artefakt | Pfad | Zweck |
|----------|------|--------|
| Source Resolution Policy | `contracts/source-resolution/source_resolution_policy.yaml` | SQL-first, Sequenz (ADR-0013) |
| **Context Assembly** | `contracts/source-resolution/context_assembly.schema.json` | Context-Array, Pflichtfelder (ADR-0011) |
| Doku Assembly | `docs/12_context_assembly_pipeline.md` | 10-Schritte-Pipeline |
| Doku Resolution | `docs/13_source_resolution.md` | Quellenreihenfolge, Konflikte |
| Beispiele | `examples/source-resolution/` | SQL-first, RAG, Graph, Assembly |

## Workflow: Contract first

```
1. Vertrag in KP definieren (Schema, Beispiel, ADR bei Bedarf)
2. Contract-Test in tests/
3. App implementiert / lädt über knowledge_paths.py
4. Integrations-Test in digiwiki/tests/
5. VERSION + knowledge_lock.json anheben
```

## Keine Breaking Changes

Neue Contract-Versionen (z. B. Schema v4) parallel zu Legacy; App-Fallback bis Deprecation.

Siehe auch: [03_knowledge_platform.md](03_knowledge_platform.md), [contracts/README.md](../contracts/README.md)
