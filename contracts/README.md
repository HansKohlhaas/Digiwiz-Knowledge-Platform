# Verträge (Contracts) — Übersicht

Die Knowledge Platform ist **kein reines Dokumentations-Repository**, sondern die verbindliche Quelle für **Regeln und Schnittstellen** (ADR-0007).

## Contract-Katalog

| Typ | Pfad | Maschinenlesbar | Beschreibung |
|-----|------|-----------------|--------------|
| Playbooks | `playbooks/`, `content/playbooks/` | YAML, Markdown | Inhaltsregeln, Brandvoice, Quellen |
| JSON-Schemas | `schemas/` | JSON Schema | Lieferungs-Envelope, Datenmodelle |
| Prompt-Schemas | `schemas/prompts/` | JSON/YAML (geplant) | Kontext- und Prompt-Struktur für DAR |
| API-Verträge | `contracts/api/` | OpenAPI/JSON (geplant) | `/api/v1/*`, `/api/v1/runtime/*` |
| Runtime | `runtime/` | JSON | Routing, Task→Agent→Modell |
| ADRs | `adr/` | Markdown | Architekturentscheidungen |
| Beispiele | `examples/` | JSON | Gültige und fehlerhafte Instanzen |

## Status v1.0.0

- ✅ Playbooks, Runtime, ADRs, `agent-lieferung.v3.json`
- ✅ Verfahrensdoku in `docs/verfahren/` (menschenlesbar, verweist auf Contracts)
- ⏳ Prompt-Schemas, API-Verträge (OpenAPI) — inkrementell nach Stufe C/D

## Prüfung

```bash
python -m unittest tests.test_contract -v
```

Details: [docs/10_contracts.md](../docs/10_contracts.md)
