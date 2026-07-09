# ADR-0011: Context Builder kombiniert kanonischen, Graph- und Retrieval-Kontext

## Status

Akzeptiert (2026-07-09)

## Metadaten

| Feld | Wert |
|------|------|
| Datum | 2026-07-09 |
| Scope | Stufe D/E |
| Artefakte | `schemas/context_builder_*.schema.json`, `contracts/retrieval/`, `ai_runtime/context_builder.py` |
| Verwandt | ADR-0003, ADR-0007, ADR-0009, ADR-0010 |

## Kontext

DAR benötigt Kontext aus mehreren Quellen. Ohne definierte **Priorität und Merge-Regeln** konkurieren Playbooks, Knowledge Graph und Chroma/RAG — mit Risiko für Halluzinationen, Quellenverlust und falsche Freigabegrenzen.

## Entscheidung

**`context_builder.py` (DAR) ist die einzige Kombinationsschicht** für KI-Kontext. Priorität:

```
1. Playbooks + ADRs + Contracts (KP, SSOT, Pflicht)
2. Knowledge Graph (strukturiert, Provenienz)          ← Stufe E
3. Chroma/RAG (semantisch, abgeleitet)                ← App-Index
```

### Output-Anforderungen (Contract, geplant)

Jeder Context-Build muss ausweisen (Schema `context_builder_output.schema.json`):

- `applied_playbooks[]`
- `applied_adrs[]` (IDs)
- `graph_snippets[]` mit Provenienz (optional bis E3)
- `rag_snippets[]` mit Quellen-Referenz (abgeleitet)
- `uncertainties[]` — fehlende Quellen, Konflikte KP vs. Index
- **Kein** `published_url`, **kein** Auto-Freigabe-Flag

### Regeln

- Bei Konflikt **KP-Contract schlägt Index** (Chroma rebuild, nicht Index korrigieren)
- Graph und RAG **ergänzen**, ersetzen Playbooks nicht
- Freigabe bleibt Regisseur-Inbox (ADR-0002)

## Konsequenzen

- Contracts: `context_builder_input.schema.json`, `context_builder_output.schema.json`
- Retrieval-Policy unter `contracts/retrieval/`
- Tests: Output muss `auto_publish: false` implizit einhalten (kein Publish-Feld)
- Implementierung in App inkrementell; KP definiert Vertrag zuerst

## Verwandte ADRs

- ADR-0002, ADR-0004, ADR-0009, ADR-0010
