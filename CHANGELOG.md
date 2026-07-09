# Changelog

Format basiert auf [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

## [1.1.0] - 2026-07-09

### Added

- ADR-0010: DAR als einzige AI Runtime
- ADR-0011: Context Builder kombiniert kanonisch + Graph + RAG
- ADR-0012: Contracts vor E/F-Automation
- `docs/12_architecture_layers.md` — Schichtenmodell KP / DAR / Graph / Chroma
- Contract-Schemas: Runtime-Output, API-Fehler, Knowledge Graph Node/Edge, Context Builder, Chroma Manifest/Rebuild, Playbook-Governance, LinkedIn
- Beispiele: `examples/linkedin/`, `examples/retrieval/`, `examples/runtime/`
- Einheitliche `governance`-Metadaten in allen Playbooks
- `tests/test_governance.py` — Schema-, YAML- und Governance-Validierung
- `cursor/CURSOR_TASK_STAGE_E.md`, `cursor/CURSOR_TASK_STAGE_F.md`
- Operative Matrix in `docs/11_roadmap_stufen_a_f.md`

### Changed

- `docs/04_ai_runtime.md` — explizite DAR-Definition und Abgrenzung
- `docs/10_contracts.md` — Runtime- und Context-Contract-Katalog

## [1.0.0] - 2026-07-09

### Added

- Initiales Knowledge-Platform-Repo im Digiwiz-Monorepo (`knowledge-platform/`)
- Playbooks: presseschau, linkedin, brandvoice, sources, image, wordpress, seo
- Content: `linkedin-presseschau.md` (kanonisch)
- Schema: `agent-lieferung.v3.json`
- Runtime: `routing.json` (aus Stufe D)
- ADR-0001 bis ADR-0005
- ADR-0006: Kein Git-Submodule bis nach Stufe E — lose Kopplung über `DIGIWIZ_KNOWLEDGE_ROOT`
- ADR-0007: Verträge (Contracts) als verbindliche Artefakte
- ADR-0008: Knowledge Graph als KP-Erweiterung, keine neue Runtime (Stufe E)
- ADR-0009: Knowledge Graph + Chroma/RAG — Rollen, DAR Context Builder kombiniert beides
- `adr/README.md` — ADR-Index
- `contracts/retrieval/` — Retrieval-Policy-Platzhalter (keine Chroma-Implementierung)
- `docs/11_roadmap_stufen_a_f.md` — Roadmap A–F inkl. Dual-Repo-Synchronisation
- Manifest `meta/manifest.yaml`, VERSION 1.0.0
- Verfahrensdoku migriert aus `docs/wiki/verfahren/`
- Digiwiz App: `knowledge_paths.py` + `knowledge_lock.json` (Fallback-kompatibel)

### Notes

- Keine Breaking Changes — Legacy-Pfade in `firmenapp/config/` bleiben als Fallback
- Stufe E (Knowledge Graph) bewusst nicht enthalten
