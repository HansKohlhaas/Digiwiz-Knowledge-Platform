# Initial Repository Review

Datum: 2026-07-09  
Scope: Struktur, Dokumentenverweise, Stufenmodell, Playbooks, JSON-Schemas, ADRs und Konsistenz zwischen README, Architektur und Cursor-Aufgaben.

## Ergebnis

Das Repository ist als initiale Digiwiz-Systemdokumentation konsistent angelegt. Die Kernprinzipien sind ueber README, Architektur, API-/MCP-Strategie, Cursor-Aufgaben und ADRs hinweg widerspruchsfrei:

- Digiwiz bleibt Regisseur-System.
- Hans bleibt finale Freigabeinstanz.
- Keine automatische Veroeffentlichung.
- Playbooks sind Single Source of Truth.
- REST-first, MCP-ready.
- Keine Breaking Changes ohne ADR.

## Pruefungen

| Bereich | Status | Ergebnis |
| --- | --- | --- |
| Dokumentenlinks | OK | Die in `00_START_HERE.md` referenzierten Dokumentpfade existieren. Es gibt aktuell keine klassischen Markdown-Links mit relativen Zielen, die brechen koennten. |
| Stufen A-F | Hinweis | README beschreibt A-F vollstaendig. Detaildokumente und Cursor-Aufgaben existieren aktuell nur fuer B-D; A, E und F sind nur auf Uebersichtsebene beschrieben. |
| Playbooks | OK | Alle YAML-Dateien in `playbooks/` sind syntaktisch valide. |
| Playbook-Schema | OK | Alle Playbooks bestehen die Validierung gegen `schemas/playbook.schema.json`. |
| JSON-Dateien | OK | Alle JSON-Dateien in `schemas/` und `examples/` sind syntaktisch valide. |
| JSON-Schemas | OK | Alle Schemas in `schemas/` sind formal gueltige Draft-2020-12-Schemas. |
| ADRs | OK mit Hinweis | Alle ADRs enthalten Status, Kontext, Entscheidung und Konsequenzen. Optional fehlen noch einheitliche Felder wie Datum, Entscheider und Scope. |
| README vs. Architektur vs. Cursor | OK | Keine inhaltlichen Widersprueche gefunden. Cursor Stage B-D folgt der Roadmap aus README und der Architektur. |

## Beobachtungen

### Dokumentenlinks

`00_START_HERE.md` verweist per Inline-Code auf:

- `docs/01_vision.md`
- `docs/02_system_architecture.md`
- `docs/03_knowledge_platform.md`
- `docs/05_api_strategy.md`
- `codex/CODEX_WORKING_RULES.md`

Alle Dateien sind vorhanden. README beschreibt Verzeichnisse statt direkter Links; dadurch gibt es aktuell keine Linkfehler.

### Stufenmodell

Das Stufenmodell ist in README klar definiert:

- A: Knowledge Layer
- B: Qualitaetssicherung
- C: CLI/API
- D: AI Runtime
- E: Knowledge Graph
- F: Autonome Agenten

Die operative Ausarbeitung ist noch asymmetrisch: B, C und D haben eigene Cursor-Aufgaben; A, E und F noch nicht. Das ist fuer den initialen Stand akzeptabel, sollte aber bewusst als Roadmap-Luecke markiert werden.

### Playbooks

Alle Playbooks sind YAML-valide und folgen dem allgemeinen Schema. Inhaltlich gibt es leichte Unterschiede in der Tiefe:

- `presseschau.yaml` und `linkedin.yaml` sind am vollstaendigsten.
- `brandvoice.yaml`, `sources.yaml` und `seo.yaml` nutzen eigene fachliche Felder und keine expliziten `approval_required`- oder `auto_publish`-Felder.

Das ist schema-konform, kann aber bei spaeterer Automatisierung zu uneinheitlicher Auswertung fuehren.

### ADRs

Die vier ADRs decken die wichtigsten Architekturprinzipien ab:

- REST before MCP
- Regisseur remains final approval
- Playbooks as Single Source of Truth
- No auto-publishing

Sie sind fuer den initialen Stand ausreichend. Fuer laengere Nachvollziehbarkeit waere ein einheitliches ADR-Template mit Datum, Status, Entscheider, Kontext, Entscheidung, Konsequenzen und betroffenen Bereichen sinnvoll.

## Empfehlungen

1. Ein eigenes Dokument fuer das Stufenmodell ergaenzen, z. B. `docs/10_roadmap_stages.md`, damit A-F nicht nur im README stehen.
2. Cursor-Aufgaben fuer Stage A, E und F ergaenzen oder explizit als noch nicht geplant markieren.
3. Playbook-Metadaten vereinheitlichen: mindestens `approval_required` und `auto_publish` fuer alle kanal- oder runtime-nahen Playbooks.
4. ADR-Template anlegen und bestehende ADRs optional um Datum, Entscheider und Scope erweitern.
5. README-Verzeichniseintraege spaeter in echte Markdown-Links umwandeln, sobald die Struktur stabil bleibt.
