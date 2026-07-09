# Knowledge Platform — Rolle und Grenzen

Dieses Repository ist die **verbindliche Contract-Quelle** (ADR-0007) — nicht nur Dokumentation.

## Contract-Artefakte

| Typ | Pfad | Status |
|-----|------|--------|
| Playbooks | `playbooks/`, `content/playbooks/` | ✅ aktiv |
| JSON-Schemas | `schemas/` | ✅ aktiv |
| Prompt-Schemas | `schemas/prompts/` | ⏳ geplant |
| API-Verträge | `contracts/api/` | ⏳ geplant |
| Knowledge Graph | `schemas/graph/`, `contracts/graph/` | ⏳ geplant (ADR-0008) |
| Retrieval-Policy | `contracts/retrieval/` | ⏳ geplant (ADR-0009, Chroma in App) |
| Runtime-Konfiguration | `runtime/` | ✅ aktiv |
| ADRs | `adr/` | ✅ aktiv |
| Beispiele | `examples/` | ✅ aktiv |

Menschenlesbare Verfahren: `docs/verfahren/` (verweisen auf Contracts).

**Nicht enthalten:** Python-Runtime, Streamlit-UI, Provider-Code, `data/`.

Binding zur App: `digiwiki/knowledge_paths.py`, Env `DIGIWIZ_KNOWLEDGE_ROOT`.

Siehe [10_contracts.md](10_contracts.md), [adr/README.md](../adr/README.md), ADR-0003, ADR-0005, ADR-0007, ADR-0009.
