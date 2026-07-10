# Codex Review KP v1.5.0

Datum: 2026-07-10  
Scope: Architektur- und Contract-Review von KP v1.5.0 mit Fokus auf ADR-0014 Decision Engine, Decision-Engine-Contracts, Context Assembly, Source Resolution/SQL-first, Graph, Chroma/RAG, Governance, Manifest, Roadmap, Changelog und Tests.

## Prüfgrundlage

Geprüfte Kernartefakte:

- `VERSION`, `CHANGELOG.md`, `meta/manifest.yaml`
- `adr/ADR-0014-decision-engine-orchestration.md`
- `docs/14_decision_engine.md`
- `contracts/decision-engine/`
- `examples/decision-engine/`
- `playbooks/presseschau.yaml`, `schemas/playbook.schema.json`
- `contracts/source-resolution/`, `docs/12_context_assembly_pipeline.md`, `docs/13_source_resolution.md`
- `contracts/retrieval/`, `contracts/graph/`, Graph-/Chroma-Schemas und Beispiele
- `docs/10_contracts.md`, `docs/11_roadmap_stufen_a_f.md`
- `tests/test_contract.py`, `tests/test_governance.py`

Ausgeführte Prüfung:

```bash
python -m unittest tests.test_contract tests.test_governance -v
```

Ergebnis: 38 Tests, alle erfolgreich.

## Festgestellte Probleme

1. Decision Engine, Source Resolution und Context Assembly sind grundsätzlich sauber getrennt, aber die Übergabegrenzen sind noch nicht streng genug maschinenlesbar verknüpft. `decision_context.schema.json` beschreibt den Plan, `context_assembly.schema.json` beschreibt die gefüllten Felder, aber es gibt keinen verpflichtenden `decision_context_ref` im Context-Assembly-Contract.

2. Reason-Codes sind in `decision_policy.yaml` definiert, aber die Decision-Schemas validieren sie nur als freie Strings. Dadurch kann ein Beispiel formal gültig sein, obwohl ein `reason_code` nicht im Policy-Katalog existiert.

3. `source_requirements` wird in `decision_output.schema.json` und `decision_context.schema.json` strukturell dupliziert. Die Duplizierung ist nachvollziehbar, weil Output und Downstream-Kontext unterschiedliche Artefakte sind, birgt aber Drift-Risiko.

4. `required_fields` existiert in Decision Output, Decision Context, Context Builder Input und Context Assembly. Das ist fachlich sinnvoll, aber noch nicht als ein gemeinsam versionierter Feld-Subcontract modelliert.

5. `decision_hints` sind aktuell nur im Presseschau-Playbook konkret belegt. Die Policy spricht allgemein von Playbook-Hints; für Playbooks ohne Hints ist der Fallback nicht maschinenlesbar dokumentiert.

6. `decision_output.decisions.answer_generation_allowed` kann bereits `true` sein, obwohl Source Resolution und Context Assembly noch nicht ausgeführt wurden. Das ist als "später erlaubt, sofern Downstream erfolgreich ist" interpretierbar, aber der Name kann als sofortige Provider-Freigabe missverstanden werden.

7. `decision_context.next_stage` erlaubt `approval_gate`, aber die Beispiele zeigen primär `source_resolution`. Es fehlt ein Beispiel für `clarification`, `approval_gate` oder `block`.

8. Die Decision Engine darf keine Retrieval-Abfragen ausführen, plant aber optionale Quellen wie `chroma_rag` und `web_external`. Der Unterschied zwischen "optional geplant" und "tatsächlich auszuführen" ist in den Schemas nur über `status` und `orchestration_plan.condition` abgebildet, nicht über eine verbindliche Eskalationsregel.

9. ADR-0014 datiert in der Historie auf 2026-07-09, während Changelog v1.5.0 auf 2026-07-10 steht. Das ist kein inhaltlicher Fehler, aber für Release-Nachvollziehbarkeit leicht irritierend.

## Risiken

1. Ohne verpflichtenden Decision-Context-Verweis in der Context Assembly kann eine spätere App-Implementierung die Decision Engine umgehen und trotzdem formal gültige Assembly-Artefakte erzeugen.

2. Freie Reason-Code-Strings schwächen die Auditierbarkeit. Ein Trace kann vollständig aussehen, ohne tatsächlich auf katalogisierte Reason-Codes zurückzugreifen.

3. Duplizierte Teilstrukturen erhöhen die Gefahr, dass Decision Output, Decision Context und Context Assembly bei künftigen Erweiterungen auseinanderlaufen.

4. `answer_generation_allowed` kann zu früh als grünes Licht für Provider-Aufruf interpretiert werden. Die eigentliche harte Grenze liegt erst nach Source Resolution und Context Assembly.

5. Wenn `decision_hints` nur punktuell gepflegt werden, könnte die Decision Engine bei anderen Tasks still auf generische Regeln fallen. Das ist akzeptabel, muss aber explizit und testbar sein.

6. Fehlende Negativ-/Grenzfallbeispiele erschweren die spätere App-Implementierung: Missing Entity, SQL leer, Governance-Block, Auto-Publish-Versuch und Quellenkonflikt sind die riskanten Pfade.

7. Chroma/RAG bleibt korrekt als abgeleitet beschrieben. Das Risiko liegt nicht in der Architektur, sondern in der späteren Ausführung: optionale RAG-Planung darf SQL-first-Felder nicht indirekt füllen.

## Verbesserungsvorschläge

1. Einen kleinen gemeinsamen Subcontract für `required_fields` und `source_requirements` einführen oder die Wiederverwendung per `$defs`/Referenz stärker vereinheitlichen.

2. `reason_code` gegen einen maschinenlesbaren Katalog validierbar machen. Praktisch wäre ein `reason_codes.schema.json` oder eine aus `decision_policy.yaml` generierte Testprüfung.

3. `decision_context_ref` in `context_assembly.schema.json` als optionales Feld ergänzen und perspektivisch für Decision-Engine-Pfade verpflichtend machen.

4. `answer_generation_allowed` umbenennen oder semantisch schärfen, z. B. `answer_generation_allowed_after_context_assembly`, oder zusätzlich `provider_call_allowed: false` bis Assembly abgeschlossen ist.

5. Fallback-Verhalten für Playbooks ohne `decision_hints` dokumentieren: generische Decision Policy, keine task-spezifische SQL-Erweiterung, Governance trotzdem Pflicht.

6. Decision-Beispiele um Negativ- und Eskalationsfälle erweitern:
   - fehlende Kundennummer bei operational lookup
   - SQL-first, aber SQL leer
   - Auto-Publish-Anforderung
   - Graph erforderlich
   - RAG nur optional, nicht kanonisch

7. In Tests zusätzlich prüfen, dass alle Reason-Codes aus Beispielen in `decision_policy.yaml` existieren.

8. In Tests zusätzlich prüfen, dass `decision_output.source_requirements` und `decision_context.source_requirements` für dasselbe Beispiel identisch sind.

## Notwendige Contract-Anpassungen

1. `contracts/decision-engine/decision_output.schema.json`
   - `reason_code` perspektivisch an einen Reason-Code-Katalog binden.
   - Semantik von `answer_generation_allowed` präzisieren.
   - Optional eine Bedingung ergänzen: `sql_required: true` muss `sql_crm_stammdaten.status: required` erzwingen.

2. `contracts/decision-engine/decision_context.schema.json`
   - `policy_refs` um `decision_trace_ref` oder `decision_output_ref` erweitern, falls Downstream vollständige Audit-Kette braucht.
   - Source-Requirement-Struktur möglichst mit Decision Output teilen.

3. `contracts/source-resolution/context_assembly.schema.json`
   - `decision_context_ref` oder `decision_id` ergänzen, damit Assembly auf die Entscheidung rückführbar ist.
   - Optional `source_requirements_ref` ergänzen, um die geplante Quelleneskalation mit der tatsächlichen Feldfüllung abzugleichen.

4. `schemas/playbook.schema.json`
   - `decision_hints` stärker typisieren, insbesondere `clarification_triggers`.
   - `preferred_sources` in `decision_hints` auf dieselben Enums wie Context Assembly begrenzen.

5. `contracts/decision-engine/decision_policy.yaml`
   - Fallback-Regel für Playbooks ohne `decision_hints` explizit aufnehmen.
   - Reason-Code für `no_structural_query_type` ergänzen, da dieser im Beispiel verwendet wird, aber im sichtbaren Reason-Code-Katalog nicht definiert ist.
   - Reason-Code `sql_first_overrides_rag_for_operational_facts` ergänzen, da er in `rejected_alternatives` verwendet wird.

## Notwendige Tests

1. Test: Alle `reason_code`-Werte in Decision Output, Decision Context und Decision Trace müssen in `decision_policy.yaml.reason_codes` existieren.

2. Test: Alle `rejected_alternatives[].reason_code` müssen ebenfalls im Reason-Code-Katalog existieren.

3. Test: Decision Output und Decision Context bleiben synchron für `source_requirements`, `required_fields`, `governance` und `next_stage`.

4. Test: Wenn `sql_required` true ist, muss `source_requirements.sql_crm_stammdaten.status` `required` sein und `resolution_policy_ref` auf ADR-0013-Policy zeigen.

5. Test: Wenn `auto_publish_allowed` nicht false ist oder Auto-Publish angefordert wird, muss `block_execution` oder `approval_required` greifen.

6. Test: Context Assembly mit Decision-Engine-Pfad muss `decision_context_ref` enthalten, sobald die App-Implementierung diesen Pfad nutzt.

7. Test: Negative Beispiele für `clarification`, `approval_gate` und `block` validieren gegen die Schemas.

8. Test: Playbooks ohne `decision_hints` verwenden dokumentierten Fallback und bleiben gültig.

## Priorisierte To-do-Liste

1. Reason-Code-Katalog mit Beispielen synchronisieren (`no_structural_query_type`, `sql_first_overrides_rag_for_operational_facts`).

2. Tests für Reason-Code-Existenz und Trace-Vollständigkeit ergänzen.

3. `decision_context_ref`/`decision_id` in Context Assembly ergänzen, damit Decision → Assembly auditierbar geschlossen ist.

4. Semantik von `answer_generation_allowed` schärfen, damit keine vorzeitige Provider-Freigabe entsteht.

5. Gemeinsame Teilstrukturen für `source_requirements` und `required_fields` konsolidieren.

6. Fallback-Regeln für Playbooks ohne `decision_hints` dokumentieren und testen.

7. Negativ- und Eskalationsbeispiele für Decision Engine ergänzen.

8. `decision_hints` im Playbook-Schema enger typisieren.

## Gesamtbewertung

KP v1.5.0 hält die wesentlichen Architekturgrenzen ein:

- Decision Engine entscheidet, führt aber nicht aus.
- Source Resolution bleibt für Quellenabfrage und SQL-first zuständig.
- Context Assembly sammelt und bewertet Felder vor Antwortgenerierung.
- Context Builder baut Provider-Kontext, keine eigene Runtime.
- DAR bleibt die einzige AI Runtime.
- Graph und Chroma/RAG bleiben Kontextlieferanten; Chroma ist nicht kanonisch.
- Governance und `auto_publish: false` sind weiterhin konsistent abgesichert.

Die größten offenen Punkte liegen nicht in der Grundarchitektur, sondern in der maschinenlesbaren Audit-Kette und der Vermeidung von Drift zwischen ähnlichen Contract-Strukturen.
