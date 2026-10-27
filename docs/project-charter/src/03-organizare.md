# Calendar și organizare

## Jaloane

**Calendarul de lucru:**
- **Sprinturi:** de câte două săptămâni. Scrum Master-ul ajustează datele exacte după programul real al ședințelor.
- **Rezultatul fiecărui sprint:** un increment funcțional, integrat pe ramura `main` și marcat cu un tag de versiune (`v0.<sprint>.0`).

Tabelul: Calendarul sprinturilor și jaloanele proiectului

| Sprint | Perioada | Obiectiv | Termene ale disciplinei |
|---|---|---|---|
| S0, Pregătire | 28.10 – 08.11.2026 | toți membrii rulează aplicația local; rolurile și tema sunt prezentate | Ședința 3 (02/09.11); înregistrarea temei până la 09.11 |
| S1, Design și fundații | 09.11 – 22.11.2026 | diagramele use case și de clase; designul bazei de date; contractele API v1 înghețate; entități și CRUD de bază; autentificarea | Ședințele 4–5 |
| S2, Fluxuri de bază | 23.11 – 06.12.2026 | crearea și răsfoirea licitațiilor, ciclul de viață, licitarea cu rezervarea fondurilor, difuzarea prin WebSocket, CI verde | **Raport Tehnic: Proiectare, 30.11** (intern 27.11) |
| S3, Timp real și integrare | 07.12 – 20.12.2026 | anti-sniping, închiderea automată și decontarea, notificările, pagina live, colecția Postman completă | Ședințele 6–7: prezentarea stadiului |
| Vacanță | 21.12.2026 – 03.01.2027 | timp-tampon opțional | — |
| S4, Cloud și final | 04.01 – 17.01.2027 | implementarea în cloud, livrarea automată, teste, scenariul de demonstrație | prezentarea finală |

## Părți interesate

Tabelul: Părțile interesate

| Parte interesată | Interes | Implicare |
|---|---|---|
| Coordonatorul disciplinei | respectarea cerințelor, calitatea tehnică și a documentației, evaluarea | ședințele de laborator, prezentări, Raportul Tehnic |
| Echipa de proiect (5 membri) | o aplicație funcțională, notă bună, experiență practică | zilnic, prin GitHub și chatul echipei |
| Utilizatorii finali (colegii, la demonstrație) | o aplicație ușor de folosit, licitare corectă și rapidă | testare de acceptanță la sprint review și la demo |
| Colegii din alte echipe | schimb de experiență | prezentările de stadiu și finale |

## Echipa și rolurile

Tabelul: Rolurile din echipă

| ID | Membru | Rol | Componente | Responsabilități principale |
|---|---|---|---|---|
| D | Pilat David Sebastian | Project Manager | user-service, api-gateway | planificare, termene, riscuri, administrarea depozitului, release-uri, asamblarea Raportului Tehnic, prezentări |
| M | M | Technical Lead | bidding-service, contracte API, arhitectură | decizii tehnice, aprobarea contractelor, revizuiri de cod, diagrama de clase, integrare |
| K | K | Scrum Master | auction-service, baza de date | ceremoniile Scrum, board-ul, eliminarea blocajelor, designul bazei de date |
| A | A | Product Owner | front-end, backlog | user stories, priorități, acceptanța poveștilor, diagrama use case, scenariul de demo |
| R | R | DevOps Engineer | notification-service, infrastructură, Postman | Docker, Compose, CI/CD, cloud, colecția Postman, sprijin pentru problemele de mediu |

## Matricea RACI

R = execută; A = răspunde și aprobă; C = consultat; I = informat.

Tabelul: Matricea RACI

| Activitate | D | M | K | A | R |
|---|---|---|---|---|---|
| Planificare, termene, riscuri | A/R | C | C | C | C |
| Arhitectură și contracte API | C | A/R | C | C | C |
| Backlog și priorități | C | C | C | A/R | I |
| Ceremonii Scrum și board | C | I | A/R | C | I |
| user-service și api-gateway | R | A | I | C | I |
| auction-service și designul bazei de date | C | A | R | I | I |
| bidding-service | C | A/R | C | I | I |
| Front-end | I | A | I | R | I |
| notification-service, Docker, CI/CD, cloud | C | A | I | I | R |
| Raport Tehnic (capitole proprii și asamblare) | A/R | R | R | R | R |
| Prezentări și demonstrație | A/R | R | R | R | R |

## Plan de comunicare

Tabelul: Planul de comunicare

| Activitate | Frecvență | Participanți | Responsabil | Canal |
|---|---|---|---|---|
| Daily stand-up asincron: Ieri / Azi / Blocaje | zilnic, până la 22:00 | toți | K | chatul echipei |
| Sprint planning | prima zi a sprintului, 45 min | toți | K (A aduce prioritățile) | întâlnire online sau fizică |
| Sprint review și retrospectivă | ultima zi a sprintului, 45 min | toți | K, A | întâlnire |
| Check-in PM – Scrum Master | săptămânal, 15 min | D, K | D | chat sau apel |
| Zi de integrare („merge day”) | o dată pe sprint | D, M (toți, la nevoie) | M | întâlnire |
| Lucru tehnic: issues, PR-uri, revizuiri | continuu | toți | autorul PR-ului | GitHub |
| Comunicarea cu coordonatorul | la ședințe și la nevoie | D, toți | D | ședințe, email |

**GitHub este sursa de adevăr:**
- sarcinile sunt issues, cu milestone-ul sprintului;
- deciziile se scriu în ADR-uri sau în documentație;
- orice modificare de cod trece prin pull request.
