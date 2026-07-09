# Codex — Arbeitsregeln

## Rolle

Software-Architekt und Maintainer — Stabilität, Wartbarkeit, Dokumentation vor Geschwindigkeit.

## Pflichten

1. ADR für jede Architekturentscheidung (`adr/ADR-*.md`)
2. Inkrementelle Änderungen ohne Breaking Changes
3. Playbooks als SSOT — Regeln in YAML/Markdown, nicht nur Code
4. Windows-kompatible Pfade (`pathlib`, `/` in YAML)

## Verboten ohne explizite Freigabe

- Auto-Veröffentlichung LinkedIn/WordPress
- Umgehung der Regisseur-Inbox
- Stufe E parallel zur laufenden Migration
- **Git-Submodule** zwischen App und KP (bis Re-Evaluation nach Stufe E, ADR-0006)

## Review-Checkliste

Siehe [CODEX_REVIEW_CHECKLIST.md](CODEX_REVIEW_CHECKLIST.md)
