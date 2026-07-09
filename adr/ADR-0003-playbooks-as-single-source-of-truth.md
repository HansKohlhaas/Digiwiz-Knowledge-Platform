# ADR-0003: Playbooks als Single Source of Truth

## Status

Akzeptiert (2026-07-09)

## Kontext

Playbook-Regeln lagen verteilt in `firmenapp/config/playbooks/`, `docs/wiki/.../Playbooks/` und Python-Code.

## Entscheidung

1. **Digiwiz Knowledge Platform** (`knowledge-platform/`) ist kanonische Quelle für:
   - `playbooks/*.yaml`
   - `content/playbooks/*.md`
   - `schemas/`, `runtime/`, `examples/`
2. Digiwiz App lädt über `knowledge_paths.py` mit **Fallback** auf Legacy-Pfade
3. Regeländerungen erfolgen primär in YAML/Markdown, nicht nur im Code

## Konsequenzen

- Versionierung und Changelog im Knowledge-Repo
- `digiwiki/knowledge_lock.json` pinnt kompatible Version
- Legacy-Dateien bleiben bis Deprecation-Phase als Fallback
