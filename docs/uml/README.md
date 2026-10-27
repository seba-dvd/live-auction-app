# Diagrame UML

**Sursele sunt în PlantUML** (fișiere `.puml` text, ușor de revizuit în PR). Imaginile PNG generate stau în [../diagrams/png/](../diagrams/png/) și se comit împreună cu sursa. Toate diagramele sunt **DRAFT** până când proprietarul le finalizează.

**Cerințele cursului:**
- **obligatorii:** diagrama de clase și diagrama use case (Ședințele 4–5);
- **opționale:** diagramele de activitate și de componente.

Le avem pe toate, plus diagrame de secvență, de stări și de implementare.

| Diagramă | Sursă | Imagine | Proprietar | Termen |
|---|---|---|---|---|
| Cazuri de utilizare | [use-case.puml](use-case.puml) | [PNG](../diagrams/png/use-case.png) | A | S1 (Ședința 4–5) |
| Clase: vedere de ansamblu | [class-diagram.puml](class-diagram.puml) | [PNG](../diagrams/png/class-diagram.png) | M (asamblează, cu input de la toți) | S1 (Ședința 4–5) |
| Clase: user-service | [class-user-service.puml](class-user-service.puml) | [PNG](../diagrams/png/class-user-service.png) | D | S1 |
| Clase: auction-service | [class-auction-service.puml](class-auction-service.puml) | [PNG](../diagrams/png/class-auction-service.png) | K | S1 |
| Clase: bidding-service | [class-bidding-service.puml](class-bidding-service.puml) | [PNG](../diagrams/png/class-bidding-service.png) | M | S1 |
| Clase: notification-service | [class-notification-service.puml](class-notification-service.puml) | [PNG](../diagrams/png/class-notification-service.png) | R | S1 |
| Componente | [component.puml](component.puml) | [PNG](../diagrams/png/component.png) | M | S2 (Raport) |
| Implementare (deployment) | [deployment.puml](deployment.puml) | [PNG](../diagrams/png/deployment.png) | R | S2 (Raport) |
| Secvență: autentificare | [sequence-login.puml](sequence-login.puml) | [PNG](../diagrams/png/sequence-login.png) | D | S2 |
| Secvență: plasare ofertă | [sequence-place-bid.puml](sequence-place-bid.puml) | [PNG](../diagrams/png/sequence-place-bid.png) | M | S2 |
| Secvență: închidere și decontare | [sequence-auction-close.puml](sequence-auction-close.puml) | [PNG](../diagrams/png/sequence-auction-close.png) | K | S2 |
| Activitate: ciclul de viață | [activity-auction-lifecycle.puml](activity-auction-lifecycle.puml) | [PNG](../diagrams/png/activity-auction-lifecycle.png) | K | S3 |
| Stări: licitație | [state-auction.puml](state-auction.puml) | [PNG](../diagrams/png/state-auction.png) | K | S3 |
| Diagrame ER (bază de date) | [../database/](../database/README.md) | `er-*.png` | K | S1 |

## Notația folosită (ca la curs)

- **Clase:**
  - trei compartimente: nume, atribute, operații;
  - vizibilitate `+` public, `-` privat, `#` protejat;
  - `atribut : Tip`, `operație(param : Tip) : TipReturnat`;
  - multiplicități `1`, `0..1`, `0..*`, `1..*`;
  - compoziție (romb plin), dependență (linie punctată cu săgeată deschisă), realizare (linie punctată cu triunghi gol).
- **Use case:**
  - actorii sunt în afara dreptunghiului sistemului;
  - `<<include>>` are săgeata de la cazul de bază spre cel inclus;
  - `<<extend>>` are săgeata de la extensie spre cazul de bază, cu condiția între paranteze drepte.
- **ER:**
  - notația crow's foot, ca în MySQL Workbench;
  - `*` = NOT NULL, `<<PK>>`, `<<FK>>`, `<<UQ>>`;
  - linia punctată marchează o referință logică între scheme, fără cheie străină.

## Cum modifici o diagramă

1. Editezi fișierul `.puml`. Extensia IntelliJ **PlantUML Integration** arată preview-ul live; alternativ, <https://www.plantuml.com/plantuml> (nu pune acolo date sensibile).
2. Regenerezi imaginile din rădăcina repo-ului: `bash tools/diagrams/render.sh` (doar Java 21; la prima rulare descarcă PlantUML ~13 MB). Pentru o singură diagramă: `bash tools/diagrams/render.sh docs/uml/use-case.puml`.
3. Faci commit cu ambele fișiere (`.puml` + `.png`) în același PR.
4. Pentru Raportul Tehnic, documentul Word se regenerează cu `bash tools/docgen/build.sh` (vezi [tools/docgen/README.md](../../tools/docgen/README.md)).
