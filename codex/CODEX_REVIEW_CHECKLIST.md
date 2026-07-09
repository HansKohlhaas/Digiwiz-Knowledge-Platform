# Codex Review Checklist

## Architektur

- Passt die Aenderung zum Stufenmodell?
- Ist ein ADR notwendig?
- Bleibt REST-first und MCP-ready gewahrt?
- Gibt es Breaking Changes?

## Playbooks und Schemas

- Ist das Playbook die Single Source of Truth?
- Sind YAML- und JSON-Dateien maschinenlesbar?
- Stimmen Beispiele mit Schemas ueberein?
- Ist `auto_publish` explizit false, wo relevant?

## Sicherheit

- Keine Secrets enthalten?
- Keine automatischen Publish-Pfade?
- Freigabe durch Hans klar markiert?
- Sensible Daten vermieden?

## Qualitaet

- Sachliche Sprache ohne Marketingfloskeln?
- Quellen- und Unsicherheitsregeln beachtet?
- Windows-Kompatibilitaet beruecksichtigt?
- Dokumentation fuer Menschen und KI verstaendlich?
