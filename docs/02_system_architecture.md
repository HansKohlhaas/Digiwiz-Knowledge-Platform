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
| Knowledge | `knowledge-platform/` | Playbooks, Schemas, ADRs, Runtime-Routing |
| Ausführung | `digiwiki/` | Pipeline, API, Validierung, Inbox |
| Zustand | `data/` | Inbox, Logs, Memory (gitignored) |
| Legacy | `firmenapp/config/` | Fallback bis Deprecation |

## Pfad-Auflösung

`digiwiki/knowledge_paths.py` — Env `DIGIWIZ_KNOWLEDGE_ROOT` oder `knowledge-platform/`.

## Verwandte Dokumente

- [03_knowledge_platform.md](03_knowledge_platform.md)
- [04_ai_runtime.md](04_ai_runtime.md)
- [05_api_strategy.md](05_api_strategy.md)
- `adr/` — verbindliche Entscheidungen
