# ADR-0012: Contracts vor Automation in Stufe E/F

## Status

Akzeptiert (2026-07-09)

## Metadaten

| Feld | Wert |
|------|------|
| Datum | 2026-07-09 |
| Scope | Stufe E, F |
| Artefakte | `schemas/`, `contracts/`, `tests/`, Roadmap |
| Verwandt | ADR-0004, ADR-0007, ADR-0010 |

## Kontext

Stufe E (Knowledge Graph) und F (Autonome Agenten) können als „autonome Fähigkeiten“ missverstanden werden — bevor Governance-Contracts und Tests stehen. Das Audit identifizierte Lücken bei Runtime-Output, API-Fehler, Graph-Nodes/Edges, Context Builder und Chroma-Rebuild.

## Entscheidung

**Stufe E/F-Automation startet erst nach Contract- und Governance-Abschluss** für die betroffenen Artefakte:

| Contract | Status vor E1-Implementierung |
|----------|------------------------------|
| `knowledge_graph_node/edge.schema.json` | Schema + Beispiel |
| `context_builder_*.schema.json` | Schema + Beispiel |
| `chroma_index_manifest.schema.json` | Schema (Rebuild-Regeln) |
| `runtime_output.schema.json` | Schema |
| `api_error.schema.json` | Schema |
| Playbook `governance.auto_publish: false` | Alle publish-nahen Playbooks |
| ADR-0010, 0011 | Akzeptiert |

### Stufe F zusätzlich

- Policy-Contracts unter `contracts/policies/` (geplant)
- Explizite Erweiterung von ADR-0004 — **kein** Override durch Autonomie
- Regisseur-Inbox bleibt für externe Wirkung verbindlich

### Reihenfolge

```
ADR → Schema → Beispiel → Contract-Test → App-Implementierung → Integrations-Test
```

## Konsequenzen

- Roadmap E1–E5 und F bleiben; **E1 = Schemas + ADRs**, nicht Produktiv-Graph-Store
- Cursor-Tasks für E/F referenzieren diese ADR
- Keine Breaking Changes an Stufe A–D Pfaden

## Verwandte ADRs

- ADR-0004, ADR-0006, ADR-0007, ADR-0008, ADR-0009
