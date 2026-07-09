# AI Runtime (Stufe D) — Dokumentation

Die **Ausführung** liegt in `digiwiki/ai_runtime/`. Dieses Repo enthält nur die **Routing-Konfiguration**:

- `runtime/routing.json` — Task → Agent, Modell, Playbooks

REST-Endpunkte: `/api/v1/runtime/*` (siehe `docs/verfahren/digiwiz_ai_runtime.md`).

Prinzip: Task → Routing → Playbooks → Provider → Validator → Regisseur-Inbox.

MCP: vorbereitet (`mcp.enabled: false`), nicht implementiert — ADR-0001.
