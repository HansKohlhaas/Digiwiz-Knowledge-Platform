# Security

Sicherheit bedeutet fuer Digiwiz vor allem kontrollierte Freigabe, nachvollziehbare Datenfluesse und begrenzte Tool-Rechte.

## Schutzprinzipien

- Least Privilege fuer APIs, CLI-Kommandos und MCP-Tools.
- Keine Secrets in Repository-Dateien.
- Keine produktiven Tokens in Beispielen.
- Auditierbare Freigaben fuer veroeffentlichungsnahe Aktionen.

## Datenklassen

- Oeffentlich: veroeffentlichte Artikel, oeffentliche Quellen.
- Intern: Playbooks, Entwuerfe, Roadmap, Architektur.
- Sensibel: Tokens, Kundendaten, private Kommunikation, unveroeffentlichte Strategie.

## Pflichtpruefungen

- Sind Quellen korrekt referenziert?
- Enthalten Entwuerfe vertrauliche Informationen?
- Gibt es versteckte Auto-Publish-Pfade?
- Sind Berechtigungen minimal gehalten?
