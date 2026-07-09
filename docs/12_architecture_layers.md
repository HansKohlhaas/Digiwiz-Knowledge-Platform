# Architektur-Schichten — Knowledge Platform, DAR, Graph, Chroma

**Stand:** 09.07.2026  
Explizite Abgrenzung der im Audit genannten Schichten.

## Schichtenmodell

```
┌─────────────────────────────────────────────────────────────┐
│  Knowledge Platform (SSOT)                                   │
│  Playbooks · ADRs · Contracts · Schemas · Graph-Schema     │
└───────────────────────────┬─────────────────────────────────┘
                            │ DIGIWIZ_KNOWLEDGE_ROOT
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Digiwiz App                                                 │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────────┐ │
│  │ Chroma/RAG  │  │ Graph-Store  │  │ DAR (einzige        │ │
│  │ (abgeleitet)│  │ (optional,   │  │  AI Runtime)        │ │
│  │             │  │  App)        │  │  context_builder    │ │
│  └──────┬──────┘  └──────┬───────┘  └──────────┬──────────┘ │
│         └────────────────┴───────────────────────┘           │
│                            │                                  │
│                            ▼                                  │
│                   Regisseur-Inbox → manuelle Freigabe         │
└─────────────────────────────────────────────────────────────┘
```

## Rollenmatrix

| Schicht | SSOT? | Runtime? | Speichert kanonisches Wissen? |
|---------|-------|----------|-------------------------------|
| Knowledge Platform | ✅ | ❌ | ✅ (versioniert) |
| **DAR** | ❌ | ✅ **einzige AI Runtime** | ❌ (nur Laufzeit/Telemetry) |
| Knowledge Graph | Schema in KP | ❌ | Struktur in KP; Instanz optional in App |
| Chroma/RAG | ❌ | ❌ | ❌ — **abgeleiteter Index** |
| Regisseur-Inbox | ❌ | ❌ | Vorschläge bis Freigabe (`data/`) |

## Stufe E in einem Satz

**Knowledge Graph** = Erweiterung der Knowledge Platform (Beziehungen, Provenienz) — **kein** Entscheidungssystem, **kein** Runtime-Ersatz (ADR-0008, ADR-0010).

## Chroma in einem Satz

**Chroma** = rebuild-fähiger semantischer Retrieval-Index aus KP-/Wiki-Quellen — bei Konflikt gilt **Knowledge Platform** (ADR-0009).

## DAR in einem Satz

**DAR** = einzige AI Runtime; **Context Builder** merged Playbooks (Pflicht) + Graph + RAG (ADR-0010, ADR-0011). Keine Auto-Veröffentlichung — Regisseur-Inbox bleibt Freigabe-Hub (ADR-0002, ADR-0004).

## ADR-Index

Siehe [adr/README.md](../adr/README.md) — insbesondere 0008–0012.

## Verwandte Dokumente

- [04_ai_runtime.md](04_ai_runtime.md) — DAR Detail
- [11_roadmap_stufen_a_f.md](11_roadmap_stufen_a_f.md) — Stufen A–F operativ
- [10_contracts.md](10_contracts.md) — Contract-Katalog
