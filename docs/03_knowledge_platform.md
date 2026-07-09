# Knowledge Platform — Rolle und Grenzen

Dieses Repository ist **Single Source of Truth** für:

- `playbooks/` — maschinenlesbare Regeln (YAML)
- `content/playbooks/` — kanonische Langtexte (Markdown)
- `schemas/` — Lieferungs- und Datenverträge
- `runtime/` — AI-Routing-Konfiguration (keine Ausführung)
- `adr/` — Architekturentscheidungen
- `examples/` — gültige und fehlerhafte Beispieldaten

**Nicht enthalten:** Python-Runtime, Streamlit-UI, Provider-Code, `data/`.

Binding zur App: `digiwiki/knowledge_paths.py`, Env `DIGIWIZ_KNOWLEDGE_ROOT`.

Siehe ADR-0003 und ADR-0005.
