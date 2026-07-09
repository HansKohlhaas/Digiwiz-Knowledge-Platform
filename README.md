# Digiwiz Knowledge Platform

Zentrale, versionierte **Wissens- und Regel-Architektur** für Digiwiz — keine Produktiv-Runtime.

## Rolle

| Dieses Repo | Digiwiz App (`digiwiki/`, `firmenapp/`) |
|-------------|----------------------------------------|
| Playbooks (YAML + Markdown) | Ausführung, UI, Inbox |
| Schemas, Examples | Import, Validierung (Code) |
| Runtime-Routing (JSON) | `ai_runtime/` Pipeline |
| ADRs, Verfahren | Betrieb, Streamlit, CRM |

**Prinzip:** KI bereitet vor → **Regisseur-Inbox** → Hans gibt frei → **keine Auto-Veröffentlichung**.

## Stufenmodell

| Stufe | Inhalt | Ort |
|-------|--------|-----|
| A | Knowledge Layer | `playbooks/`, `content/` |
| B | Qualitätssicherung | `schemas/`, `docs/verfahren/` |
| C | CLI/API | dokumentiert, Code in App |
| D | AI Runtime | `runtime/`, Code in App |
| E | Knowledge Graph | **nächste Phase** — nur hier |
| F | Autonome Agenten | Roadmap |

## Schnellstart

1. Lesen: [00_START_HERE.md](00_START_HERE.md)
2. ADRs: [adr/](adr/)
3. Playbooks: [playbooks/](playbooks/)
4. App-Einbindung: `digiwiki/knowledge_paths.py` + `digiwiki/knowledge_lock.json`

## Version

Siehe [VERSION](VERSION) und [CHANGELOG.md](CHANGELOG.md).

## Next Actions

1. ~~Migration Playbooks/Schemas aus Digiwiz-Monorepo~~ (v1.0.0)
2. Contract-Tests in `tests/` erweitern
3. Regeln aus Python nach `quality/` extrahieren (inkrementell)
4. **Stufe E — Knowledge Graph** (nach Freigabe, nicht parallel)

## Einbindung in Digiwiz App

```env
# Optional — Default: <monorepo>/knowledge-platform
DIGIWIZ_KNOWLEDGE_ROOT=C:\Pfad\zu\knowledge-platform
```

Ohne Env-Variable nutzt die App automatisch `knowledge-platform/` neben `digiwiki/`, mit Fallback auf Legacy-Pfade unter `firmenapp/config/`.
