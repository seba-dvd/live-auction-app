# Raport Tehnic: Proiectare (Tema 1)

**Livrabilul de evaluare pe parcurs al cursului:** termen de predare **30.11.2026** (S9), termen intern **27.11.2026**.

**Conținut cerut de curs:**
- (a) modelul de dezvoltare ales și descrierea lui;
- (b) rolurile și responsabilitățile din echipă;
- (c) structura bazei de date cu relațiile dintre tabele;
- (d) modelarea arhitecturii: diagrama de clase și diagrama use case.

**Formatul** respectă șablonul UNITBV (`Documentatie_Licenta.docx`):
- font UT Sans;
- capitole numerotate automat;
- figuri, tabele și coduri cu legendă („Figura N”, „Tabelul N”, „Codul N”);
- listă de figuri și listă de acronime;
- bibliografie cu `[n]`;
- antet diferit pe paginile pare și impare.

| Fișier | Conținut |
|---|---|
| [Raport_Tehnic_Proiectare.docx](Raport_Tehnic_Proiectare.docx) | documentul Word generat: **ce se predă** (după revizuire) |
| [Raport_Tehnic_Proiectare.pdf](Raport_Tehnic_Proiectare.pdf) | exportul PDF |
| [src/](src/) | sursele Markdown, câte un fișier per capitol; **aici se editează** |
| [document.toml](document.toml) | titlul, coperta, ordinea capitolelor |

## Capitole, responsabili, termene

| Nr. | Capitol | Fișier sursă | Responsabil | Cerință curs | Draft gata până la |
|---|---|---|---|---|---|
| 1 | Descrierea aplicației | `src/01-descrierea-aplicatiei.md` | A | — | 20.11.2026 |
| 2 | Metodologia de dezvoltare: Agile/Scrum | `src/02-metodologia.md` | K | (a) | 20.11.2026 |
| 3 | Roluri și responsabilități | `src/03-roluri.md` | D | (b) | 20.11.2026 |
| 4 | Arhitectura sistemului (+ diagrama de componente) | `src/04-arhitectura.md` | M | (d) | 24.11.2026 |
| 5 | Diagrama cazurilor de utilizare | `src/05-cazuri-de-utilizare.md` | A | (d) | 24.11.2026 |
| 6 | Diagrama de clase | `src/06-diagrama-de-clase.md` | M, cu input de la toți | (d) | 24.11.2026 |
| 7 | Structura bazei de date | `src/07-baza-de-date.md` | K | (c) | 24.11.2026 |
| 8 | Infrastructură: Docker, Compose, CI/CD, Cloud | `src/08-infrastructura.md` | R | — | 24.11.2026 |
| 9 | Securitate | `src/09-securitate.md` | D | — | 24.11.2026 |
| 10 | Plan și concluzii | `src/10-plan-si-concluzii.md` | D | — | 26.11.2026 |
| — | Acronime, Bibliografie, Rezumat, Abstract | `src/00-acronime.md`, `src/90-bibliografie.md`, `src/95-rezumat.md`, `src/96-abstract.md` | D | — | 26.11.2026 |

Bootstrap-ul a scris o **versiune v0.1 completă** a fiecărui capitol, ca punct de plecare. Fiecare responsabil verifică, corectează și completează capitolul lui, mai ales ce s-a decis între timp în echipă.

## Cum lucrezi la capitolul tău

1. Pe ramura ta, editezi `src/<capitol>.md`.
2. **Diagramele** le modifici în `docs/uml/*.puml` sau `docs/database/*.puml` și le regenerezi cu `bash tools/diagrams/render.sh`.
3. Regenerezi documentul Word cu `bash tools/docgen/build.sh raport` (detalii în [tools/docgen/README.md](../../tools/docgen/README.md)) și îl verifici vizual.
4. PR către `develop` cu D ca reviewer.

**Convenții Markdown pentru generator:**
- `# Titlu` = capitol, `##` = subcapitol, `###` = secțiune. Nu le numerota manual: Word le numerotează automat.
- **Figuri:** `![Legenda figurii](../../diagrams/png/nume.png)`. Legenda devine „Figura N. Legenda figurii”.
- **Figuri late:** cu `{landscape}` după imagine, figura apare pe o pagină orientată orizontal.
- **Tabele:** paragraful `Tabelul: Legenda tabelului` pus imediat **înaintea** unui tabel Markdown devine legenda tabelului.
- **Cod:** paragraful `Codul: Legenda codului` pus imediat **după** un bloc de cod devine legenda codului.
- **Citări:** `[3]`, cu intrarea corespunzătoare în `src/90-bibliografie.md`.

## Asamblare și predare (D)

- [ ] 27.11: toate capitolele sunt pe `develop`, revizuite de câte un coleg.
- [ ] Documentul se regenerează, cuprinsul și listele se actualizează (scriptul o face automat prin Word).
- [ ] Verificări: diacritice, legende, numerotarea figurilor, bibliografie, acronime, antet/subsol.
- [ ] Fontul **UT Sans** e instalat pe calculatorul care exportă PDF-ul (fonturile se descarcă de pe intranet.unitbv.ro).
- [ ] 28–29.11: citire finală de către toată echipa.
- [ ] 30.11: predare (formatul cerut de coordonator: .docx și/sau .pdf).
