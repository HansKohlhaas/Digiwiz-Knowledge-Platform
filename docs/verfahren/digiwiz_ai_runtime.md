---
title: Digiwiz AI Runtime (Stufe D)
slug: digiwiz-ai-runtime
category: Verfahren
audience: admin
version: "2026-07-09"
order: 12
knowledge_platform: "1.0.0"
---

# Digiwiz AI Runtime (DAR) — Stufe D

Digiwiz fungiert als **AI Director**: für jede Aufgabe wählt die Runtime Agent, Modell und Playbooks — Ergebnisse landen nach Validierung in der **Regisseur-Inbox** (keine Auto-Veröffentlichung).

## Vision

```
Task → Routing → Playbooks → Memory → Kontext → KI → Validator → Regisseur-Inbox
```

## Kernmodule (Digiwiz App)

| Modul | Datei | Rolle |
|-------|--------|--------|
| Routing Engine | `ai_runtime/routing_engine.py` | Agent/Modell/Playbooks |
| Playbook Loader | `ai_runtime/playbook_loader.py` | YAML + Markdown |
| Pipeline | `ai_runtime/pipeline.py` | Orchestrierung |

## Konfiguration (Knowledge Platform)

`runtime/routing.json` — Routing-Regeln pro Task.  
Fallback: `firmenapp/config/ai_runtime.json`.

## REST-Endpunkte

| Methode | Pfad | Auth |
|---------|------|------|
| GET | `/api/v1/runtime/status` | nein |
| GET | `/api/v1/runtime/models` | nein |
| POST | `/api/v1/runtime/task` | ja |

`submit_inbox: true` → Validierung → Regisseur-Inbox (`inbox_id` in Response).

## MCP

Vorbereitet (`mcp.enabled: false`), nicht implementiert — ADR-0001.

## Tests

```cmd
cd c:\Digiwiz\digiwiki
python -m unittest tests.test_ai_runtime_stufe_d -v
```

Siehe auch: [digiwiz_agent_api.md](digiwiz_agent_api.md), [presseschau_qualitaetssicherung.md](presseschau_qualitaetssicherung.md)
