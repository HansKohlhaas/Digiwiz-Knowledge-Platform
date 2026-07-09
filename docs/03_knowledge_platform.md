# Knowledge Platform

Die Knowledge Platform ist die dokumentierte Steuerungsschicht fuer Digiwiz. Sie macht Ablaufe, Datenmodelle und Entscheidungen versionierbar.

## Inhalte

- Playbooks fuer wiederholbare Arbeitsablaeufe.
- Schemas fuer Validierung und Austauschformate.
- ADRs fuer Architekturentscheidungen.
- Beispiele fuer erwartete Ergebnisse.
- Implementierungsanweisungen fuer Cursor und Codex.

## Single Source of Truth

Playbooks sind die primaere Quelle fuer Prozessregeln. Code, Prompts und API-Handler duerfen Playbook-Regeln nur referenzieren oder umsetzen, aber nicht widerspruechlich neu definieren.

## Pflege

Neue Workflows werden zuerst als Playbook beschrieben, danach mit Schema validiert und erst anschliessend in CLI, API oder Runtime umgesetzt.
