# ADR-0010: DAR als einzige AI Runtime

## Status

Akzeptiert (2026-07-09)

## Metadaten

| Feld | Wert |
|------|------|
| Datum | 2026-07-09 |
| Scope | Stufe D, E, F |
| Artefakte | `digiwiki/ai_runtime/`, `runtime/routing.json`, `docs/04_ai_runtime.md` |
| Verwandt | ADR-0005, ADR-0008, ADR-0011 |

## Kontext

Digiwiz Stufe D implementiert die **Digiwiz AI Runtime (DAR)** in `digiwiki/ai_runtime/`. Mit Stufe E (Knowledge Graph) und bestehendem Chroma/RAG besteht das Risiko, parallele „Runtimes“ zu schaffen (`graph_runtime`, `rag_runtime`, separater Orchestrator).

Die Doku nannte bisher oft nur „AI Runtime“, ohne den **DAR**-Begriff und die Einzigkeit verbindlich festzuhalten.

## Entscheidung

**DAR (Digiwiz AI Runtime) ist die einzige AI Runtime in Digiwiz.**

| Komponente | Rolle | Runtime? |
|------------|--------|----------|
| **DAR** | Task → Routing → Context → Provider → Validator → Inbox | ✅ **einzige AI Runtime** |
| Knowledge Platform | Contracts, Playbooks, Schemas, Routing-JSON | ❌ |
| Knowledge Graph (Stufe E) | Strukturierter Kontext | ❌ (ADR-0008) |
| Chroma/RAG | Semantischer Index | ❌ (ADR-0009) |
| Regisseur-Inbox | Freigabe-Hub | ❌ |

### DAR-Umfang (App)

- `ai_runtime/pipeline.py`, `routing_engine.py`, `context_builder.py`
- Provider-Registry, Task/Agent-Registry
- REST `/api/v1/runtime/*`
- Konfiguration: `runtime/routing.json` (KP) + Env/Keys (App)

### Verboten ohne neue ADR

- Zweite Pipeline neben DAR für KI-Orchestrierung
- Eigener HTTP-Server als „Graph Runtime“ oder „RAG Runtime“
- Auto-Publish aus DAR-Ergebnissen (ADR-0004)

## Konsequenzen

- `docs/04_ai_runtime.md` benennt DAR explizit
- Stufe E/F erweitern **Context Builder** und Contracts — nicht DAR duplizieren
- Neue Features prüfen: „Ist das DAR-Erweiterung oder neue Runtime?“

## Verwandte ADRs

- ADR-0004 — Keine Auto-Veröffentlichung
- ADR-0005 — Knowledge getrennt von Runtime
- ADR-0008 — Knowledge Graph keine Runtime
- ADR-0009 — Chroma/RAG abgeleitet
- ADR-0011 — Context Builder
