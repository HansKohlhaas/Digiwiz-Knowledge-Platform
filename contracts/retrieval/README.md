# Retrieval- und RAG-Policy (Stufe E — geplant)

Verträge für **Kontext-Zusammenführung** im DAR Context Builder — nicht für die Chroma-DB selbst.

**Voraussetzung:** [Source Resolution](../source-resolution/) (ADR-0013) — SQL-first **vor** Graph/RAG-Merge.

## Abgrenzung (ADR-0009)

| Artefakt | Rolle | SSOT? |
|----------|--------|-------|
| Playbooks, ADRs, Contracts (KP) | Regeln, Schnittstellen | ✅ führend |
| Knowledge Graph (`contracts/graph/`) | Struktur, Beziehungen, Provenienz | ✅ Schema in KP |
| **Dieser Ordner** | Retrieval-Prioritäten, Limits, Merge-Regeln Graph↔RAG | ✅ Policy in KP |
| Chroma / Vektor-Index | Semantischer Retrieval-Index | ❌ abgeleitet, App |

**Keine Chroma-Implementierung** in der Knowledge Platform. Chroma bleibt in der Digiwiz App (`digiwiki/Chroma_DB/`).

## Geplante Inhalte

- Kontext-Priorität **nach** Source Resolution: Graph → RAG (innerhalb Schritt 3–4)
- Token-/Passage-Limits pro Task
- Provenienz-Pflicht in DAR-Kontext
- No-Gos (kein Auto-Publish aus RAG-Snippets)

Siehe [ADR-0009](../adr/ADR-0009-knowledge-graph-and-chroma-rag.md), [ADR-0013](../adr/ADR-0013-source-resolution-and-sql-first-policy.md), [merge_policy.yaml](merge_policy.yaml) (Platzhalter).
