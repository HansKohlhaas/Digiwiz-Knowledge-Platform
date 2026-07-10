---
title: DAR — KP v1.5.1 Integrationsplan (App)
slug: dar-kp-integration-plan
category: Architektur
audience: developers
version: "2026-07-10"
order: 15
---

# DAR — Integrationsplan Knowledge Platform v1.5.1

**Stand:** 10.07.2026  
**Scope:** Digiwiz App (Monorepo) — **Planung, keine Implementierung**  
**KP-Version:** 1.5.1 (`knowledge_lock.json`)

**Verbindlich:** ADR-0011 (Context Assembly), ADR-0013 (Source Resolution / SQL-first), ADR-0014 (Decision Engine), ADR-0010 (DAR einzige Runtime), ADR-0002/0004 (Regisseur-Inbox, kein Auto-Publish)

---

## Executive Summary

Die Digiwiz-App hat heute **zwei getrennte KI-Pfade**:

| Pfad | Einstieg | Fähigkeit |
|------|----------|-----------|
| **DAR** (`digiwiki/ai_runtime/`) | `POST /api/v1/runtime/task` | Task-Routing → Playbooks → Provider → Validator → Inbox |
| **Wiki Oracle** (`ask_wiki.py`, `frage_strukturierung.py`) | `15_wiki_web_ui.py` | Heuristisches Intent → SQL / Spezialdokumente → Chroma RAG |

KP v1.5.1 beschreibt eine **einheitliche Pipeline innerhalb DAR**. Die Wiki-Logik ist fachlich näher an ADR-0013, ist aber **nicht policy-gesteuert** und **nicht mit DAR verbunden**.

**Strategie:** DAR schrittweise erweitern, Wiki-Adapter **wiederverwenden** (nicht ersetzen), Legacy-Pfad per Feature-Flag absicherbar.

---

## 1. Ist-Architektur

```
POST /api/v1/runtime/task
        │
        ▼
route_task()          ← routing.json (KP)
        │
        ▼
baue_kontext()        ← Playbooks + Memory only
        │
        ▼
provider.complete()
        │
        ▼
validiere_antwort() → optional regisseur_inbox
```

**Parallel (nicht DAR):**

```
Wiki UI → frage_strukturierung / wiki_frage_register → SQL
       → ask_wiki.frage_das_wiki() → Chroma RAG
```

**KP-Contracts:** `contracts/decision-engine/`, `contracts/source-resolution/` — **nicht von App-Code konsumiert**.

### Betroffene DAR-Module

| Datei | Rolle heute |
|-------|-------------|
| `digiwiki/ai_runtime/pipeline.py` | Orchestrierung |
| `digiwiki/ai_runtime/context_builder.py` | Playbooks + Memory → Provider-Messages |
| `digiwiki/ai_runtime/routing_engine.py` | Task → Agent/Model/Playbooks |
| `digiwiki/knowledge_paths.py` | KP-Pfad-Auflösung (Playbooks, routing.json) |

### Wiki-Module (Wiederverwendung)

| Datei | Mapping zu KP |
|-------|----------------|
| `frage_strukturierung.py` | → `intent_classification` |
| `sql_frage_katalog.py` | → `sql_first_domains` |
| `wiki_frage_register.py` | Referenz Source Resolution |
| `ask_wiki.py` | → `chroma_rag` |

---

## 2. Ziel-Pipeline

```
User Query
    → Intent Recognition
    → Decision Engine          (ADR-0014)
    → Source Resolution        (ADR-0013)
    → Context Assembly         (ADR-0011)
    → DAR Context Builder
    → Provider → Validator → Regisseur-Inbox
```

**Leitplanken:**

- `provider_call_allowed = false` bis Context Assembly `ready_for_generation`
- Kein Auto-Publish (ADR-0004)
- SQL-first für operative Fakten (ADR-0013)
- Chroma nie SSOT (ADR-0009)
- Decision Engine: entscheidet, führt **kein** Retrieval aus

---

## 3. Einbindungspunkte (10 Analysefragen)

### 3.1 Betroffene Module

**Direkt:** `pipeline.py`, `context_builder.py`, `knowledge_paths.py`  
**Neu:** `intent_recognition.py`, `decision_engine.py`, `source_resolution_router.py`, `context_assembly_pipeline.py`, `contracts/`, `adapters/`  
**Unverändert:** `regisseur_inbox.py`, `agent_lieferung*`, `providers/*`

### 3.2 Intent Recognition — heute

| Ort | Status |
|-----|--------|
| Wiki (`frage_strukturierung.py`) | ✅ Heuristiken + SQL-Intents |
| DAR | ❌ Nur `task_id`, kein Freitext-Intent |

**Ziel:** `intent_recognition.py` → `intent_classification` (KP `decision_input.schema.json`), Adapter auf `frage_strukturierung`.

### 3.3 Source Resolution

**Nach** Decision Engine, **vor** Context Assembly.  
Policy: `contracts/source-resolution/source_resolution_policy.yaml`  
Output: `sql_snippets`, `rag_snippets`, `graph_snippets`, `resolution_path`, `conflicts`

### 3.4 Context Assembly

**Nach** Source Resolution, **vor** `baue_kontext`.  
Contract: `context_assembly.schema.json`  
Gate: `ready_for_generation` — kein Provider bei `false`

### 3.5 Decision Engine

**Nach** Intent, **vor** Source Resolution.  
Contracts: `contracts/decision-engine/`  
Output: `decision_output`, `decision_trace`, `decision_context`  
Bei `next_stage: clarification|block|approval_gate` → Stopp vor Provider

### 3.6 SQL-first technisch

1. Klassifikation: Policy `sql_first_domains` + `intent_classification`
2. Decision: `sql_crm_stammdaten: required`
3. Ausführung: `SqlCrmAdapter` (Wiki-SQL-Pfad wiederverwenden)
4. Output: `sql_snippets[]` mit `provenance`
5. Konflikt: SQL > Chroma für operative Felder

### 3.7 Graph + Chroma später

| Quelle | Phase | Adapter |
|--------|-------|---------|
| Chroma/RAG | Phase 5 | `ChromaRagAdapter` (`ask_wiki.baue_retriever`) |
| Knowledge Graph | Phase 6 | `GraphQueryAdapter` (`graph_query.schema.json`, Stub zuerst) |

### 3.8 Adapter / Loader / Interfaces

```
digiwiki/ai_runtime/
├── contracts/
│   ├── kp_loader.py
│   ├── schema_validator.py
│   └── policy_refs.py
├── adapters/
│   ├── intent_adapter.py
│   ├── sql_crm_adapter.py
│   ├── kp_governance_adapter.py
│   ├── chroma_rag_adapter.py
│   ├── graph_query_adapter.py
│   └── web_external_adapter.py
├── intent_recognition.py
├── decision_engine.py
├── source_resolution_router.py
└── context_assembly_pipeline.py
```

**knowledge_paths.py erweitern:** `contracts_dir()`, `decision_policy_pfad()`, `source_resolution_policy_pfad()`, `schema_pfad()`, `pruefe_knowledge_lock()`

### 3.9 APIs unverändert

| API | Anforderung |
|-----|-------------|
| `POST /api/v1/runtime/task` | Request identisch; Response **superset** (optionale Felder) |
| `GET /api/v1/runtime/*` | Unverändert |
| `POST /api/v1/agenten/*` | Unverändert |
| Wiki `frage_das_wiki()` | Unverändert bis Phase 7+ |

**Legacy:** `DAR_KP_PIPELINE=0` oder `use_kp_pipeline=False` → heutiger Pfad.

### 3.10 Tests vor Implementierung

| ID | Test |
|----|------|
| T0 | knowledge_lock ≥ 1.5.1, Pfade resolvierbar |
| T1 | Contract-Loader (YAML/JSON) |
| T2 | KP-Beispiele gegen Schemas |
| T3 | Intent-Adapter → gültiges `intent_classification` |
| T4 | Decision Golden Paths (Presseschau, Clarification, Block) |
| T5 | Output/Context `source_requirements` synchron |
| T6 | `provider_call_allowed` immer `false` auf Decision-Ebene |
| T7 | `ready_for_generation: false` → kein Provider |
| T8 | Legacy-Fallback → bestehende Tests grün |
| T9 | Inbox manuell, kein `published_url` |
| T10 | `sql_required` → SQL-Adapter, nicht Chroma |

---

## 4. Neue Module (Übersicht)

| Modul | ADR | Contract |
|-------|-----|----------|
| `intent_recognition.py` | 0014 Input | `decision_input.schema.json` |
| `decision_engine.py` | 0014 | `decision_output`, `decision_trace`, `decision_context` |
| `source_resolution_router.py` | 0013 | `source_resolution_policy.yaml` |
| `context_assembly_pipeline.py` | 0011 | `context_assembly.schema.json` |
| `context_builder.py` (erweitert) | 0011/0013 | `context_builder_input/output.schema.json` |

---

## 5. Inkrementeller Implementierungsplan

| Phase | Inhalt | Rollback |
|-------|--------|----------|
| **0** | `knowledge_paths` + Contract-Loader + Tests T0–T2 | Neue Dateien only |
| **1** | Intent Recognition (dry-run, nicht in Pipeline) | Flag aus |
| **2** | Decision Engine dry-run + Telemetrie | `DAR_KP_PIPELINE=0` |
| **3** | Source Resolution (SQL + KP only) | Playbooks-only Fallback |
| **4** | Context Assembly + Provider-Gate | Legacy-Pfad |
| **5** | Chroma-Adapter + merge_policy | Adapter deaktivierbar |
| **6** | Graph-Adapter (Stub → Store) | Graph skipped |
| **7** | API-Transparenz + Wiki-Konsolidierung (optional) | Später |

---

## 6. Risiken

| Risiko | Mitigation |
|--------|------------|
| Wiki vs DAR divergiert | Adapter auf `frage_strukturierung`, nicht duplizieren |
| Provider zu früh | `provider_call_allowed` + Assembly-Gate + T7 |
| Breaking API | Nur optionale Response-Felder |
| Chroma füllt SQL-Felder | Policy + Tests T10 |
| Fachlogik im Code | Nur Policy/Playbook interpretieren |
| Schema-Drift | `knowledge_lock` + Contract-Tests in CI |

---

## 7. Teststrategie

1. **KP Contract Tests** (44/44 in KP) — unverändert
2. **App Contract Tests** — Loader + Schema (neu)
3. **Modul-Tests** — Intent, Decision, SR, Assembly
4. **Pipeline-Integration** — mock Provider
5. **Regression** — `test_ai_runtime_stufe_d` Legacy
6. **Governance** — kein Auto-Publish, Inbox-Pflicht

**CI:** Zwei Jobs — `DAR_LEGACY=1` und `DAR_KP_PIPELINE=1` (ab Phase 2).

---

## 8. Definition of Done

| Kriterium | Nachweis |
|-----------|----------|
| KP-Sequenz | `resolution_path` mit `classify_intent`, `kp_governance` |
| Decision → Assembly | `decision_context_ref` in `context_assembly` |
| SQL-first CRM | Presseschau-CRM-Szenario E2E (mock SQL) |
| Kein Provider vor Assembly | Test T7 |
| Legacy grün | `test_ai_runtime_stufe_d` mit Fallback |
| Inbox-Hub | `submit_inbox` → `regisseur_inbox` |
| Audit | `decision_trace` mit `rule_ref` pro Schritt |

---

## 9. Verwandte KP-Dokumente

- [14_decision_engine.md](14_decision_engine.md)
- [13_source_resolution.md](13_source_resolution.md)
- [12_context_assembly_pipeline.md](12_context_assembly_pipeline.md)
- [11_roadmap_stufen_a_f.md](11_roadmap_stufen_a_f.md)
- ADR-0011, ADR-0013, ADR-0014

**App-Pfad (Monorepo):** `docs/wiki/verfahren/dar_kp_integration_plan.md`
