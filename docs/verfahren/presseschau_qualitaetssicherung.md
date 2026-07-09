---
title: Presseschau — Qualitätssicherung (Stufe B)
slug: presseschau-qualitaetssicherung
category: Verfahren
audience: all
version: "2026-07-09"
order: 10
knowledge_platform: "1.0.0"
---

# Presseschau — Qualitätssicherung (Stufe B)

Qualitäts- und Freigabeprozess für externe Presseschau-Lieferungen innerhalb der **Regisseur-Inbox**. Keine Auto-Veröffentlichung auf LinkedIn.

## Datenfluss

```
ChatGPT / externer Agent
    │ JSON v3 (Pflichtfelder)
    ▼
data/agenten/inbox/*.json
    │ sync_aus_inbox_ordner() — auch Morgen-Lauf
    ▼
agent_lieferung_validierung.aufbereiten_lieferung()
    ├── Schema-Validierung (v3 strikt)
    ├── Quellen-URL-Prüfung
    ├── Dublettenprüfung
    └── Brandvoice-Ampel
    ▼
regisseur_inbox.json → Organisation → Inbox
    ├── Heute dran (tages_themen.py)
    ├── Markdown-Entwurf (docs/content/linkedin/entwuerfe/)
    └── Manuelle Freigabe (Annehmen / Trotzdem / Verwerfen)
```

## Pflichtfelder (Schema v3)

| Ebene | Feld | Bedeutung |
|-------|------|-----------|
| Envelope | `version` | `3` für strikte Prüfung |
| Envelope | `datum` | `YYYY-MM-DD` |
| Envelope | `quelle_agent` | z. B. `chatgpt-presseschau` |
| Envelope | `created_at` | ISO-Zeitstempel der Lieferung |
| Envelope | `vorschlaege[]` | Mindestens ein Vorschlag |
| Vorschlag | `typ` | `linkedin_post` |
| Vorschlag | `titel` | Inbox-Titel |
| Vorschlag | `linkedin_post` | Vollständiger Post-Text |
| Vorschlag | `quellen[]` | Mindestens eine Quelle mit `url` |

Schema-Datei (kanonisch): `knowledge-platform/schemas/agent-lieferung.v3.json`  
Beispiel gültig: `knowledge-platform/examples/presseschau/gueltig_v3.json`

**Legacy v1/v2** werden weiterhin importiert (weiche Warnungen), für Produktion wird **v3** empfohlen.

## Validierungslogik

| Stufe | Modul | Ergebnis |
|-------|--------|----------|
| Schema | `validiere_schema()` | Fehler → gesamte v3-Lieferung abgelehnt |
| URLs | `pruefe_quellen_liste()` | rot → Vorschlag nicht importiert; gelb → import mit Warnung |
| Dublette | `fingerabdruck_vorschlag()` | übersprungen, Log-Eintrag |
| Brandvoice | `pruefe_linkedin_post_mit_ampel()` | in `meta.brandvoice_status` |

Protokoll: `data/agenten/import_log.json` (gitignored)

## URL-Prüfung

- Nur `http://` und `https://`
- HEAD-Request, bei 405/501 Fallback GET
- **ok** — HTTP 2xx
- **gelb** — Timeout, Netzwerk, HTTP 3xx
- **rot** — 404, 4xx/5xx, ungültiges Format

Tracking-Parameter werden bereinigt (`utm_*`, `fbclid`, `gclid`, …) — `bereinige_tracking_url()`.

## Dublettenprüfung

Fingerabdruck aus:

- `datum`
- `titel` (normalisiert)
- primäre Quellen-URL (bereinigt)
- Hash des `linkedin_post`-Texts

Bekannte Fingerabdrücke: aktive Inbox, Archiv, Import-Log.  
Dubletten werden **nicht** erneut als offene Vorschläge angelegt.

## Brandvoice-Ampel

| Ampel | Bedeutung | Freigabe |
|-------|-----------|----------|
| **grün** | freigabefähig | Annehmen |
| **gelb** | manuell prüfen (Hinweise) | Annehmen mit Bewusstsein |
| **rot** | nicht freigabefähig (No-Gos, Floskeln, Pitch) | blockiert — nur **Trotzdem** |

Gespeichert in:

- `meta.brandvoice_status` — `gruen` | `gelb` | `rot`
- `meta.brandvoice_hinweise` — Liste
- `meta.brandvoice_verstoesse` — harte Verstöße

Playbook: `knowledge-platform/content/playbooks/linkedin-presseschau.md`

## Regisseur-Inbox-Anzeige

Pro `linkedin_post`-Vorschlag:

- Validierung, Quellen, Brandvoice, Dublette
- Quellen-Details aus `meta.quellen_pruefung`
- Beitragsbild-Vorschau falls vorhanden

## Manuelle Freigabe

1. **Annehmen** — bei grün/gelb (gelb: Hinweis beachten)
2. **Trotzdem** — nur bei `linkedin_post`, übergang Brandvoice rot
3. **Verwerfen** — mit Grund (Lernsignal)
4. **Erledigt** — nach manuellem Posten in LinkedIn

Es gibt **keine** direkte LinkedIn-API-Veröffentlichung.

## Fehlerbehandlung

| Situation | Verhalten |
|-----------|-----------|
| Schema v3 ungültig | Datei archiviert, nichts importiert, `import_log` + `fehler[]` |
| Quelle rot | Einzelvorschlag abgelehnt |
| Dublette | Übersprungen, Log `typ=dublette` |
| Netzwerk timeout (URL) | gelb, Import mit Warnung |

## Tests

```bash
cd digiwiki
python -m unittest tests.test_presseschau_stufe_b -v
```

Abgedeckt: gültige Lieferung, fehlendes Pflichtfeld, defekte URL, Dublette, Brandvoice-Ampel, E2E-Inbox.

## Module

| Datei | Rolle |
|-------|--------|
| `agent_lieferung_validierung.py` | QS-Kern |
| `agent_lieferung.py` | Import + Sync |
| `brandvoice_pruefung.py` | Ampel |
| `presseschau.py` | LinkedIn-Mapping, Entwürfe |
| `regisseur_inbox.py` | Freigabe-Logik |
