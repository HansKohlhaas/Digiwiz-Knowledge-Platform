# ADR-0001: REST vor MCP

## Status

Akzeptiert (2026-07-09)

## Kontext

Externe KI-Systeme sollen Digiwiz anbinden. MCP ist attraktiv, aber noch nicht überall stabil einsetzbar.

## Entscheidung

1. **REST/CLI zuerst** (Stufe C/D): `digiwiz-agent`, FastAPI `/api/v1/*`
2. **MCP vorbereiten**, nicht implementieren: Routing-Config enthält `mcp.enabled: false`
3. Gleiche Semantik für spätere MCP-Tools wie REST-Endpunkte

## Konsequenzen

- Externe Agenten nutzen HTTP + API-Key
- Knowledge Platform dokumentiert REST-Contracts
- MCP folgt als Adapter-Schicht ohne Logik-Duplikat
