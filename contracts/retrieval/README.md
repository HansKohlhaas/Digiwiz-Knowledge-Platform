# Retrieval- und RAG-Policy (Stufe E — geplant)

Verträge für **Kontext-Zusammenführung** im DAR Context Builder — nicht für die Chroma-DB selbst.

## Abgrenzung (ADR-0009)

| Artefakt | Rolle | SSOT? |
|----------|--------|-------|
| Playbooks, ADRs, Contracts (KP) | Regeln, Schnittstellen | ✅ führend |
| Knowledge Graph (`contracts/graph/`) | Struktur, Beziehungen, Provenienz | ✅ Schema in KP |
| **Dieser Ordner** | Retrieval-Prioritäten, Limits, Merge-Regeln Graph↔RAG | ✅ Policy in KP |
| Chroma / Vektor-Index | Semantischer Retrieval-Index | ❌ abgeleitet, App |

**Keine Chroma-Implementierung** in der Knowledge Platform. Chroma bleibt in der Digiwiz App (`digiwiki/Chroma_DB/`).

## Geplante Inhalte

- Kontext-Priorität: Playbooks → Graph → RAG
- Token-/Passage-Limits pro Task
- Provenienz-Pflicht in DAR-Kontext
- No-Gos (kein Auto-Publish aus RAG-Snippets)

Siehe [ADR-0009](../adr/ADR-0009-knowledge-graph-and-chroma-rag.md), [ADR-0008](../adr/ADR-0008-knowledge-graph-as-platform-extension.md).
