# ADR-Index — Digiwiz Knowledge Platform

Architekturentscheidungen in Lesereihenfolge (empfohlen für Neueinsteiger).

| ADR | Titel | Stufe / Thema |
|-----|-------|----------------|
| [0001](ADR-0001-rest-before-mcp.md) | REST vor MCP | C, D |
| [0002](ADR-0002-regisseur-remains-final-approval.md) | Regisseur-Inbox bleibt Freigabe-Hub | alle |
| [0003](ADR-0003-playbooks-as-single-source-of-truth.md) | Playbooks als SSOT | A |
| [0004](ADR-0004-no-auto-publishing.md) | Keine Auto-Veröffentlichung | alle |
| [0005](ADR-0005-knowledge-separated-from-runtime.md) | Knowledge getrennt von Runtime | A–E |
| [0006](ADR-0006-no-git-submodule-until-stage-e.md) | Kein Git-Submodule bis nach E | Querschnitt |
| [0007](ADR-0007-contracts-as-binding-artifacts.md) | Contracts als verbindliche Artefakte | alle |
| [0008](ADR-0008-knowledge-graph-as-platform-extension.md) | Knowledge Graph = KP-Erweiterung | E |
| [0009](ADR-0009-knowledge-graph-and-chroma-rag.md) | Graph + Chroma/RAG — Rollen | E |
| [0010](ADR-0010-dar-as-only-ai-runtime.md) | DAR als einzige AI Runtime | D, E |
| [0011](ADR-0011-context-builder-combines-context-layers.md) | Context Assembly before Answer Generation | D, E |
| [0012](ADR-0012-contracts-before-stage-e-f-automation.md) | Contracts vor E/F-Automation | E, F |
| [0013](ADR-0013-source-resolution-and-sql-first-policy.md) | Source Resolution, SQL-first | D, E, Wiki |
| [0014](ADR-0014-decision-engine-orchestration.md) | Decision Engine — Orchestrierung | E4, D |
| [0015](ADR-0015-provider-data-boundary.md) | Provider Data Boundary — externe LLM-Übertragung | D, E, Phase 7E |

**Leitplanke:** Bei Widerspruch zwischen abgeleitetem Index (Chroma) und KP-Contract gilt die **Knowledge Platform**. Bei Widerspruch zwischen Chroma/RAG/Web und **SQL-Firmendaten** gilt **SQL** (ADR-0013). Bei Widerspruch zwischen vollständigem Context Assembly und Provider-Kontext gilt **Provider Data Policy** (ADR-0015).
