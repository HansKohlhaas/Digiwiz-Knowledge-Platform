# Deployment

Dieses Repository enthaelt keine Produktivlogik und wird daher nicht als Anwendung deployed. Deployment bedeutet hier die kontrollierte Verteilung von Dokumentation, Schemas und Playbooks.

## Artefakte

- Markdown-Dokumente fuer Menschen und KI-Assistenten.
- YAML-Playbooks fuer Workflow-Steuerung.
- JSON Schemas fuer Validierung.
- Beispiele fuer Implementierung und Tests.

## Regeln

- Aenderungen werden versioniert.
- Breaking Changes an Schemas benoetigen ADR und Migrationshinweis.
- Produktivsysteme importieren nur freigegebene Versionen.
- Windows-Pfade und Shell-Kommandos muessen kompatibel dokumentiert werden.
