# Digiwiz Knowledge Platform

Zentrale, versionierte **Quelle für Regeln und Schnittstellen (Contracts)** für Digiwiz — keine Produktiv-Runtime.

Nicht nur Dokumentation: **Playbooks, JSON-Schemas, Prompt-Schemas, API-Verträge, Runtime-Konfiguration und ADRs** sind maschinenlesbare, versionierte Verträge (ADR-0007).

## Rolle

| Dieses Repo | Digiwiz App (`digiwiki/`, `firmenapp/`) |
|-------------|----------------------------------------|
| **Contracts:** Playbooks, Schemas, API-Specs, Runtime-JSON, ADRs | Ausführung, Validierungscode, UI |
| Beispiele (`examples/`) | Laufzeit (`data/`) |

**Prinzip:** KI bereitet vor → **Regisseur-Inbox** → Hans gibt frei → **keine Auto-Veröffentlichung**.

## Stufenmodell

| Stufe | Inhalt | Ort |
|-------|--------|-----|
| A | Knowledge Layer | `playbooks/`, `content/` |
| B | Qualitätssicherung | `schemas/`, `docs/verfahren/` |
| C | CLI/API | dokumentiert, Code in App |
| D | AI Runtime | `runtime/`, Code in App |
| E | Knowledge Graph | ⏳ [Roadmap](docs/11_roadmap_stufen_a_f.md) · [Architektur-Schichten](docs/12_architecture_layers.md) |
| F | Autonome Agenten | 📋 [Roadmap](docs/11_roadmap_stufen_a_f.md) |

**Abgrenzung Stufe E:** Knowledge Graph erweitert die **Knowledge Platform** (Schemas, Provenienz) — nicht die App-Runtime. **DAR** bleibt einzige AI Runtime; **Chroma/RAG** ist abgeleiteter Index in der App; **SQL/CRM** ist SSOT für Firmendaten (**ADR-0013**).

## Schnellstart

1. Lesen: [00_START_HERE.md](00_START_HERE.md)
2. **Roadmap:** [docs/11_roadmap_stufen_a_f.md](docs/11_roadmap_stufen_a_f.md)
3. **Context Assembly:** [docs/12_context_assembly_pipeline.md](docs/12_context_assembly_pipeline.md) — Pipeline vor Antwort (ADR-0011)
4. **Source Resolution:** [docs/13_source_resolution.md](docs/13_source_resolution.md) — SQL-first (ADR-0013)
5. **Contracts:** [docs/10_contracts.md](docs/10_contracts.md) · [contracts/](contracts/)
6. ADRs: [adr/](adr/) ([Index](adr/README.md))
7. Playbooks: [playbooks/](playbooks/)
8. App-Einbindung: `digiwiki/knowledge_paths.py` + `digiwiki/knowledge_lock.json`

## Version

Siehe [VERSION](VERSION) und [CHANGELOG.md](CHANGELOG.md).

## Next Actions

1. ~~Migration Playbooks/Schemas aus Digiwiz-Monorepo~~ (v1.0.0)
2. Contract-Tests in `tests/` erweitern
3. Regeln aus Python nach `quality/` extrahieren (inkrementell)
4. **Stufe E — Knowledge Graph** (nach Freigabe, siehe [docs/11_roadmap_stufen_a_f.md](docs/11_roadmap_stufen_a_f.md))

## Einbindung in Digiwiz App

```env
# Kanonisch: geklontes KP-Repo (eigenständiges Repository)
DIGIWIZ_KNOWLEDGE_ROOT=C:\Pfad\zu\Digiwiz-Knowledge-Platform

# Optional — nur Monorepo-Entwicklung: Default knowledge-platform/ neben digiwiki/
```

**Kein Git-Submodule** (vorläufig) — siehe [ADR-0006](adr/ADR-0006-no-git-submodule-until-stage-e.md).  
Binding nur über Pfad + `knowledge_lock.json`, nicht über Repo-Verschachtelung.

Ohne Env-Variable nutzt die App `knowledge-platform/` im Monorepo, mit Fallback auf Legacy-Pfade unter `firmenapp/config/`.
