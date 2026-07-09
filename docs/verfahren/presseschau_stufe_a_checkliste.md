---
title: Presseschau — Stufe A Checkliste
slug: presseschau-stufe-a-checkliste
category: Verfahren
audience: admin
version: "2026-07-09"
order: 5
knowledge_platform: "1.0.0"
---

# Stufe A — Definition of Done vs. Ist-Stand

Folgestufen: [Stufe B](presseschau_qualitaetssicherung.md) · [Stufe C](digiwiz_agent_api.md) · [Stufe D](digiwiz_ai_runtime.md)

## Gesamt-DoD Stufe A

| # | Kriterium | Ist |
|---|-----------|-----|
| A0 | Externe Agenten liefern JSON per Datei | ✅ |
| A0 | Import in Regisseur-Inbox | ✅ |
| A0 | Keine Auto-Veröffentlichung LinkedIn | ✅ |
| A0 | Manuelle Freigabe-UI | ✅ |
| A0 | „Heute dran“ mit Begründung | ✅ |

## A1 — Playbook

| | |
|---|---|
| **Kanonisch** | `content/playbooks/linkedin-presseschau.md` |
| **YAML** | `playbooks/presseschau.yaml`, `playbooks/linkedin.yaml` |
| **Legacy** | `docs/wiki/.../linkedin-presseschau.md` (Fallback brandvoice_korpus) |

## A3 — Newsletter → Inbox

✅ `digiwiki/newsletter_inbox.py` — kein Auto-Versand

## A4 — E-Mail-Eingang

✅ `digiwiki/agent_mail_eingang.py` — `data/agenten/mail_inbox/`

## Stufenüberblick

| Stufe | Status |
|-------|--------|
| A | ✅ |
| B | ✅ |
| C | ✅ |
| D | ✅ |
| E | ⏳ nach Migration |
| F | Roadmap |

## Tests

```cmd
cd c:\Digiwiz\digiwiki
python -m unittest tests.test_stufe_a_a3_a4 tests.test_presseschau_stufe_b -v
```
