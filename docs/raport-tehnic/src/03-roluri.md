<!-- Responsabil: D (Project Manager). Cerința (b) a disciplinei: rolurile și responsabilitățile din echipă. -->

# Roluri și responsabilități

## Echipa

Cursul recomandă împărțirea responsabilităților pe dezvoltarea microserviciilor, Docker, CI/CD, baza de date și cloud, plus rolurile de Scrum Master, Product Owner, Technical Lead și Project Manager [1].

**Cum am împărțit rolurile:**
- **Un rol de coordonare:** fiecare membru are un singur rol de coordonare.
- **O componentă tehnică:** fiecare membru deține un microserviciu sau front-end-ul. Astfel, toți cinci scriu cod de business, iar fiecare componentă are un responsabil clar.

Tabelul: Membrii echipei, rolurile și componentele deținute

| ID | Membru | Rol | Componente | Ramură Git |
|---|---|---|---|---|
| D | Pilat David Sebastian | Project Manager | user-service (autentificare, portofel), api-gateway | `d/user-gateway` |
| M | M | Technical Lead | bidding-service, contractele API, arhitectura | `m/bidding` |
| K | K | Scrum Master | auction-service, designul bazei de date | `k/auction` |
| A | A | Product Owner | front-end (React), backlog, diagrama use case | `a/frontend` |
| R | R | DevOps Engineer | notification-service (WebSocket), Docker, Compose, CI/CD, cloud, Postman | `r/devops` |

## Responsabilitățile rolurilor

**Project Manager (D)**
- Administrează depozitul GitHub: setări, protecția ramurilor, invitații.
- Integrează `develop` în `main` la finalul fiecărui sprint și creează tag-ul de versiune.
- Urmărește termenele disciplinei și registrul riscurilor. Are un check-in săptămânal cu Scrum Master-ul.
- Înregistrează tema la coordonator și asamblează Raportul Tehnic.
- Coordonează pregătirea prezentărilor de stadiu și a celei finale.

**Technical Lead (M)**
- Deține contractele API și documentul de arhitectură. Aprobă orice modificare de contract.
- Stabilește convențiile de cod și face revizuiri pentru D și K.
- Coordonează deciziile de arhitectură (ADR-uri) și ziua de integrare din fiecare sprint.
- Asamblează diagrama de clase și are ultimul cuvânt în disputele tehnice.

**Scrum Master (K)**
- Facilitează sprint planning, sprint review și retrospectiva.
- Urmărește stand-up-ul asincron zilnic și ține la zi board-ul GitHub Project.
- Identifică blocajele și le escaladează către Project Manager.
- Finalizează designul bazei de date împreună cu proprietarii serviciilor.

**Product Owner (A)**
- Scrie și prioritizează user stories (MoSCoW) și acceptă poveștile la sprint review.
- Realizează diagrama cazurilor de utilizare și descrierile cazurilor.
- Pregătește scenariul de demonstrație.

**DevOps Engineer (R)**
- Deține Dockerfile-urile, fișierele Compose, pipeline-urile CI/CD și mediul de cloud.
- Structurează colecția Postman și o rulează automat cu Newman.
- Este primul sprijin pentru problemele de mediu ale colegilor: Docker Desktop, WSL2, porturi.

## Matricea RACI

R = execută; A = răspunde și aprobă; C = consultat; I = informat.

Tabelul: Matricea RACI a proiectului

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
| Raport Tehnic | A/R | R | R | R | R |
| Prezentări și demonstrație | A/R | R | R | R | R |

## Proprietatea codului și revizuirea

**Proprietatea codului:**
- Fiecare membru modifică doar folderele pe care le deține.
- Fișierele comune se schimbă prin pull request revizuit de proprietarul lor: fișierele Compose, CI-ul, contractele API, documentația de arhitectură.
- Fișierul `CODEOWNERS` cere automat revizuirea proprietarului.

**Harta revizuirilor:**
- D este revizuit de M, iar M de D;
- K este revizuit de M;
- A este revizuit de K;
- R este revizuit de D.

Astfel, fiecare pull request este citit de cineva care cunoaște zona afectată, iar Technical Lead-ul vede toate modificările de backend.

## Comunicare

- **Stand-up zilnic:** asincron, în chatul echipei.
- **Ședințe:** de planificare, de review și retrospectivă, la începutul și finalul fiecărui sprint.
- **Lucrul tehnic** se face exclusiv în GitHub: issues, pull requests, comentarii de revizuire.
- **Deciziile importante** se documentează în ADR-uri, ca să nu se piardă în conversații.
- **Ghiduri individuale:** fiecare membru are un ghid (`docs/team/<ID>.md`, plus versiunea Word) cu sarcinile pe sprinturi, specificația tehnică a componentei și comenzile de lucru zilnic.
