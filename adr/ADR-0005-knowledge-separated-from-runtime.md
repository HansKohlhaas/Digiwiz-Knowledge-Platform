# ADR-0005: Knowledge Platform getrennt von App-Runtime

## Status

Akzeptiert (2026-07-09)

## Kontext

Stufen A–D wurden im Digiwiz-Monorepo implementiert. Für Wartbarkeit und Versionierung soll Wissen von Ausführung getrennt werden.

## Entscheidung

| Knowledge Platform | Digiwiz App (Monorepo) |
|------------------|------------------------|
| Playbooks, Schemas, ADRs | `ai_runtime/`, `agent_*.py` |
| Runtime-Routing JSON | Pipeline, Provider |
| Examples, Verfahren | UI, Inbox, `data/` |

Binding: `DIGIWIZ_KNOWLEDGE_ROOT` oder Default `../knowledge-platform/` im Monorepo.

## Konsequenzen

- Knowledge Platform kann als eigenes Git-Repo ausgekoppelt werden
- App-Tests bleiben Integrations-Tests; Knowledge-Tests sind Contract-Tests
- Stufe E (Knowledge Graph) startet **nur** in Knowledge Platform
