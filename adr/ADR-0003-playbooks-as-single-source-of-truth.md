# ADR-0003: Playbooks als Single Source of Truth

## Status

Akzeptiert (2026-07-09)

## Kontext

Playbook-Regeln lagen verteilt in `firmenapp/config/playbooks/`, `docs/wiki/.../Playbooks/` und Python-Code.

## Entscheidung

1. **Digiwiz Knowledge Platform** ist kanonische Quelle für **Contracts** (ADR-0007):
   - `playbooks/*.yaml`, `content/playbooks/*.md`
   - `schemas/`, `runtime/`, `examples/`
   - künftig: `schemas/prompts/`, `contracts/api/`
2. Digiwiz App lädt über `knowledge_paths.py` mit **Fallback** auf Legacy-Pfade
3. Regeländerungen erfolgen primär in Contract-Artefakten, nicht nur im Code

Siehe auch: [ADR-0007](ADR-0007-contracts-as-binding-artifacts.md)

## Konsequenzen

- Versionierung und Changelog im Knowledge-Repo
- `digiwiki/knowledge_lock.json` pinnt kompatible Version
- Legacy-Dateien bleiben bis Deprecation-Phase als Fallback
