# MCP Strategy

MCP wird als spaetere Integrationsschicht fuer kontrollierte Tool-Nutzung vorbereitet.

## Ziel

MCP soll Digiwiz-Funktionen fuer Agenten zugaenglich machen, ohne Freigabe- und Sicherheitsgrenzen aufzuweichen.

## Reihenfolge

1. Playbooks und Schemas stabilisieren.
2. REST API definieren.
3. MCP-Adapter fuer stabile REST-Funktionen bauen.
4. Tool-Berechtigungen restriktiv dokumentieren.

## MCP-Grenzen

- Tools duerfen Entwuerfe erzeugen und pruefen.
- Tools duerfen keine Inhalte automatisch veroeffentlichen.
- Schreibende Tools benoetigen explizite Freigabe und Audit-Spur.
- Kritische Operationen muessen idempotent oder klar bestaetigungspflichtig sein.
