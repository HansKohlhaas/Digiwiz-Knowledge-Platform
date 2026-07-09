# ADR-0006: Kein Git-Submodule bis nach Stufe E

## Status

Akzeptiert (2026-07-09)

## Kontext

Die Knowledge Platform existiert als eigenständiges Repository (`Digiwiz-Knowledge-Platform`). Im Digiwiz-Monorepo liegt zudem eine Kopie unter `knowledge-platform/`. Die Frage ist, ob die Repositories per Git-Submodule gekoppelt werden sollen.

## Entscheidung

1. **Vorläufig keine Git-Submodule** zwischen Digiwiz App und Knowledge Platform.
2. Die Knowledge Platform wird **zunächst als eigenständiges Repository** entwickelt (kanonische Quelle für Wissen/Regeln).
3. Die Digiwiz App bindet sie ausschließlich über die **konfigurierbare Schnittstelle** ein:
   - `DIGIWIZ_KNOWLEDGE_ROOT` (Pfad zum geklonten KP-Repo), oder
   - Default `knowledge-platform/` im Monorepo (Entwicklungs-Fallback).
4. **Nach Abschluss von Stufe E (Knowledge Graph)** wird erneut bewertet, ob eine Submodule-Einbindung sinnvoll ist.

## Begründung

- **Stabilität** von Architektur und Schnittstellen (`knowledge_paths.py`, Schemas, Playbooks) hat Vorrang vor Repo-Kopplung.
- Submodule erhöhen die Komplexität (Clone, CI, Windows-Pfade, Contributor-Onboarding) ohne unmittelbaren Nutzen in Stufe A–D.
- Lose Kopplung erlaubt parallele Entwicklung und unabhängige Versionierung (`VERSION`, `knowledge_lock.json`).

## Konsequenzen

- Zwei Repos können kurzzeitig divergieren — Abgleich über `VERSION` + `digiwiki/knowledge_lock.json` + Contract-Tests.
- Deployment: KP-Repo separat klonen, `DIGIWIZ_KNOWLEDGE_ROOT` setzen.
- Monorepo-Kopie `knowledge-platform/` bleibt optionaler Dev-Fallback, nicht verbindliche Submodule-Referenz.
- Re-Evaluation-Stufe: **E (Knowledge Graph)** — Kriterien: Graph-Assets, Release-Prozess, CI über Repo-Grenzen.

## Verwandte ADRs

- ADR-0003 — Playbooks als SSOT
- ADR-0005 — Knowledge getrennt von Runtime
