# Cursor — Stufe E (Knowledge Graph)

**Status:** ⏳ nach Architektur-Freigabe  
**Voraussetzung:** ADR-0008, ADR-0009, ADR-0010, ADR-0011, ADR-0012, Contracts in `schemas/`

## Ziel

Knowledge Graph als **Erweiterung der Knowledge Platform** — kein neues Entscheidungssystem, keine zweite Runtime.

## Nicht-Ziele

- Kein `graph_runtime/` parallel zu `digiwiki/ai_runtime/`
- Keine Chroma-DB oder Vektor-Store-Implementierung in KP
- Kein Auto-Publish, kein Umgehen der Regisseur-Inbox (ADR-0002, ADR-0004)
- Kein Git-Submodule (ADR-0006)

## Eingänge

| Quelle | Pfad |
|--------|------|
| Playbooks | `playbooks/` |
| ADRs | `adr/` |
| Graph-Schemas | `schemas/knowledge_graph_*.schema.json` |
| Retrieval-Policy | `contracts/retrieval/` |

## Ausgänge

| Artefakt | Pfad |
|----------|------|
| Beispiel-Graph | `examples/graph/` |
| Abfrage-Verträge | `contracts/graph/` |
| Contract-Tests | `tests/test_governance.py` |

## Freigabegrenzen

- Alle extern sichtbaren Inhalte → **Regisseur-Inbox**
- DAR bleibt **einzige AI Runtime** (ADR-0010)
- Context Builder merged Playbooks + Graph + RAG (ADR-0011)
- Automation erst nach Contract-Abschluss (ADR-0012)

## Meilensteine

1. **E1** — `examples/graph/` + Validierung gegen Node/Edge-Schemas
2. **E2** — Import-Spec aus Wiki/Playbooks (read-only)
3. **E3** — Context-Builder-Contract in App anbinden (kein neuer Runtime-Pfad)
4. **E4** — Chroma-Manifest + Rebuild-Report in App-Prozess
5. **E5** — Submodule-Re-Evaluation (ADR-0006)

## Tests vor Merge

```bash
pip install -r requirements-dev.txt
python -m unittest tests.test_contract tests.test_governance -v
```

## Referenzen

- [docs/11_roadmap_stufen_a_f.md](../docs/11_roadmap_stufen_a_f.md)
- [docs/12_architecture_layers.md](../docs/12_architecture_layers.md)
- [ADR-0008](../adr/ADR-0008-knowledge-graph-as-platform-extension.md)
- [ADR-0012](../adr/ADR-0012-contracts-before-stage-e-f-automation.md)
