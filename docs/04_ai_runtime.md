# Digiwiz AI Runtime (DAR) — Stufe D

## Definition

**DAR (Digiwiz AI Runtime)** ist die **einzige AI Runtime** in Digiwiz (ADR-0010). Sie orchestriert KI-Tasks — sie ist weder Knowledge Platform noch Knowledge Graph noch Chroma.

## Abgrenzung

| Begriff | Was es ist | Was es nicht ist |
|---------|------------|------------------|
| **DAR** | Pipeline, Provider, Routing, Context Builder, Validator | SSOT, Graph-Store, Vektor-DB |
| **Knowledge Platform** | Contracts, Playbooks, Schemas, ADRs | Ausführung |
| **Knowledge Graph** | Struktur + Provenienz (KP-Schema) | Eigene Runtime (ADR-0008) |
| **Chroma/RAG** | Abgeleiteter semantischer Index (App) | Kanonisches Wissen, Firmendaten (→ SQL) |
| **SQL / CRM** | Operative Stammdaten (App-DB) | Regeln, Playbooks (→ KP) |

## Architektur (DAR)

```
POST /api/v1/runtime/task
        │
        ▼
routing_engine  ← runtime/routing.json (KP)
        │
        ▼
source_resolution_router  ← SQL-first (geplant, ADR-0013)
        │
        ▼
playbook_loader ← playbooks/ (KP)
        │
        ▼
context_builder ← context_assembly_pipeline → Playbooks + SQL? + Graph? + RAG?
        │
        ▼
Provider (OpenAI, Mock, …)
        │
        ▼
response_validator  ← Stufe B Brandvoice
        │
        ▼
regisseur_inbox  (optional submit_inbox: true)
```

**Keine Auto-Veröffentlichung** — Response enthält `inbox_id`, nicht `published_url` (ADR-0004).

## Code (Digiwiz App)

| Modul | Rolle |
|-------|--------|
| `ai_runtime/pipeline.py` | Orchestrierung |
| `ai_runtime/routing_engine.py` | Task → Agent, Modell, Playbooks |
| `ai_runtime/context_builder.py` | Kontext-Merge (ADR-0011, ADR-0013 geplant) |
| `ai_runtime/providers/` | KI-Provider |
| `11_wiki_api.py` | REST `/api/v1/runtime/*` |

## Konfiguration

- **KP:** `runtime/routing.json`
- **App:** Env-Keys (`OPENAI_API_KEY`, …), `data/ai_runtime/`

## Geplante Contracts (KP)

| Schema | Zweck |
|--------|--------|
| `runtime_output.schema.json` | Struktur DAR-Ausgabe |
| `context_builder_input.schema.json` | Kontext-Anfrage |
| `context_assembly.schema.json` | Context-Array vor Antwortgenerierung (ADR-0011) |
| `context_builder_output.schema.json` | Angewandte Playbooks, Quellen, Source Resolution, Unsicherheiten |
| `api_error.schema.json` | Einheitliche API-Fehler |

Stufe E/F-Automation erst nach Contract-Abschluss (ADR-0012).

## MCP

Vorbereitet (`mcp.enabled: false`), nicht implementiert — ADR-0001.

## Verfahren

[Dokumentation Stufe D in der App](verfahren/digiwiz_ai_runtime.md)

## Verwandte ADRs

- ADR-0010 — DAR als einzige Runtime
- ADR-0011 — Context Assembly Pipeline
- ADR-0013 — Source Resolution, SQL-first
