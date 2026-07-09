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
[0] Source Resolution — SQL-first? (ADR-0013)
        │
        ▼
Playbooks + Contracts (KP, SSOT für Regeln)
        │
        ├──► SQL / CRM (Firmendaten, SSOT operativ)
        │
        ├──► Knowledge Graph (strukturiert, Provenienz)     ← Stufe E
        │
        └──► Chroma/RAG (semantisch, abgeleitet)            ← App
                  │
                  ▼
        DAR context_builder  →  Validator  →  Regisseur-Inbox
```

**ADR-0008:** Graph = KP-Erweiterung, keine neue Runtime.  
**ADR-0009:** Chroma ist nicht SSOT.  
**ADR-0013:** SQL ist SSOT für Firmendaten; Klassifikation vor Graph/RAG.

## Pfad-Auflösung

`digiwiki/knowledge_paths.py` — Env `DIGIWIZ_KNOWLEDGE_ROOT` oder `knowledge-platform/`.

## Verwandte Dokumente

- [03_knowledge_platform.md](03_knowledge_platform.md)
- [04_ai_runtime.md](04_ai_runtime.md)
- [05_api_strategy.md](05_api_strategy.md)
- [10_contracts.md](10_contracts.md)
- [11_roadmap_stufen_a_f.md](11_roadmap_stufen_a_f.md)
- [13_source_resolution.md](13_source_resolution.md)
- [adr/README.md](../adr/README.md) — ADR-Index
