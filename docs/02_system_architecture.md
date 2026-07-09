# Systemarchitektur

```
Externe Agenten / DAR
        │
        ▼
Knowledge Platform (Regeln, Schemas, Playbooks)
        │
        ▼
Digiwiz App (Validierung, Inbox, UI)
        │
        ▼
Regisseur-Inbox → manuelle Freigabe
```

## Komponenten

| Schicht | Ort | Verantwortung |
|---------|-----|---------------|
| **Contracts** | `knowledge-platform/` | Playbooks, Schemas, API-Specs, Runtime-JSON, ADRs |
| Ausführung | `digiwiki/` | Pipeline, API-Implementierung, Validierung, Inbox |
| Zustand | `data/` | Inbox, Logs, Memory (gitignored) |
| Legacy | `firmenapp/config/` | Fallback bis Deprecation |

## Kontext-Schichten (Stufe D/E)

```
Playbooks + Contracts (KP, SSOT)
        │
        ├──► Knowledge Graph (strukturiert, Provenienz)     ← Stufe E, KP-Schema
        │
        └──► Chroma/RAG (semantisch, abgeleitet)            ← App, rebuild-fähig
                  │
                  ▼
        DAR context_builder  →  Validator  →  Regisseur-Inbox
```

**ADR-0008:** Graph = KP-Erweiterung, keine neue Runtime.  
**ADR-0009:** Chroma ist nicht SSOT; Context Builder kombiniert Graph + RAG.

## Pfad-Auflösung

`digiwiki/knowledge_paths.py` — Env `DIGIWIZ_KNOWLEDGE_ROOT` oder `knowledge-platform/`.

## Verwandte Dokumente

- [03_knowledge_platform.md](03_knowledge_platform.md)
- [04_ai_runtime.md](04_ai_runtime.md)
- [05_api_strategy.md](05_api_strategy.md)
- [10_contracts.md](10_contracts.md)
- [11_roadmap_stufen_a_f.md](11_roadmap_stufen_a_f.md)
- [adr/README.md](../adr/README.md) — ADR-Index
