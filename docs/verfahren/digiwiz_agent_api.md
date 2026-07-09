---
title: Digiwiz Agent API (Stufe C)
slug: digiwiz-agent-api
category: Verfahren
audience: admin
version: "2026-07-09"
order: 11
knowledge_platform: "1.0.0"
---

# Digiwiz Agent API — Stufe C

Kontrollierte Anbindung externer KI-Systeme an Digiwiz — **lokal per CLI und REST**, ohne Auto-Veröffentlichung. Alle Inhalte laufen über die **Regisseur-Inbox** zur manuellen Freigabe.

## Zweck

| Komponente | Rolle |
|------------|--------|
| `digiwiz-agent` CLI | Lokale Einreichung und Validierung |
| REST-API (`11_wiki_api.py`) | Maschinelle Anbindung (später MCP-fähig) |
| Playbooks (YAML) | Maschinenlesbare Regeln für externe Agenten |
| Stufe B QS | Schema, URLs, Dubletten, Brandvoice-Ampel |

**Keine** direkte LinkedIn-Veröffentlichung. **Keine** automatische Freigabe.

## Voraussetzungen

- Python 3.12, Digiwiz-venv mit `pip install -r requirements.txt`
- `DIGIWIZ_API_KEY` in `.env` (Repo-Root, `digiwiki/.env` oder `firmenapp/.env`)
- Optional: `DIGIWIKI_API_HOST` (Standard `0.0.0.0`), `DIGIWIKI_API_PORT` (Standard `8000`)

```env
DIGIWIZ_API_KEY=ihr-lokaler-geheimer-schluessel
```

Alternativ: `firmenapp/config/agent_api.json` mit `{"api_key": "..."}`

## CLI-Nutzung

```cmd
cd c:\Digiwiz\digiwiki
digiwiz_agent.bat validate ..\knowledge-platform\examples\presseschau\gueltig_v3.json
digiwiz_agent.bat submit presseschau ..\knowledge-platform\examples\presseschau\gueltig_v3.json
digiwiz_agent.bat status
digiwiz_agent.bat list-playbooks
digiwiz_agent.bat show-playbook presseschau
```

| Befehl | Beschreibung |
|--------|--------------|
| `validate <file>` | JSON prüfen (Schema, URLs, Dubletten, Brandvoice) — **kein Import** |
| `submit presseschau <file>` | Prüfen + in Regisseur-Inbox importieren |
| `status` | Betriebsmonitor (JSON) |
| `list-playbooks` | Verfügbare Playbooks |
| `show-playbook <name>` | Playbook als JSON (oder `--format yaml`) |

Option: `--skip-url-check` — Quellen-URL-Prüfung überspringen (nur Tests/Dev).

Exit-Codes: `0` = Erfolg, `1` = Validierungsfehler/Dublette, `2` = Laufzeitfehler

## REST-API starten

```cmd
cd c:\Digiwiz\digiwiki
start_agent_api.bat
```

Basis-URL: `http://localhost:8000`

## REST-Endpunkte

| Methode | Pfad | Auth | Beschreibung |
|---------|------|------|--------------|
| GET | `/api/v1/status` | nein | Betriebsmonitor |
| GET | `/api/v1/playbooks` | nein | Playbook-Liste |
| GET | `/api/v1/playbooks/{name}` | nein | Playbook-Detail (JSON) |
| POST | `/api/v1/agenten/validate` | **ja** | Nur validieren |
| POST | `/api/v1/agenten/lieferung` | **ja** | Validieren + Inbox-Import |
| GET | `/health` | nein | Health-Check |

## Authentifizierung

Header: `X-DIGIWIZ-API-KEY: <Schlüssel>`

## Playbooks

YAML (kanonisch): `knowledge-platform/playbooks/` — Auflösung via `digiwiki/knowledge_paths.py`  
Fallback: `firmenapp/config/playbooks/`

Markdown wird aus `content_file` in YAML geladen (z. B. `content/playbooks/linkedin-presseschau.md`).

## Datenfluss

```
Externer Agent → CLI/REST → Stufe B QS → regisseur_inbox.json → Manuelle Freigabe
```

## Tests

```cmd
cd c:\Digiwiz\digiwiki
python -m unittest tests.test_agent_api_stufe_c -v
```

Siehe auch: [presseschau_qualitaetssicherung.md](presseschau_qualitaetssicherung.md), [digiwiz_ai_runtime.md](digiwiz_ai_runtime.md)
