# Cursor — Stufe F (Autonome Agenten)

**Status:** 📋 Roadmap — **erst nach abgeschlossener Stufe E**  
**Leitplanke:** ADR-0004 bleibt verbindlich — Stufe F erweitert, ersetzt nicht.

## Ziel

Agenten planen und wiederholen Aufgaben **innerhalb Policy-Contracts** — externe Wirkung weiterhin nur nach Regisseur-Freigabe.

## Nicht-Ziele

- Keine Auto-Veröffentlichung (LinkedIn, WordPress, externe APIs)
- Keine zweite AI Runtime neben DAR
- Keine Policies nur im Code ohne KP-Contract
- Kein Start vor E4 (Graph + Context Builder + Retrieval-Contracts)

## Eingänge

| Quelle | Pfad |
|--------|------|
| Agent-Policies | `contracts/policies/` (geplant) |
| Freigabe-Regeln | ADR-0002, ADR-0004, ADR-0012 |
| Kontext | DAR Context Builder (ADR-0011) |
| Feedback | Verwerfen-Gründe aus Inbox (Schema geplant) |

## Ausgänge

| Artefakt | Pfad |
|----------|------|
| Policy-Contracts | `contracts/policies/` |
| Verfahren | `docs/verfahren/autonome_agenten.md` (geplant) |
| ADR bei Bedarf | `adr/ADR-0013-*.md` |

## Freigabegrenzen

- **Regisseur-Inbox** für alle publish-nahen Outputs
- Scheduler/Nacht-Jobs dürfen nur **Vorschläge** erzeugen (`auto_publish: false`)
- Jede autonome Aktion muss `applied_playbooks`, `applied_adrs`, `sources`, `uncertainties` im Context-Builder-Output ausweisen
- Verstöße gegen DAR-Freigabegrenzen sind Contract-Test-Fehler

## Meilensteine (Entwurf)

1. **F1** — Policy-Schema + Beispiel-Policies in KP
2. **F2** — Scheduler-Spec (App) ohne Auto-Publish
3. **F3** — Feedback-Loop aus Inbox-Ablehnungen (Lern-Log, kein Publish)
4. **F4** — Multi-Agent-Koordination über DAR (kein paralleler Orchestrator)

## Tests vor Merge

```bash
python -m unittest tests.test_governance -v
```

Governance-Test `test_stage_e_f_docs_kein_dar_bypass` muss grün bleiben.

## Referenzen

- [docs/11_roadmap_stufen_a_f.md](../docs/11_roadmap_stufen_a_f.md)
- [ADR-0004](../adr/ADR-0004-no-auto-publishing.md)
- [ADR-0012](../adr/ADR-0012-contracts-before-stage-e-f-automation.md)
