# Verträge (Contracts)

Die Knowledge Platform definiert **verbindliche Schnittstellen** zwischen Wissen, App und externen Agenten (ADR-0007).

## Contract-Typen

### 1. Playbooks

- **Format:** YAML (`playbooks/`) + Langtext (`content/playbooks/`)
- **Verbraucher:** `agent_playbooks.py`, `ai_runtime/playbook_loader.py`, externe Agenten
- **Änderung:** Version im Playbook-YAML, Changelog in KP

### 2. JSON-Schemas

- **Format:** JSON Schema Draft 2020-12
- **Beispiel:** `schemas/agent-lieferung.v3.json`
- **Verbraucher:** `agent_lieferung_validierung.py` (Logik in App, Schema in KP)
- **Beispiele:** `examples/presseschau/`

### 3. Prompt-Schemas (geplant)

- **Format:** JSON/YAML unter `schemas/prompts/`
- **Zweck:** Einheitliche Prompt- und Kontext-Struktur für DAR
- **Status:** Stufe D/E

### 4. API-Verträge (geplant)

- **Format:** OpenAPI 3.x unter `contracts/api/`
- **Zweck:** REST-Stufe C/D — Request, Response, Auth, Fehlercodes
- **Status:** Verfahrensdoku existiert; OpenAPI folgt

### 5. Runtime-Konfiguration

- **Format:** JSON (`runtime/routing.json`)
- **Verbraucher:** `ai_runtime/routing_engine.py`
- **Hinweis:** Konfiguration, keine Pipeline-Ausführung

### 6. ADRs

- **Format:** Markdown (`adr/`)
- **Zweck:** Architektur- und Prozessverträge für Menschen und Maintainer

## Workflow: Contract first

```
1. Vertrag in KP definieren (Schema, Beispiel, ADR bei Bedarf)
2. Contract-Test in tests/
3. App implementiert / lädt über knowledge_paths.py
4. Integrations-Test in digiwiki/tests/
5. VERSION + knowledge_lock.json anheben
```

## Keine Breaking Changes

Neue Contract-Versionen (z. B. Schema v4) parallel zu Legacy; App-Fallback bis Deprecation.

Siehe auch: [03_knowledge_platform.md](03_knowledge_platform.md), [contracts/README.md](../contracts/README.md)
