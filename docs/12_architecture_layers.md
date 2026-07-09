# Architektur-Schichten — Knowledge Platform, DAR, Graph, Chroma

**Stand:** 09.07.2026  
Explizite Abgrenzung der im Audit genannten Schichten.

Siehe auch: [13_source_resolution.md](13_source_resolution.md) — **SQL-first** vor Graph/RAG (ADR-0013).

## Schichtenmodell

```
┌─────────────────────────────────────────────────────────────┐
│  Knowledge Platform (SSOT)                                   │
│  Playbooks · ADRs · Contracts · Schemas · Graph-Schema     │
│  Source-Resolution-Policy (SQL-first)                        │
└───────────────────────────┬─────────────────────────────────┘
                            │ DIGIWIZ_KNOWLEDGE_ROOT
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Digiwiz App                                                 │
│  ┌──────────┐ ┌─────────────┐ ┌──────────────┐ ┌──────────┐ │
│  │ SQL/CRM  │ │ Chroma/RAG  │ │ Graph-Store  │ │ DAR      │ │
│  │ Stammdaten│ │ (abgeleitet)│ │ (optional)   │ │ context_ │ │
│  │ SSOT Firm│ │             │ │              │ │ builder  │ │
│  └────┬─────┘ └──────┬──────┘ └──────┬───────┘ └────┬─────┘ │
│       └──────────────┴───────────────┴──────────────┘       │
│                            │                                  │
│                            ▼                                  │
│                   Regisseur-Inbox → manuelle Freigabe         │
└─────────────────────────────────────────────────────────────┘
```

## Rollenmatrix

| Schicht | SSOT? | Runtime? | Speichert kanonisches Wissen? |
|---------|-------|----------|-------------------------------|
| Knowledge Platform | ✅ | ❌ | ✅ (versioniert) |
| **SQL / CRM** | ✅ **Firmendaten** | ❌ | ✅ operative Stammdaten (App-DB) |
| **DAR** | ❌ | ✅ **einzige AI Runtime** | ❌ (nur Laufzeit/Telemetry) |
| Knowledge Graph | Schema in KP | ❌ | Struktur in KP; Instanz optional in App |
| Chroma/RAG | ❌ | ❌ | ❌ — **abgeleiteter Index** |
| Regisseur-Inbox | ❌ | ❌ | Vorschläge bis Freigabe (`data/`) |

## Source Resolution (ADR-0013)

**Reihenfolge:** Klassifikation → KP (Regeln) → **SQL bei Firmendaten** → Graph → Chroma → Web.

Bei Konflikt **SQL schlägt Chroma/Web** für Stammdaten; **KP schlägt Chroma** für Regeln.

## Stufe E in einem Satz

**Knowledge Graph** = Erweiterung der Knowledge Platform (Beziehungen, Provenienz) — **kein** Entscheidungssystem, **kein** Runtime-Ersatz (ADR-0008, ADR-0010).

## Chroma in einem Satz

**Chroma** = rebuild-fähiger semantischer Retrieval-Index aus KP-/Wiki-Quellen — bei Konflikt gilt **Knowledge Platform** (ADR-0009).

## DAR in einem Satz

**DAR** = einzige AI Runtime; **Context Builder** merged Playbooks (Pflicht) + SQL (bei Firmendaten) + Graph + RAG (ADR-0010, ADR-0011, ADR-0013). Keine Auto-Veröffentlichung — Regisseur-Inbox bleibt Freigabe-Hub (ADR-0002, ADR-0004).

## ADR-Index

Siehe [adr/README.md](../adr/README.md) — insbesondere 0008–0012.

## Verwandte Dokumente

- [04_ai_runtime.md](04_ai_runtime.md) — DAR Detail
- [11_roadmap_stufen_a_f.md](11_roadmap_stufen_a_f.md) — Stufen A–F operativ
- [13_source_resolution.md](13_source_resolution.md) — SQL-first, Auflösungssequenz
