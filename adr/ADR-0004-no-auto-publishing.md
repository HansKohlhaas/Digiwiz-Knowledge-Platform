# ADR-0004: Keine Auto-Veröffentlichung

## Status

Akzeptiert (2026-07-09)

## Kontext

Presseschau, LinkedIn und Newsletter bergen Reputations- und Compliance-Risiken bei unkontrollierter Veröffentlichung.

## Entscheidung

- **Keine** direkte LinkedIn-API-Veröffentlichung aus Digiwiz
- **Keine** automatische WordPress-Publish-Pipeline
- **Keine** Auto-Freigabe bei grün/gelb in der Brandvoice-Ampel
- Bildgenerierung nur manuell per UI-Button

## Konsequenzen

- Playbooks enthalten `no_auto_publish` als harte Regel
- API-Responses liefern `inbox_id`, nicht `published_url`
- Stufe F (autonome Agenten) muss diese ADR explizit erweitern, nicht überschreiben
