# Digiwiz Knowledge Platform

Dieses Repository ist die zentrale, versionierte Systemdokumentation fuer Digiwiz. Es enthaelt keine Produktivlogik, sondern beschreibt Architektur, Playbooks, API-Spezifikationen, MCP-Strategie, Datenmodelle, ADRs, Roadmap und Implementierungsanweisungen fuer Cursor und Codex.

## Zweck

Digiwiz bleibt ein Regisseur-System: KI darf recherchieren, strukturieren, vorschlagen und pruefen. Die finale Freigabe liegt immer bei Hans. Es gibt keine automatische Veroeffentlichung auf LinkedIn, WordPress oder anderen Kanaelen.

## Prinzipien

- Playbooks sind die Single Source of Truth fuer wiederholbare Workflows.
- REST kommt zuerst; MCP-Faehigkeit wird vorbereitet.
- Bestehender Digiwiz-Code wird nicht durch Breaking Changes gefaehrdet.
- Windows-Kompatibilitaet ist verbindlich.
- Architekturentscheidungen werden als ADR dokumentiert.
- Markdown, YAML und JSON bleiben menschenlesbar und maschinenlesbar.

## Stufenmodell

| Stufe | Fokus | Ergebnis |
| --- | --- | --- |
| A | Knowledge Layer | Dokumentierte Architektur, Playbooks, Datenmodelle |
| B | Qualitaetssicherung | Review-Regeln, Validierung, Checklisten |
| C | CLI/API | Lokale Automatisierung und REST-Schnittstellen |
| D | AI Runtime | KI-gestuetzte Vorbereitung und Pruefung |
| E | Knowledge Graph | Verknuepfte Wissensbasis |
| F | Autonome Agenten | Kontrollierte Teilautomatisierung mit Freigabegrenzen |

## Repository-Struktur

- `docs/`: Systemarchitektur, Strategien, Security, QA und Deployment.
- `playbooks/`: Wiederverwendbare Prozessdefinitionen.
- `schemas/`: JSON Schemas fuer Playbooks und Ergebnisformate.
- `adr/`: Architekturentscheidungen.
- `examples/`: Beispielartefakte fuer API- und Content-Ergebnisse.
- `cursor/`: Implementierungsanweisungen fuer Cursor.
- `codex/`: Arbeitsregeln und Review-Checkliste fuer Codex.

## Next actions

1. Bestehende Digiwiz-Architektur importieren/zusammenfassen.
2. Stufe B finalisieren.
3. Stufe C spezifizieren.
4. Stufe D als AI Runtime vorbereiten.
