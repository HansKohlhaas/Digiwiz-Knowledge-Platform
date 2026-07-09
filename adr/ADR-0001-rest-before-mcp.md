# ADR-0001: REST before MCP

## Status

Accepted

## Context

Digiwiz benoetigt stabile Integrationspunkte fuer bestehende Systeme, CLI-Aufrufe und spaetere Agenten.

## Decision

REST wird zuerst spezifiziert und umgesetzt. MCP wird als Adapter auf stabile REST-Funktionen vorbereitet.

## Consequences

- Fruehe Integrationen bleiben einfach testbar.
- MCP-Tools koennen spaeter kontrolliert ergaenzt werden.
- API-Vertraege muessen versioniert und dokumentiert werden.
