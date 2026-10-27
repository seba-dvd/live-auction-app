# Resurse, constrângeri și riscuri

## Resurse și buget

**Bugetul proiectului este 0 lei.** Se folosesc doar instrumente gratuite sau oferite studenților.

Tabelul: Resursele proiectului

| Resursă | Utilizare | Sursă |
|---|---|---|
| Laptopurile membrilor (recomandat 16 GB RAM) | dezvoltare, Docker Desktop cu WSL2 | proprii |
| JDK 21, IntelliJ IDEA, Node.js 24 LTS, Docker Desktop, Git, Postman | dezvoltare și testare | gratuite / licență de student |
| GitHub: depozit privat, Actions, Container Registry, Projects | cod, CI/CD, imagini Docker, board Scrum | GitHub Pro prin GitHub Student Developer Pack |
| Mașină virtuală în cloud | implementarea finală | credite pentru studenți (alegerea se documentează în ADR-005) |
| Nume de domeniu și certificat HTTPS | opțional, pentru demo | oferte pentru studenți, Let's Encrypt |
| Timp | aproximativ 6–8 ore pe săptămână pentru fiecare membru | — |

## Ipoteze

- Toți membrii au acces la GitHub Student Developer Pack și la un calculator care rulează Docker Desktop.
- Calendarul ședințelor disciplinei rămâne cel anunțat. Modificările se reflectă în planul sprinturilor.
- Fiecare membru poate aloca în medie 6–8 ore pe săptămână proiectului.
- Coordonatorul acceptă implementarea pe o mașină virtuală cu Docker Compose ca formă de implementare în cloud.

## Constrângeri

- **Termene fixe:**
  - înregistrarea temei până la 09.11.2026;
  - Raportul Tehnic până la 30.11.2026;
  - prezentările la ședințele stabilite de coordonator.
- **Tehnologii impuse:** microservicii Spring Boot, bază de date SQL, Docker și Docker Compose, cloud, testare cu Postman sau front-end.
- **Echipă și buget:** echipă de 5 persoane cu experiență diferită, buget zero.
- **Modul de lucru:** codul de business este scris de membri. Este o lucrare evaluată, iar instrumentele de asistență pot explica și revizui, dar nu pot înlocui munca proprie.

## Riscuri inițiale

Probabilitatea (P) și impactul (I) sunt evaluate pe scara mică / medie / mare.

Tabelul: Registrul inițial al riscurilor

| Risc | P | I | Măsuri de reducere | Responsabil |
|---|---|---|---|---|
| Integrare târzie: serviciile funcționează separat, dar nu și împreună | mare | mare | contracte API înghețate în S1, profilul `stub`, zi de integrare în fiecare sprint, CI pe fiecare push | M |
| Erori de concurență la licitare (doi lideri, bani rezervați greșit) | medie | mare | lock pesimist per licitație, constrângeri unice în baza de date, test cu 50 de oferte paralele | M |
| Probleme cu Docker pe Windows (memorie, WSL2, porturi ocupate) | mare | medie | configurarea `.wslconfig`, limite de memorie per container, ghid de depanare, R ca prim suport | R |
| Limitele mediului de cloud (credite, memorie) | medie | medie | prima implementare încă din S3, imagini mici (JRE), un singur MySQL | R |
| Indisponibilitatea unui membru (examene, boală) | medie | mare | sarcini mici în issues, ghiduri detaliate, revizuiri încrucișate, redistribuire la sprint planning | D |
| Extinderea necontrolată a cerințelor | medie | medie | backlog prioritizat MoSCoW, MVP definit, funcțiile „Could” doar în S4 | A |
| Diferențele Spring Boot 4 față de tutorialele pentru Boot 3 | mare | mică | secțiune dedicată în fiecare ghid, `CLAUDE.md`, exemple verificate | M |
| Scurgerea de secrete în depozit | mică | mare | `.env` ignorat de git, doar valori de dezvoltare în `.env.example`, secrete în GitHub Secrets | R |
