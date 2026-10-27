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

Toate sunt documentate în ADR-uri și pot fi demonstrate și testate.

**Metodologia:** Scrum, cu roluri distincte și componente deținute de fiecare membru, permite lucrul în paralel. Contractele API comune și profilul `stub` reduc dependențele dintre membri.

## Dezvoltări ulterioare

- Un broker de mesaje (RabbitMQ) pentru evenimente, cu livrare garantată și mai multe instanțe ale serviciului de notificări.
- Tiparul transactional outbox sau saga, pentru consistența completă între servicii la eșecuri parțiale.
- Circuit breaker (Resilience4j) pe apelurile interne.
- Tokenuri RS256 cu cheie publică (JWKS) și tokenuri de reîmprospătare.
- Stocarea fotografiilor într-un serviciu de stocare de obiecte.
- Căutare după titlu, anularea licitațiilor programate, notificări prin email.
