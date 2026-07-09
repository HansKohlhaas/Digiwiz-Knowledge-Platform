# ADR-0002: Regisseur-Inbox bleibt Freigabe-Hub

## Status

Akzeptiert (2026-07-09)

## Kontext

Digiwiz ist ein Regisseur-System: KI bereitet vor, Hans entscheidet.

## Entscheidung

Alle Agenten-Lieferungen (Presseschau, Newsletter, Runtime-Tasks mit `submit_inbox`) enden in `regisseur_inbox.json` mit Status `offen`.

Freigabe nur über `annehmen_vorschlag()` — optional `erzwingen=True` bei Brandvoice rot.

## Konsequenzen

- Kein Umgehen der Inbox in Produktivpfaden
- Runtime und API liefern `inbox_id`, nicht Publish-URLs
- Knowledge Platform dokumentiert Freigabe als Pflicht-Schritt
