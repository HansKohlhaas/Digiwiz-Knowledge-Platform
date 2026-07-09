# Changelog

Format basiert auf [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Added

- ADR-0006: Kein Git-Submodule bis nach Stufe E — lose Kopplung über `DIGIWIZ_KNOWLEDGE_ROOT`
- ADR-0007: Verträge (Contracts) als verbindliche Artefakte
- ADR-0008: Knowledge Graph als KP-Erweiterung, keine neue Runtime (Stufe E)
- `docs/11_roadmap_stufen_a_f.md` — Roadmap A–F inkl. Dual-Repo-Synchronisation

## [1.0.0] - 2026-07-09

### Added

- Initiales Knowledge-Platform-Repo im Digiwiz-Monorepo (`knowledge-platform/`)
- Playbooks: presseschau, linkedin, brandvoice, sources, image, wordpress, seo
- Content: `linkedin-presseschau.md` (kanonisch)
- Schema: `agent-lieferung.v3.json`
- Runtime: `routing.json` (aus Stufe D)
- ADR-0001 bis ADR-0005
- Manifest `meta/manifest.yaml`, VERSION 1.0.0
- Verfahrensdoku migriert aus `docs/wiki/verfahren/`
- Digiwiz App: `knowledge_paths.py` + `knowledge_lock.json` (Fallback-kompatibel)

### Notes

- Keine Breaking Changes — Legacy-Pfade in `firmenapp/config/` bleiben als Fallback
- Stufe E (Knowledge Graph) bewusst nicht enthalten
