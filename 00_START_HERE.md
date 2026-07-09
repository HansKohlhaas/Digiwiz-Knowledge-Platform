# Start here — Digiwiz Knowledge Platform

## Für Menschen

1. [README.md](README.md) — Zweck und Grenzen
2. [docs/11_roadmap_stufen_a_f.md](docs/11_roadmap_stufen_a_f.md) — **Roadmap A–F**
3. [docs/10_contracts.md](docs/10_contracts.md) — Verträge (Contracts)
4. [adr/](adr/) — Architekturentscheidungen ([Index](adr/README.md))
5. [docs/verfahren/](docs/verfahren/) — Betriebsverfahren
6. [playbooks/](playbooks/) — Maschinenlesbare Regeln
7. [content/playbooks/](content/playbooks/) — Kanonische Langtexte

## Für Digiwiz App / Cursor

- Manifest: [meta/manifest.yaml](meta/manifest.yaml)
- Schema Presseschau: [schemas/agent-lieferung.v3.json](schemas/agent-lieferung.v3.json)
- Runtime-Routing: [runtime/routing.json](runtime/routing.json)
- Beispiele: [examples/presseschau/](examples/presseschau/)
- Cursor: [cursor/CURSOR_IMPLEMENTATION_GUIDE.md](cursor/CURSOR_IMPLEMENTATION_GUIDE.md)
- Codex: [codex/CODEX_WORKING_RULES.md](codex/CODEX_WORKING_RULES.md)

## Stufen A–D (bereits in App umgesetzt)

| Stufe | Knowledge Platform | Digiwiz App |
|-------|-------------------|-------------|
| A | Playbooks, Content, Examples | Inbox, Import, Morgen-Lauf |
| B | Schemas, QS-Docs | `agent_lieferung_validierung.py` |
| C | API-Doku in `docs/verfahren/` | `digiwiz_agent.py`, `11_wiki_api.py` |
| D | `runtime/routing.json` | `digiwiki/ai_runtime/` |

## Stufen E–F (Roadmap)

| Stufe | Fokus | Status |
|-------|--------|--------|
| E | Knowledge Graph + RAG-Rollen | ⏳ [Roadmap](docs/11_roadmap_stufen_a_f.md) · ADR-0008/0009 |
| F | Autonome Agenten | 📋 Roadmap |

Details: [docs/11_roadmap_stufen_a_f.md](docs/11_roadmap_stufen_a_f.md)
