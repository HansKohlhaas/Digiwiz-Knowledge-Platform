# ADR-0004: No auto-publishing

## Status

Accepted

## Context

Externe Kanaele wie LinkedIn oder WordPress haben reputative und rechtliche Wirkung.

## Decision

Digiwiz veroeffentlicht keine Inhalte automatisch. Das System darf Veroeffentlichung vorbereiten, aber nicht final ausloesen.

## Consequences

- Publish-nahe Funktionen benoetigen explizite Freigabe.
- APIs und MCP-Tools duerfen standardmaessig keine Publish-Aktionen anbieten.
- Beispiele muessen `auto_publish: false` respektieren.
