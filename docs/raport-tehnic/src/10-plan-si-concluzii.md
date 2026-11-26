<!-- Responsabil: D. -->

# Plan și concluzii

## Planul de implementare

Tabelul: Planul de implementare pe sprinturi

| Sprint | Livrabile principale |
|---|---|
| S0 (până la 08.11) | depozitul, scheletul aplicației, CI; mediul de lucru funcțional pentru toți; prezentarea temei și a rolurilor |
| S1 (până la 22.11) | diagramele de clase și use case; designul final al bazei de date; contractele API v1; entitățile și CRUD-ul de bază; înregistrarea, autentificarea, validarea JWT la gateway |
| S2 (până la 06.12) | Raportul Tehnic (30.11); crearea și răsfoirea licitațiilor; ciclul de viață; licitarea cu rezervarea fondurilor; difuzarea prin WebSocket; aplicația completă în Docker Compose |
| S3 (până la 20.12) | anti-sniping; închiderea automată și decontarea; notificările; pagina live; testul de concurență; colecția Postman completă; prima implementare manuală în cloud |
| S4 (până la 17.01) | livrarea automată în cloud; HTTPS; revizuirea securității; finisarea interfeței; scenariul de demonstrație și prezentarea finală |

## Stadiul la data predării

Tabelul: Stadiul proiectului la 26.11.2026

| Domeniu | Stadiu |
|---|---|
| Depozitul, ramurile, regulile de lucru, issue-urile pe sprinturi | realizat (S0) |
| Scheletul celor cinci servicii și al front-end-ului; Docker Compose; CI pe fiecare push | realizat (S0): toate serviciile pornesc, testele de încărcare a contextului trec |
| Contractele API v1, arhitectura, ADR-urile, diagramele UML | realizat (S1) |
| Designul bazei de date și migrațiile inițiale (`V1__init.sql`) | realizat (S1); schema `bidding_db` este verificată automat în CI pe MySQL real |
| Entitățile, CRUD-ul de bază, înregistrarea, autentificarea, validarea JWT la gateway | neîncepute; se reportează din S1 în S2 |
| Licitarea, ciclul de viață, WebSocket, decontarea, cloud | planificate pentru S2–S4, conform tabelului de mai sus |

**Concluzia stadiului:** livrabilele de proiectare din S0 și S1 sunt complete, dar implementarea logicii de business din S1 a întârziat. Sarcinile reportate au prioritate în S2, înaintea sarcinilor noi. Riscul de integrare târzie este redus de contractele deja fixate și de profilul `stub`, care permit fiecărui serviciu să fie dezvoltat și testat separat.

## Riscuri principale

Tabelul: Riscurile principale ale proiectului

| Risc | Măsură |
|---|---|
| Integrarea târzie a serviciilor | contracte API înghețate în S1, profil `stub`, zi de integrare în fiecare sprint |
| Erori de concurență la licitare | lock pesimist, constrângeri unice, test automat cu oferte paralele |
| Probleme cu Docker pe Windows | limite de memorie, ghid de depanare, suport din partea DevOps Engineer-ului |
| Indisponibilitatea unui membru | sarcini mici și documentate, revizuiri încrucișate, redistribuire la sprint planning |
| Limitele mediului de cloud | implementare timpurie (S3), imagini mici, o singură instanță MySQL |

## Concluzii

**Ce acoperă proiectul:** proiectarea aplicației Live Auction App îndeplinește toate cerințele disciplinei:
- cinci microservicii Spring Boot, care comunică prin REST;
- o bază de date MySQL, cu câte o schemă per serviciu;
- containerizare completă cu Docker și Docker Compose;
- un plan de implementare în cloud cu livrare automată;
- testare pe mai multe niveluri.

**Decizii-cheie** pentru problemele reale ale unei licitații live:
- lock-ul pesimist pe un rând de stare per licitație;
- rezervarea fondurilor cu decontare idempotentă;
- închiderea în doi pași, fără apeluri HTTP cât timp se ține un lock;
- notificările trimise doar după commit;
- sincronizarea cronometrelor cu ceasul serverului.

Toate sunt documentate în ADR-uri și sunt proiectate astfel încât să poată fi demonstrate și testate automat pe măsură ce sunt implementate.

**Metodologia:** Scrum, cu roluri distincte și componente deținute de fiecare membru, permite lucrul în paralel. Contractele API comune și profilul `stub` reduc dependențele dintre membri.

## Dezvoltări ulterioare

- Un broker de mesaje (RabbitMQ) pentru evenimente, cu livrare garantată și mai multe instanțe ale serviciului de notificări.
- Tiparul transactional outbox sau saga, pentru consistența completă între servicii la eșecuri parțiale.
- Circuit breaker (Resilience4j) pe apelurile interne.
- Tokenuri RS256 cu cheie publică (JWKS) și tokenuri de reîmprospătare.
- Stocarea fotografiilor într-un serviciu de stocare de obiecte.
- Căutare după titlu, anularea licitațiilor programate, notificări prin email.
