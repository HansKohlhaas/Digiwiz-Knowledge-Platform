# Cursor — Implementierungsleitfaden

## Arbeitsweise

1. **Analysieren, dann implementieren** — Architekturentscheidungen als ADR in `adr/`
2. **Keine Breaking Changes** — Digiwiz App behält Legacy-Fallbacks
3. **Regisseur-Inbox** bleibt Freigabe-Hub (ADR-0002, ADR-0004)
4. **Stufe E — Knowledge Graph** — [ADR-0008](adr/ADR-0008-knowledge-graph-as-platform-extension.md); KP-Erweiterung, keine neue Runtime

## Repo-Grenzen

| Knowledge Platform | Digiwiz App |
|-------------------|-------------|
| `playbooks/`, `schemas/`, `runtime/` | `digiwiki/ai_runtime/`, `agent_*.py` |
| ADRs, Verfahren | UI, Inbox, `data/` |

**Lose Kopplung:** kein Git-Submodule (ADR-0006). Nur `DIGIWIZ_KNOWLEDGE_ROOT` + Contract-Schnittstelle.

## Pfad-Auflösung (App)

```python
from knowledge_paths import knowledge_root, playbooks_dir, agent_lieferung_schema_pfad
```

Env: `DIGIWIZ_KNOWLEDGE_ROOT` (optional)

## Stufen A–D (abgeschlossen in App)

- **A:** Knowledge Layer — Playbooks, Import, Inbox
- **B:** QS — Schema v3, URL/Dublette/Brandvoice
- **C:** CLI `digiwiz-agent`, REST `/api/v1/*`
- **D:** AI Runtime `/api/v1/runtime/*`

Details: `docs/verfahren/` und `cursor/CURSOR_TASK_STAGE_*.md`

## Nächste Aufgabe

**Stufe E — Knowledge Graph** — nur in diesem Repo, nach Freigabe.
