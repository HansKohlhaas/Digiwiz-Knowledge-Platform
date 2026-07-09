---
title: Roadmap Stufen A–F
slug: roadmap-stufen-a-f
category: Planung
audience: all
version: "2026-07-09"
order: 11
---

# Roadmap — Stufen A bis F

**Stand:** 09.07.2026  
**Geltungsbereich:** Digiwiz Knowledge Platform (Contracts) + Digiwiz App (Runtime)  
**Prinzip:** KI bereitet vor → **Regisseur-Inbox** → manuelle Freigabe → **keine Auto-Veröffentlichung** (ADR-0002, ADR-0004)

## Übersicht

```
Stufe A  Knowledge Layer          ✅ abgeschlossen
Stufe B  Qualitätssicherung        ✅ abgeschlossen
Stufe C  CLI / Agenten-API        ✅ abgeschlossen (Contracts API-Spec ⏳)
Stufe D  AI Runtime (DAR)           ✅ abgeschlossen (Prompt-Schemas ⏳)
Stufe E  Knowledge Graph            ⏳ nächste Phase — nur in KP
Stufe F  Autonome Agenten           📋 Roadmap — nach E, ADR-0004 beachten
```

| Stufe | Fokus | Knowledge Platform | Digiwiz App | Status |
|-------|--------|-------------------|-------------|--------|
| **A** | Wissen & Import | Playbooks, Content, Examples | Inbox, Import, Morgen-Lauf | ✅ |
| **B** | QS vor Freigabe | JSON-Schemas, QS-Verfahren | `agent_lieferung_validierung.py` | ✅ |
| **C** | Externe Anbindung | API-Verfahren, API-Contract (geplant) | CLI, FastAPI `/api/v1/*` | ✅ / ⏳ Contract |
| **D** | AI Director | `runtime/routing.json`, Prompt-Schema (geplant) | `digiwiki/ai_runtime/` | ✅ / ⏳ Contract |
| **E** | Knowledge Graph | Graph-Schema, Abfrage-Verträge | Graph-Client (geplant) | ⏳ |
| **F** | Autonomie | Policy-Contracts, Freigabe-Regeln | Scheduler, Agent-Orchestrierung | 📋 |

**Querschnitt:** ADR-0006 (kein Git-Submodule bis nach E) · ADR-0007 (Contracts als SSOT)

Siehe auch: [12_architecture_layers.md](12_architecture_layers.md) — explizite Abgrenzung KP / DAR / Graph / Chroma.

## Operative Matrix (Scope je Stufe)

| Stufe | Scope | Nicht-Ziele | Eingänge | Ausgänge | Freigabegrenze |
|-------|--------|-------------|----------|----------|----------------|
| **A** | Playbooks, Content, Inbox-Import | Auto-Publish | Agent-JSON, Newsletter, E-Mail | Inbox-Vorschläge | Regisseur-Inbox |
| **B** | QS vor Inbox | Publish | Lieferungs-JSON v3 | validiert / blockiert | Rot → keine Standard-Freigabe |
| **C** | CLI + REST API | Auto-Publish | API-Key, JSON | validate/submit | Submit → Inbox only |
| **D** | DAR Pipeline | Zweite Runtime, Publish | Tasks, routing.json | Runtime-Output, optional inbox_id | ADR-0010, ADR-0004 |
| **E** | Graph-Schema, Retrieval-Contracts | Graph-Runtime, Chroma in KP | Playbooks, Wiki, ADRs | Graph-Beispiele, Context-Spec | Kein Bypass DAR/Inbox |
| **F** | Agent-Policies, Scheduler-Spec | Auto-Publish, Runtime-Duplikat | Policies, Graph-Kontext | Vorschläge, Lern-Log | ADR-0012, Inbox für externe Wirkung |

---

## Stufe A — Knowledge Layer

### Ziel

Externe und interne Agenten liefern strukturiertes Wissen; Regeln und Inhalte sind **versioniert und maschinenlesbar** — Grundlage für alle Folgestufen.

### Definition of Done

| Kriterium | Status |
|-----------|--------|
| Playbooks (YAML) + Langtexte (Markdown) kanonisch in KP | ✅ |
| JSON-Import in Regisseur-Inbox (`data/agenten/inbox/`) | ✅ |
| Morgen-Lauf: `sync_aus_inbox_ordner()` | ✅ |
| Newsletter → Inbox (A3) | ✅ |
| E-Mail-Ordner-Import (A4, dateibasiert) | ✅ |
| Keine Auto-Veröffentlichung LinkedIn | ✅ |
| Manuelle Freigabe-UI | ✅ |

### Contracts (KP)

| Artefakt | Pfad |
|----------|------|
| Playbooks | `playbooks/*.yaml` |
| Langtexte | `content/playbooks/*.md` |
| Beispiele | `examples/presseschau/` |

### App (Digiwiz)

| Modul | Rolle |
|-------|--------|
| `agent_lieferung.py` | Envelope, Sync |
| `regisseur_inbox.py` | Freigabe-Hub |
| `newsletter_inbox.py` | A3 |
| `agent_mail_eingang.py` | A4 |
| `morgen_briefing.py` | Auto-Import |

### Verfahren

- [presseschau_stufe_a_checkliste.md](verfahren/presseschau_stufe_a_checkliste.md)

### Offen / Nachziehen

- [ ] `brandvoice_korpus` vollständig auf `knowledge_paths` (Legacy-Pfade deprecaten)
- [ ] Planungsdoc `docs/planung-digiwiz.md` M2-Stand (niedrige Priorität)

---

## Stufe B — Qualitätssicherung

### Ziel

Jede Agenten-Lieferung wird **vor** der Inbox auf Schema, Quellen, Dubletten und Brandvoice geprüft. Rot blockiert Standard-Freigabe.

### Definition of Done

| Kriterium | Status |
|-----------|--------|
| Schema v3 strikt (`agent-lieferung.v3`) | ✅ |
| URL-Prüfung (ok/gelb/rot) | ✅ |
| Dubletten-Fingerabdruck | ✅ |
| Brandvoice-Ampel in `meta` | ✅ |
| Import-Protokoll `import_log.json` | ✅ |
| Tests `test_presseschau_stufe_b` | ✅ |

### Contracts (KP)

| Artefakt | Pfad |
|----------|------|
| Lieferungs-Schema | `schemas/agent-lieferung.v3.json` |
| QS-Verfahren | `docs/verfahren/presseschau_qualitaetssicherung.md` |
| Negative Beispiele | `examples/presseschau/fehlerhaft_schema.json`, `defekte_url.json` |

### App (Digiwiz)

| Modul | Rolle |
|-------|--------|
| `agent_lieferung_validierung.py` | QS-Kern |
| `brandvoice_pruefung.py` | Ampel |

### Geplant (inkrementell)

- [ ] QS-Regeln aus Python nach KP `quality/` extrahieren (deklarativ, ADR-0007)
- [ ] Vollständiges JSON Schema (nicht nur Metadaten-Stub)

---

## Stufe C — CLI / Agenten-API

### Ziel

Externe KI-Systeme binden sich **kontrolliert** an — per CLI und REST, mit API-Key, ohne Auto-Publish.

### Definition of Done

| Kriterium | Status |
|-----------|--------|
| CLI `digiwiz-agent` (validate, submit, playbooks) | ✅ |
| REST `/api/v1/status`, `/playbooks`, `/agenten/*` | ✅ |
| API-Key-Auth (`DIGIWIZ_API_KEY`) | ✅ |
| Ops-Monitor, API-Log | ✅ |
| Tests `test_agent_api_stufe_c` | ✅ |
| OpenAPI-Contract in KP | ⏳ |

### Contracts (KP)

| Artefakt | Pfad | Status |
|----------|------|--------|
| Verfahren | `docs/verfahren/digiwiz_agent_api.md` | ✅ |
| API-Vertrag (OpenAPI) | `contracts/api/` | ⏳ |
| Playbook-Auslieferung | `playbooks/` | ✅ |

### App (Digiwiz)

| Modul | Rolle |
|-------|--------|
| `digiwiz_agent.py` | CLI |
| `11_wiki_api.py` | FastAPI |
| `agent_lieferung_service.py` | Validate/Submit |
| `agent_playbooks.py` | Playbook-JSON |

### Geplant

- [ ] `contracts/api/openapi-agent-v1.yaml` aus Verfahren ableiten
- [ ] MCP-Adapter (ADR-0001) — **nach** stabilem OpenAPI-Contract

---

## Stufe D — AI Runtime (DAR)

### Ziel

Digiwiz als **AI Director**: Task → Routing → Playbooks → Provider → Validator → Regisseur-Inbox.

### Definition of Done

| Kriterium | Status |
|-----------|--------|
| Task/Agent/Model Registry | ✅ |
| Routing Engine + `runtime/routing.json` | ✅ |
| Provider-Abstraktion (Mock, OpenAI, …) | ✅ |
| Pipeline + Memory + Telemetry | ✅ |
| REST `/api/v1/runtime/*` | ✅ |
| `submit_inbox: true` → Inbox | ✅ |
| Tests `test_ai_runtime_stufe_d` | ✅ |
| Prompt-Schemas in KP | ⏳ |
| MCP Runtime-Tools | ⏳ |

### Contracts (KP)

| Artefakt | Pfad | Status |
|----------|------|--------|
| Runtime-Routing | `runtime/routing.json` | ✅ |
| Verfahren | `docs/verfahren/digiwiz_ai_runtime.md` | ✅ |
| Prompt-Schemas | `schemas/prompts/` | ⏳ |

### App (Digiwiz)

| Modul | Rolle |
|-------|--------|
| `digiwiki/ai_runtime/` | Pipeline, Provider, API-Routes |

### Geplant

- [ ] Prompt-Schema pro Task (`presseschau`, `linkedin_post`, …)
- [ ] Runtime-API in `contracts/api/` ergänzen
- [ ] MCP: `digiwiz_runtime_task` als Adapter auf Pipeline (ADR-0001)

---

## Stufe E — Knowledge Graph

### Ziel

Wissensbeziehungen **explizit modellieren** (Entitäten, Kanten, Provenienz) — Grundlage für bessere Kontextwahl, RAG und spätere Autonomie.

**Architektur (ADR-0008, ADR-0009):** Knowledge Graph als **Erweiterung der Knowledge Platform** — **keine neue Runtime**. Chroma/RAG ist **abgeleiteter semantischer Index**, nicht SSOT. DAR Context Builder kombiniert später Graph- und RAG-Kontext.

### Voraussetzungen (vor Start)

- [x] Migration KP v1.0.0 abgeschlossen
- [x] Lose Repo-Kopplung (`DIGIWIZ_KNOWLEDGE_ROOT`, ADR-0006)
- [x] Contract-Modell definiert (ADR-0007)
- [x] ADR-0008: Graph = KP-Erweiterung, nicht neue Runtime
- [x] ADR-0009: Graph + Chroma/RAG — Rollen, kein Chroma in KP
- [ ] Freigabe durch Maintainer / Architektur-Review für E1-Implementierung

### Contracts (KP) — kanonisch

| Artefakt | Pfad | Beschreibung |
|----------|------|--------------|
| Graph-Schema | `schemas/graph/` | Knoten, Kanten, Typen |
| Abfrage-Verträge | `contracts/graph/` | Deklarative Queries (TBD) |
| Retrieval-Policy | `contracts/retrieval/` | Merge Graph↔RAG, Limits, Provenienz (ADR-0009) |
| Beispiele | `examples/graph/` | Referenz-Graph |
| Provenienz | Schema + ADR-0008/0009 | Quelle, Vertrauen, Zeitstempel |

### App-Integration — Konsument, nicht Runtime

| Komponente | Rolle |
|------------|--------|
| Graph-Loader | Lädt KP-Schema; optional persistenter Store in App |
| Chroma/RAG (bestehend) | Semantischer Index — **abgeleitet**, rebuild-fähig, nicht SSOT |
| `context_builder` (DAR) | **Kombiniert** Playbooks + Graph-Kontext + RAG-Kontext (ADR-0009) |
| Kein `graph_runtime/` / `rag_runtime/` | ❌ bewusst ausgeschlossen (ADR-0008, ADR-0009) |
| Kein Auto-Publish | Unverändert ADR-0004 |
| Regisseur-Inbox | Unverändert Freigabe-Hub ADR-0002 |

### Nicht in Stufe E

- Neue Runtime-Schicht parallel zu `ai_runtime/`
- Eigener Graph-API-Server
- **Chroma-Implementierung oder -Migration in KP** (ADR-0009)
- Chroma als SSOT — bei Konflikt gilt KP-Contract
- Git-Submodule (Re-Evaluation **nach** E, ADR-0006)
- Ersetzen der Regisseur-Inbox

### Meilensteine (Entwurf)

1. **E1** — Graph-Schema + ADR, Beispiel-Graph in `examples/graph/`
2. **E2** — Import aus Wiki/Playbooks (read-only)
3. **E3** — DAR Context Builder: Graph-Kontext + Chroma/RAG-Kontext (ADR-0009)
4. **E4** — Contract-Tests + Integrations-Tests
5. **E5** — Re-Evaluation Submodule / Deployment-Modell

---

## Stufe F — Autonome Agenten

### Ziel

Agenten arbeiten **selbstständiger** (Planung, Wiederholung, Feedback-Schleifen) — innerhalb klarer **Policy-Contracts** und weiterhin mit Regisseur-Freigabe für externe Wirkung.

### Leitplanken (verbindlich)

- ADR-0004: Keine Auto-Veröffentlichung — Stufe F **erweitert** ADR-0004, überschreibt es nicht
- ADR-0002: Regisseur-Inbox bleibt Hub für alle extern sichtbaren Inhalte
- Freigabe-Policies als Contracts in KP, nicht nur Code

### Geplant (grobe Roadmap)

| Thema | KP | App |
|-------|-----|-----|
| Agent-Policy-Contracts | `contracts/policies/` | Policy-Engine |
| Scheduler / Nacht-Jobs | Verfahren | Task Orchestrator |
| Feedback aus Verwerfen-Gründen | Schema | Lern-Log (ohne Auto-Publish) |
| Multi-Agent-Koordination | ADR | Runtime-Erweiterung |

### Abhängigkeit

**Stufe F startet erst nach abgeschlossener Stufe E** — Graph liefert Kontext und Provenienz für verantwortungsvolle Autonomie.

---

## Querschnitt — alle Stufen

### Binding App ↔ Knowledge Platform

```
DIGIWIZ_KNOWLEDGE_ROOT → knowledge_paths.py → Contracts laden
Fallback: knowledge-platform/ (Monorepo) → firmenapp/config/ (Legacy)
Version-Pin: digiwiki/knowledge_lock.json ↔ KP VERSION
```

### Teststrategie

| Ebene | Ort | Prüft |
|-------|-----|--------|
| Contract | `knowledge-platform/tests/` | Artefakte vollständig, konsistent |
| Integration | `digiwiki/tests/test_*_stufe_*` | App lädt und wendet Contracts an |

### Dokumentations-Index

| Stufe | Verfahren / Doc |
|-------|-----------------|
| A | [presseschau_stufe_a_checkliste.md](verfahren/presseschau_stufe_a_checkliste.md) |
| B | [presseschau_qualitaetssicherung.md](verfahren/presseschau_qualitaetssicherung.md) |
| C | [digiwiz_agent_api.md](verfahren/digiwiz_agent_api.md) |
| D | [digiwiz_ai_runtime.md](verfahren/digiwiz_ai_runtime.md) |
| E–F | dieses Dokument + künftige ADRs |

### ADRs

| ADR | Relevanz |
|-----|----------|
| 0001 | REST vor MCP (C, D) |
| 0002 | Regisseur-Inbox (alle) |
| 0003 | Playbooks SSOT (A) |
| 0004 | Keine Auto-Publish (alle, besonders F) |
| 0005 | KP getrennt von Runtime (E) |
| 0006 | Kein Submodule bis nach E |
| 0007 | Contracts als SSOT (alle) |
| 0008 | Knowledge Graph = KP-Erweiterung, keine neue Runtime (E) |
| 0009 | Graph + Chroma/RAG — Rollen, Retrieval-Policy in KP (E) |
| 0010 | DAR als einzige AI Runtime (D, E) |
| 0011 | Context Builder kombiniert kanonisch + Graph + RAG (D, E) |
| 0012 | Contracts vor E/F-Automation (E, F) |

---

## Dual-Repo-Synchronisation (Entwicklungsplan)

**Es gibt keine automatische Synchronisation** zwischen den Repositories. Bis zur Re-Evaluation nach Stufe E (ADR-0006) gelten zwei parallele Arbeitskopien:

| Repository | Rolle | URL |
|------------|-------|-----|
| **Digiwiz-Knowledge-Platform** | Kanonisch — Contracts, ADRs, Roadmap | `github.com/HansKohlhaas/Digiwiz-Knowledge-Platform` |
| **Digiwiz** (Monorepo) | App + optionale KP-Kopie unter `knowledge-platform/` | `github.com/HansKohlhaas/Digiwiz` |

### Regel: KP-Repo zuerst

1. Änderung an Contracts/ADRs/Roadmap **zuerst** im KP-Repo committen und pushen
2. Dieselben Dateien nach `knowledge-platform/` im Monorepo übernehmen (manuell oder Copy-Script)
3. `VERSION` in KP und `digiwiki/knowledge_lock.json` in der App abstimmen
4. Contract-Tests in beiden Kontexten grün:
   - KP: `python -m unittest tests.test_contract -v`
   - App: `python -m unittest tests.test_knowledge_platform -v`

### Was wohin gehört

| Nur KP-Repo | Nur Digiwiz-Monorepo | Beide (spiegeln) |
|-------------|---------------------|------------------|
| ADRs, Roadmap, `contracts/` | `digiwiki/`, `firmenapp/`, UI | `playbooks/`, `schemas/`, `runtime/`, `docs/verfahren/` (KP-Anteil) |
| `meta/manifest.yaml` | `knowledge_paths.py`, Tests App | `VERSION` ↔ `knowledge_lock.json` |

### Abgleich-Checkliste (bei jedem KP-Release)

- [ ] `VERSION` und `CHANGELOG.md` in KP erhöht
- [ ] `digiwiki/knowledge_lock.json` auf gleiche Version
- [ ] KP-Repo gepusht
- [ ] Monorepo `knowledge-platform/` nachgezogen und gepusht
- [ ] Contract- + Integrations-Tests grün

### Bis Stufe E

- **Kein Git-Submodule** — lose Kopplung über `DIGIWIZ_KNOWLEDGE_ROOT` (ADR-0006)
- Divergenz ist toleriert, aber **nicht ignoriert** — `VERSION`/`knowledge_lock` machen Drift sichtbar
- Nach Stufe E: Submodule oder „nur externes KP-Repo“ neu bewerten

---

## Nächste Schritte (priorisiert)

1. ~~ADR-0006 + ADR-0007 + Roadmap in beide Repos~~ → siehe Abschnitt *Dual-Repo-Synchronisation*
2. OpenAPI für Stufe C (`contracts/api/`)
3. Prompt-Schemas für Stufe D (`schemas/prompts/`)
4. **Stufe E — Freigabe einholen**, dann E1 (Graph-Schema)
5. Nach E: Submodule-Re-Evaluation (ADR-0006)
