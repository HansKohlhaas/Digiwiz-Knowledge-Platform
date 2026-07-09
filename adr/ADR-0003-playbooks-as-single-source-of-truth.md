# ADR-0003: Playbooks as Single Source of Truth

## Status

Accepted

## Context

Wiederholbare Arbeitsablaeufe brauchen konsistente Regeln fuer Menschen, APIs und KI-Assistenten.

## Decision

Playbooks werden als Single Source of Truth fuer Prozessregeln genutzt.

## Consequences

- Prompts und Code muessen Playbooks referenzieren.
- Aenderungen an Workflow-Regeln beginnen im Playbook.
- Schemas validieren zentrale Ergebnisformate.
