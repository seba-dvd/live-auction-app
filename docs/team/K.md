# Ghidul lui K — Scrum Master · auction-service + baza de date

## 1. Pe scurt

- **Deții:** `auction-service` (licitații, fotografii, ciclul de viață, anti-sniping) și designul bazei de date (`docs/database/`).
- **Ramura ta:** `k/auction`. PR-urile tale le revizuiește **M**; tu revizuiești PR-urile lui **A**.
- **Rolul de curs:** Scrum Master. Conduci ceremoniile, ții board-ul la zi și elimini blocajele.
- **Primele 3 acțiuni săptămâna asta:**
  1. creează board-ul GitHub Project și calendarul întâlnirilor;
  2. anunță regula stand-up-ului asincron în chat;
  3. conduci primul sprint planning (S1, 09.11).
- **Ai un `Clock` injectat în auction-service.** Folosește-l peste tot în loc de `Instant.now()`, ca să poți testa ciclul de viață cu timp fix.

## 2. Rolul tău

| Responsabilitate | Frecvență |
|---|---|
| Sprint planning (45 min): obiectivul sprintului și issues mutate în milestone; A aduce prioritățile | prima zi a fiecărui sprint |
| Stand-up asincron: citești mesajele „Ieri / Azi / Blocaje” până la 22:00 și reacționezi la blocaje | zilnic |
| Sprint review (25 min, demo) + retrospectivă (20 min, o acțiune concretă de îmbunătățire) | ultima zi a sprintului |
| Ții board-ul la zi (coloanele Todo / In progress / In review / Done) | de 2–3 ori pe săptămână |
| Escaladezi blocajele nerezolvate în 48 h către D (check-in săptămânal de 15 min) | săptămânal |
| Verifici că fiecare `V1__init.sql` respectă designul și convențiile bazei de date | S1, apoi la fiecare migrație nouă |
| Scrii secțiunea despre metodologie din Raport | S1–S2 |

## 3. Ce deții

| Al tău | Doar prin PR, cu proprietarul ca reviewer |
|---|---|
| `auction-service/**` | `user-service/**/db/migration` (D), `bidding-service/**/db/migration` (M): le revizuiești, nu le scrii |
| `docs/database/**` (README + diagramele ER) | `docs/api-contracts.md` (M), `docker-compose*.yml` (R) |

**Nu atinge** codul din celelalte servicii și din `frontend/`.

## 4. Setup (o singură dată)

1. **Instalează:**
   - Git;
   - Docker Desktop cu WSL2;
   - JDK 21 Temurin (<https://adoptium.net/temurin/releases/?version=21>);
   - IntelliJ IDEA (licența de student);
   - Postman;
   - MySQL Workbench (<https://dev.mysql.com/downloads/workbench/>), pentru diagramele EER.
2. **Acceptă invitația** la repository.
3. **Clonează și configurează:**
   ```bash
   git clone https://github.com/seba-dvd/live-auction-app.git
   cd live-auction-app
   git checkout k/auction
   cp .env.example .env
   docker compose up -d --build
   ```
4. **Conectează MySQL Workbench:** `localhost:3306`, utilizator `auction_service`, parolă `auction-service-dev-pw` (sau `root` / `root-dev-password` pentru toate schemele).
5. **Deschide `auction-service/pom.xml` în IntelliJ** (SDK 21).

## 5. Cum rulezi și testezi partea ta

**Serviciul tău în IntelliJ, restul în Docker:**
```bash
docker compose stop auction-service
# în .env decomentează:  DOCKER_AUCTION_SERVICE_URL=http://host.docker.internal:8082
docker compose up -d
```
Rulează `AuctionServiceApplication` din IntelliJ. Fotografiile se salvează local în `auction-service/uploads/`, care e ignorat de git.

**Fără user-service sau notification-service:** rulează cu profilul `stub`. Clienții `WalletClient` și `NotificationClient` folosesc atunci implementările din memorie.

**Testare directă:**
```bash
curl -s -X POST http://localhost:8082/api/auctions -H "X-User-Id: 3" -H "Content-Type: application/json" \
     -d '{"title":"Aparat foto","description":"Funcțional","startingPrice":100,"minIncrement":10,"startTime":"2026-11-20T18:00:00Z","endTime":"2026-11-20T19:00:00Z"}'
curl -s "http://localhost:8082/api/auctions?status=ACTIVE&page=0&size=12"
curl -s http://localhost:8082/internal/auctions/1 -H "X-Internal-Key: dev-only-internal-api-key"
```

**Teste și imagine:**
- **Teste:** `./mvnw -B verify`. În profilul `test`, jobul programat e oprit (`app.scheduling.enabled=false`), deci îl apelezi direct din test, cu un `Clock` fix.
- **Reconstruiește doar containerul tău:** `docker compose up -d --build auction-service`.

## 6. Plan pe sprinturi

### S0 · Setup (28.10–08.11)

- [ ] **K-S0-01 · Board-ul GitHub Project și calendarul întâlnirilor**
  - **Ce:**
    - proiectul „Live Auction – Scrum” (coloane Todo / In progress / In review / Done), legat de repository;
    - adaugi toate issue-urile;
    - fixezi datele pentru planning și review pentru fiecare sprint.
  - **Gata când:** board-ul arată toate issue-urile S0–S1; calendarul e anunțat în chat.
  - **Depinde de:** D-S0-01 (sau `gh auth refresh -s project` pentru D).
  - **Etichete:** `area:docs` `type:chore` `priority:must`
- [ ] **K-S0-02 · Regula stand-up-ului asincron**
  - **Ce:** mesajul fixat în chat cu formatul „Ieri / Azi / Blocaje”, termenul 22:00 și ce se întâmplă cu blocajele.
  - **Gata când:** toți au postat cel puțin un stand-up în S0.
  - **Depinde de:** —
  - **Etichete:** `area:docs` `type:chore` `priority:must`
- [ ] **K-S0-03 · Primul sprint planning (S1)**
  - **Ce:** obiectivul S1 și issues mutate în milestone-ul S1, cu A pentru priorități.
  - **Gata când:** milestone-ul S1 are toate task-urile asumate, fiecare cu un responsabil.
  - **Depinde de:** K-S0-01.
  - **Etichete:** `area:docs` `type:chore` `priority:must`

### S1 · Design & fundații (09.11–22.11)

- [ ] **K-S1-01 · Designul final al bazei de date (toate schemele)**
  - **Ce:**
    - parcurgi `user_db` cu D și `bidding_db` cu M, plus `auction_db`;
    - corectezi `V1__init.sql`, `docs/database/README.md` și diagramele ER;
    - opțional, generezi și EER-ul din Workbench (Reverse Engineer).
  - **Gata când:** cele trei `V1__init.sql` rulează în Compose fără erori, iar documentul și diagramele corespund cu SQL-ul.
  - **Depinde de:** —
  - **Etichete:** `area:docs` `type:docs` `priority:must`
- [ ] **K-S1-02 · Entitățile Item, ItemPhoto, Auction și enum-urile**
  - **Ce:** `AuctionStatus` și `SettlementStatus` (`@Enumerated(EnumType.STRING)`), relațiile 1:1 și 1:N din schemă, `@Version` pe `Auction`.
  - **Gata când:** serviciul pornește cu `ddl-auto: validate`, iar `./mvnw verify` e verde.
  - **Depinde de:** K-S1-01.
  - **Etichete:** `area:auction` `type:feature` `priority:must`
- [ ] **K-S1-03 · POST /api/auctions cu validări**
  - **Ce:**
    - `start < end` și durata între 1 minut și 7 zile, altfel `INVALID_AUCTION_TIMES`;
    - prețurile ≥ 1;
    - statusul inițial e `ACTIVE` dacă `startTime ≤ now`;
    - `currentPrice = startingPrice` și `originalEndTime = endTime`.
  - **Gata când:** răspunde 201 cu `Location`; testele acoperă toate validările.
  - **Depinde de:** K-S1-02.
  - **Etichete:** `area:auction` `type:feature` `priority:must`
- [ ] **K-S1-04 · GET /api/auctions (filtru, paginare, sortare) și GET /api/auctions/{id}**
  - **Ce:** `PagedModel<AuctionSummary>` filtrat după `status` și `AuctionDetails` cu `serverTime`, conform [contracte §6](../api-contracts.md#6-auction-service-api-public).
  - **Gata când:** cererile din Postman trec; 404 `AUCTION_NOT_FOUND` e tratat.
  - **Depinde de:** K-S1-02.
  - **Etichete:** `area:auction` `type:feature` `priority:must`
- [ ] **K-S1-05 · Finalizează ADR-004 și diagrama de clase auction-service**
  - **Ce:** ADR-004 primește statusul „Acceptat”; `docs/uml/class-auction-service.puml` reflectă implementarea; îi trimiți lui M ce s-a schimbat.
  - **Gata când:** diagrama e regenerată și inclusă în ansamblu.
  - **Depinde de:** K-S1-02.
  - **Etichete:** `area:docs` `type:uml` `priority:should`

### S2 · Fluxuri de bază (23.11–06.12)

- [ ] **K-S2-01 · Jobul de ciclu de viață: SCHEDULED → ACTIVE → ENDED**
  - **Ce:**
    - `@Scheduled(fixedDelay = 1000)`, cu `Clock` injectat;
    - pornire la `startTime ≤ now`;
    - închidere: lock, re-verificare, apoi `ENDED`, `winnerId`, `finalPrice` și `settlement_status = PENDING`.
  - **Gata când:** testele cu `Clock.fixed(...)` verifică ambele tranziții, inclusiv licitația prelungită care **nu** se închide.
  - **Depinde de:** K-S1-02.
  - **Etichete:** `area:auction` `type:feature` `priority:must`
- [ ] **K-S2-02 · GET /internal/auctions/{id}**
  - **Ce:** endpoint-ul intern pentru bidding-service, protejat cu filtrul `X-Internal-Key` (401 `INTERNAL_KEY_INVALID`).
  - **Gata când:** cererea din folderul „internal” al colecției Postman trece; fără cheie, răspunsul e 401.
  - **Depinde de:** K-S1-04.
  - **Etichete:** `area:auction` `type:feature` `priority:must`
- [ ] **K-S2-03 · POST /internal/auctions/{id}/bid-placed: lock și anti-sniping**
  - **Ce:**
    - `PESSIMISTIC_WRITE` pe licitație;
    - 409 `AUCTION_NOT_ACTIVE` dacă `status ≠ ACTIVE` sau `bidAt ≥ endTime`;
    - actualizezi `currentPrice`, `highestBidderId` și `bidCount`;
    - dacă `endTime − bidAt < 30 s`, faci `endTime += 30 s` și `extensionCount++`;
    - răspunzi `{endTime, extended}`.
  - **Gata când:** testele cu `Clock` fix acoperă: cu prelungire, fără prelungire, după expirare (409), licitație inactivă (409).
  - **Depinde de:** K-S2-02.
  - **Etichete:** `area:auction` `type:feature` `priority:must`
- [ ] **K-S2-04 · Încărcarea și servirea fotografiilor**
  - **Ce:**
    - `POST /api/auctions/{id}/photos`: doar vânzătorul; maximum 5 în total; doar jpeg/png/webp (verifică și conținutul, nu doar extensia); maximum 5 MB; nume UUID; salvare în `app.upload-dir`;
    - `GET /api/auctions/photos/{filename}`, cu `Content-Type` corect.
  - **Gata când:**
    - erorile `NOT_AUCTION_OWNER`, `TOO_MANY_PHOTOS`, `UNSUPPORTED_PHOTO_TYPE` și `PHOTO_TOO_LARGE` funcționează;
    - în Docker, fotografiile supraviețuiesc unui `docker compose restart` (volumul `auction-uploads`).
  - **Depinde de:** K-S1-03.
  - **Etichete:** `area:auction` `type:feature` `priority:should`
- [ ] **K-S2-05 · Evenimentul AUCTION_STARTED**
  - **Ce:** la pornirea unei licitații, trimiți evenimentul prin `NotificationClient`, după commit.
  - **Gata când:** `tools/ws-test.html`, abonat la `/topic/auctions/{id}`, primește evenimentul.
  - **Depinde de:** K-S2-01, R-S1-02.
  - **Etichete:** `area:auction` `type:feature` `priority:should`
- [ ] **K-S2-06 · Raport Tehnic: capitolele 2 și 7**
  - **Ce:** revizuiești și completezi `02-metodologia.md` și `07-baza-de-date.md` cu deciziile reale.
  - **Gata când:** cap. 2 e pe `develop` până pe 20.11, iar cap. 7 până pe 24.11, cu D ca reviewer.
  - **Depinde de:** K-S1-01.
  - **Etichete:** `area:docs` `type:docs` `priority:must`

### S3 · Timp real & integrare (07.12–20.12)

- [ ] **K-S3-01 · Închiderea cu decontare și reîncercarea PENDING**
  - **Ce:**
    - după commit-ul stării `ENDED`, apelezi `POST /internal/wallet/settlements` (`WalletClient`);
    - la succes: `DONE`;
    - la eșec: rămâne `PENDING` și se reîncearcă la fiecare tick.
  - **Gata când:** testul cu `WalletClient` care eșuează o dată și apoi reușește ajunge la `DONE` și decontează o singură dată.
  - **Depinde de:** K-S2-01, D-S2-02.
  - **Etichete:** `area:auction` `type:feature` `priority:must`
- [ ] **K-S3-02 · Evenimentele AUCTION_ENDED, AUCTION_WON și AUCTION_SOLD**
  - **Ce:** după decontarea reușită, `ENDED` pe topic. Dacă au existat oferte, mai trimiți `WON` către câștigător și `SOLD` către vânzător.
  - **Gata când:** în demo-ul cu două browsere, ambii utilizatori primesc notificarea lor.
  - **Depinde de:** K-S3-01, R-S2-01.
  - **Etichete:** `area:auction` `type:feature` `priority:must`
- [ ] **K-S3-03 · GET /api/auctions/mine**
  - **Ce:** licitațiile apelantului ca vânzător, paginat.
  - **Gata când:** cererea din Postman trece cu JWT, iar gateway-ul o protejează.
  - **Depinde de:** K-S1-04.
  - **Etichete:** `area:auction` `type:feature` `priority:should`
- [ ] **K-S3-04 · Teste pentru ciclul de viață și anti-sniping cu `Clock` fix**
  - **Ce:** scenarii complete: creare, pornire, oferte, prelungire, închidere și decontare, cu timpul controlat.
  - **Gata când:** cel puțin 8 teste verzi în CI.
  - **Depinde de:** K-S3-01.
  - **Etichete:** `area:auction` `type:feature` `priority:must`
- [ ] **K-S3-05 · Diagramele de activitate și de stări (finalizare)**
  - **Ce:** actualizezi `activity-auction-lifecycle.puml`, `state-auction.puml` și `sequence-auction-close.puml` după implementare.
  - **Gata când:** diagramele sunt regenerate și corespund codului.
  - **Depinde de:** K-S3-01.
  - **Etichete:** `area:docs` `type:uml` `priority:should`
- [ ] **K-S3-06 · Postman: aserțiuni pentru auctions**
  - **Ce:** teste pentru toate cererile din folderul „auction-service” (status, câmpuri, erori).
  - **Gata când:** folderul e verde în Newman (CI).
  - **Depinde de:** R-S2-02.
  - **Etichete:** `area:auction` `type:feature` `priority:must`

### S4 · Cloud & final (04.01–17.01)

- [ ] **K-S4-01 · (stretch) Anularea unei licitații programate**
  - **Ce:** endpoint nou, doar pentru vânzător și doar pentru starea `SCHEDULED` (contract nou aprobat de M).
  - **Gata când:** US-18 e acceptată de A.
  - **Depinde de:** —
  - **Etichete:** `area:auction` `type:feature` `priority:could`
- [ ] **K-S4-02 · (stretch) Căutare după titlu**
  - **Ce:** parametrul `q` la `GET /api/auctions`, fără diferențe între majuscule și minuscule.
  - **Gata când:** US-19 e acceptată de A.
  - **Depinde de:** —
  - **Etichete:** `area:auction` `type:feature` `priority:could`
- [ ] **K-S4-03 · Retrospectiva întregului proiect**
  - **Ce:** ce a mers, ce nu și ce am învățat, sub formă de slide-uri pentru prezentarea finală.
  - **Gata când:** slide-urile sunt incluse în prezentare.
  - **Depinde de:** —
  - **Etichete:** `area:docs` `type:docs` `priority:should`

## 7. Specificație tehnică

### 7.1 Endpoint-uri pe care le expui

| Endpoint | Auth | Detalii |
|---|---|---|
| `POST /api/auctions` | JWT (`X-User-Id`) | [contracte §6.1](../api-contracts.md#6-auction-service-api-public) |
| `POST /api/auctions/{id}/photos` | JWT, doar vânzătorul | §6.2 |
| `GET /api/auctions/photos/{filename}`, `GET /api/auctions`, `GET /api/auctions/{id}` | public | §6.3–6.5 |
| `GET /api/auctions/mine` | JWT | §6.6 |
| `GET /internal/auctions/{id}`, `POST /internal/auctions/{id}/bid-placed` | `X-Internal-Key` | §8.2 |

### 7.2 Ce consumi

**Apeluri către alte servicii:**
- `POST /internal/wallet/settlements` (user-service, D);
- `POST /internal/events` (notification-service, R).

Ambele merg prin interfețe din `client`, cu implementare `@Profile("stub")`. Clientul REST cu timeouts arată ca în ghidul lui M (§7.3): `SimpleClientHttpRequestFactory` cu 2 s / 5 s și `X-Internal-Key` ca header implicit.

**Tabelele tale (`auction_db`):** `items`, `item_photos`, `auctions`, cu detaliile în [database/README §4](../database/README.md#4-auction_db-auction-service-k). Indexurile pe `(status, start_time)` și `(status, end_time)` există pentru jobul tău.

**Clase recomandate:**
- `entity`: `Item`, `ItemPhoto`, `Auction` (cu metodele `start()`, `end()`, `applyBid(...)`, care conțin regulile stării);
- `service`: `AuctionService`, `PhotoService`, `BidPlacementService`, `AuctionLifecycleJob`;
- `client`: `WalletClient`, `NotificationClient`.

### 7.3 Codul care previne greșelile clasice

**Timpul vine din `Clock`.** În teste înlocuiești bean-ul `Clock` cu `Clock.fixed(...)`:

```java
@Bean
Clock clock() {
    return Clock.systemUTC();
}
```

**Lock-ul pe licitație la `bid-placed`.** Același tipar ca în ghidul lui M, cu `@Lock(LockModeType.PESSIMISTIC_WRITE)` pe o metodă `findByIdForUpdate` din `AuctionRepository`.

### 7.4 Decizii și capcane

- **Închiderea în doi pași:**
  1. tranzacția 1: lock, re-verificare, `ENDED` + `PENDING`, apoi commit;
  2. **după** commit, apelul HTTP de decontare.
  
  Nu ține lock-ul bazei de date pe durata unui apel HTTP.
- **Re-verifică `endTime` după lock:** între interogare și lock, anti-sniping poate muta sfârșitul.
- **Un singur tick lent nu blochează următorul:** `fixedDelay` așteaptă terminarea tick-ului. Procesează licitațiile pe rând, fiecare în tranzacția ei, ca o eroare să nu oprească restul.
- **Fotografii:**
  - verifică tipul real (primii octeți sau `ImageIO`), nu doar `Content-Type`-ul trimis de client;
  - numele de pe disc este UUID + extensie;
  - nu construi niciodată calea din `{filename}` fără să validezi formatul UUID (atacuri de tip `../../`).
- **Câmpuri:**
  - `currentPrice` pornește egal cu `startingPrice`;
  - `bidCount = 0` înseamnă „fără oferte”, deci `winnerId` și `finalPrice` rămân `null` la închidere.
- **`@Scheduled` în teste:** e oprit în profilul `test`. Apelează direct `auctionLifecycleJob.tick()`.

> **Spring Boot 4 vs. tutoriale Boot 3**
> - Hibernate 7 + MySQL: în acest proiect `Instant` se mapează pe `DATETIME(6)` prin `hibernate.type.preferred_instant_jdbc_type: TIMESTAMP` (deja configurat). Nu schimba coloanele în `TIMESTAMP`.
> - Upload multipart: limitele sunt în `spring.servlet.multipart.*` (deja 5 MB / 30 MB). Pentru excepția de dimensiune, prinde `MaxUploadSizeExceededException` și transform-o în `PHOTO_TOO_LARGE`.
> - `@ConditionalOnProperty` și `@EnableScheduling` funcționează la fel. Vezi `SchedulingConfig`.
> - În teste: `@MockitoBean` în loc de `@MockBean`; `@DataJpaTest` este în `org.springframework.boot.data.jpa.test.autoconfigure`.

## 8. Dependențe

| Aștepți de la | Ce | Cum te deblochezi |
|---|---|---|
| D | decontările (`/internal/wallet/settlements`) | `StubWalletClient` (răspunde 200) |
| R | `/internal/events` | `StubNotificationClient` (doar loghează) |
| D | gateway cu JWT | trimiți manual `X-User-Id` |

| Așteaptă de la tine | Ce | Când |
|---|---|---|
| M | `GET /internal/auctions/{id}`, `bid-placed` | S2 (M are stub până atunci) |
| A | listele, detaliile, crearea, fotografiile | S2 |
| toți | designul final al bazei de date | S1 |

## 9. Documentație

| Ce | Fișier | Termen |
|---|---|---|
| Raport cap. 2 (metodologia) | `docs/raport-tehnic/src/02-metodologia.md` | 20.11 |
| Raport cap. 7 (structura bazei de date) | `docs/raport-tehnic/src/07-baza-de-date.md` | 24.11 |
| Diagramele ER (pe scheme + ansamblu) | `docs/database/er-*.puml` | S1 |
| Diagramele de activitate, de stări, secvența de închidere | `docs/uml/activity-…`, `state-…`, `sequence-auction-close.puml` | S3 |
| ADR-004 | `docs/decisions/ADR-004-database-per-service.md` | 22.11 |

## 10. Git zilnic

```bash
git checkout k/auction
git fetch origin && git merge origin/develop
# ... lucrezi ...
git add auction-service/ docs/database/
git commit -m "feat(auction): close expired auctions and request settlement"
git push origin k/auction
gh pr create --base develop --head k/auction --title "feat(auction): lifecycle job" --body "Closes #<nr>"
```

**Conflicte de merge:** [CONTRIBUTING §5](../../CONTRIBUTING.md#5-conflicte-de-merge). După 30.11, schemele se schimbă **doar** prin migrații noi `V2__…`.

## 11. Definition of Done

- [ ] `./mvnw -B verify` e verde;
- [ ] criteriile „Gata când…” sunt îndeplinite;
- [ ] tranzițiile de stare și anti-sniping-ul au teste cu `Clock` fix;
- [ ] contractele, colecția Postman, `docs/database/README.md` și diagramele ER sunt actualizate;
- [ ] PR-ul e aprobat de M, iar CI-ul e verde;
- [ ] funcționează în stack-ul complet.

## 12. Resurse și ajutor

- **Scrum Guide 2020:** <https://scrumguides.org/scrum-guide.html>
- **GitHub Projects:** <https://docs.github.com/en/issues/planning-and-tracking-with-projects>
- **Task scheduling în Spring:** <https://docs.spring.io/spring-framework/reference/integration/scheduling.html>
- **Spring Data JPA, paginare și sortare:** <https://docs.spring.io/spring-data/jpa/reference/repositories/query-methods-details.html>
- **Flyway:** <https://documentation.red-gate.com/fd/>
- **MySQL Workbench, reverse engineering:** <https://dev.mysql.com/doc/workbench/en/wb-reverse-engineering.html>
- **Pe cine întrebi:**
  - fluxul ofertelor și contractele: **M**;
  - decontările: **D**;
  - evenimentele WebSocket și Docker: **R**;
  - ce afișează UI-ul: **A**.
- **Dacă folosești un asistent AI:** pune-l să citească întâi `CLAUDE.md`, ghidul acesta și `docs/api-contracts.md`.
