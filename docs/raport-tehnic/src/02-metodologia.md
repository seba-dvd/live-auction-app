<!-- Responsabil: K (Scrum Master). Cerința (a) a disciplinei: modelul de dezvoltare ales și descrierea lui. -->

# Metodologia de dezvoltare

## Modele analizate

La curs au fost prezentate mai multe modele de dezvoltare software [1]. Echipa le-a comparat din perspectiva proiectului:
- 5 membri cu roluri diferite;
- termene intermediare fixe (Raportul Tehnic, prezentările de stadiu);
- cerințe care se clarifică pe parcurs.

Tabelul: Comparația modelelor de dezvoltare

| Model | Caracteristici | Potrivire pentru proiect |
|---|---|---|
| Waterfall (cascadă) | etape secvențiale: cerințe, proiectare, implementare, testare; schimbările târzii sunt costisitoare | slabă: integrarea și testarea ar veni abia la final, iar riscul de a nu avea nimic funcțional la prezentarea de stadiu este mare |
| Agile / Scrum | iterații scurte (sprinturi), increment funcțional la fiecare sprint, roluri clare, adaptare pe baza feedbackului | foarte bună: livrări intermediare care se potrivesc cu ședințele disciplinei, roluri care corespund rolurilor cerute de curs |
| DevOps | integrare și livrare continuă, automatizare, responsabilitate comună pentru operare | complementar: practicile DevOps (CI/CD, Docker) sunt folosite în interiorul sprinturilor Scrum |
| Rapid Application Development | prototipare rapidă, implicarea intensă a utilizatorului | parțială: lipsesc procesele pentru coordonarea a 5 persoane |

**Decizia:** echipa folosește **Scrum** pentru organizarea muncii și **practici DevOps** pentru calitatea tehnică: integrare continuă, containere, livrare automată în cloud. Scrum oferă:
- un increment demonstrabil la fiecare două săptămâni;
- un backlog prioritizat de Product Owner;
- ceremonii care fac vizibile blocajele.

Aceste lucruri sunt esențiale într-o echipă studențească, în care membrii lucrează în paralel și asincron.

## Scrum în echipa noastră

**Roluri Scrum** [2]:
- **Product Owner (A)** gestionează backlog-ul.
- **Scrum Master (K)** facilitează procesul și elimină blocajele.
- **Echipa de dezvoltare** este formată din toți cei cinci membri. Fiecare deține o componentă: un microserviciu sau front-end-ul.

Rolurile suplimentare cerute de disciplină (Project Manager, Technical Lead, DevOps Engineer) sunt descrise în capitolul 3.

Tabelul: Evenimentele Scrum adaptate proiectului

| Eveniment | Când | Durată | Rezultat |
|---|---|---|---|
| Sprint planning | prima zi a sprintului | 45 min | obiectivul sprintului; issues alese din backlog și atribuite (milestone-ul sprintului) |
| Daily stand-up | zilnic, asincron, în chatul echipei, până la 22:00 | 2–3 min / membru | mesajul „Ieri / Azi / Blocaje”; Scrum Master-ul urmărește blocajele |
| Sprint review | ultima zi a sprintului | 25 min | demonstrarea incrementului; Product Owner-ul acceptă sau respinge poveștile |
| Retrospectiva | după review | 20 min | o acțiune concretă de îmbunătățire pentru sprintul următor |

**Artefacte:**
- **Product backlog:** issues GitHub de tip `type:story`, cu criterii de acceptanță „Dat fiind / Când / Atunci” și prioritate MoSCoW.
- **Sprint backlog:** issues-urile din milestone-ul sprintului, vizibile pe board-ul GitHub Project.
- **Incrementul:** codul integrat pe ramura `main` la finalul sprintului, marcat cu tag-ul `v0.<sprint>.0`.

**Definition of Done.** O sarcină este gata când:
- codul compilează și testele trec;
- criteriile de acceptanță sunt îndeplinite;
- PR-ul spre `develop` are CI-ul verde;
- contractele API și colecția Postman sunt actualizate;
- nu există secrete în cod;
- funcționalitatea rulează în stack-ul complet din Docker Compose.

## Calendarul sprinturilor

Tabelul: Calendarul sprinturilor

| Sprint | Perioada | Obiectiv |
|---|---|---|
| S0, Pregătire | 28.10 – 08.11.2026 | mediul de lucru funcțional pentru toți; tema și rolurile prezentate |
| S1, Design și fundații | 09.11 – 22.11.2026 | diagrame UML, baza de date, contracte API v1, entități, autentificare |
| S2, Fluxuri de bază | 23.11 – 06.12.2026 | licitații, licitare cu rezervarea fondurilor, WebSocket; Raport Tehnic (30.11) |
| S3, Timp real și integrare | 07.12 – 20.12.2026 | anti-sniping, decontare, notificări, pagina live, Postman |
| S4, Cloud și final | 04.01 – 17.01.2027 | implementare în cloud, livrare automată, teste, demonstrație |

## Fluxul de lucru cu Git

Codul se află într-un singur depozit GitHub (monorepo). Reguli:

- **`main`:** conține doar versiuni stabile. Primește la final de sprint un pull request din `develop`, integrat de Project Manager.
- **`develop`:** ramura de integrare. Primește pull request-uri din ramurile personale.
- **Ramurile personale de lungă durată:** `d/user-gateway`, `m/bidding`, `k/auction`, `a/frontend`, `r/devops`. Fiecare membru lucrează pe ramura lui și o sincronizează cu `develop` după fiecare integrare.
- **Protecția ramurilor:** `main` și `develop` primesc modificări doar prin pull request, fără aprobare obligatorie. Force-push-ul și ștergerea sunt interzise.
- **Merge:** pull request-urile se integrează doar prin merge commit, nu prin squash, ca ramurile de lungă durată să rămână ușor de sincronizat.
- **Mesajele de commit** respectă convenția Conventional Commits, de exemplu `feat(bidding): ...`. Fiecare pull request închide issue-ul lui prin `Closes #…`.
- **Integrarea continuă** (GitHub Actions) compilează și testează la fiecare push doar componentele modificate.

## Instrumente

Tabelul: Instrumentele folosite în procesul de dezvoltare

| Scop | Instrument |
|---|---|
| Cod, revizuiri, sarcini, board | GitHub (repository, pull requests, Issues, Projects) |
| Integrare continuă și livrare | GitHub Actions, GitHub Container Registry |
| Dezvoltare backend | IntelliJ IDEA, JDK 21, Maven Wrapper |
| Dezvoltare front-end | Node.js 24 LTS, Vite, VS Code / IntelliJ |
| Rulare locală | Docker Desktop (WSL2), Docker Compose |
| Testarea API-ului | Postman, Newman |
| Diagrame | PlantUML, MySQL Workbench |
| Comunicare | chatul echipei, ședințele de laborator |
