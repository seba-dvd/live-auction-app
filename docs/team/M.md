# Ghidul lui M — Technical Lead · bidding-service

## 1. Pe scurt

- **Deții:** `bidding-service` (plasarea ofertelor cu lock per licitație, istoricul ofertelor), `docs/api-contracts.md`, `docs/architecture.md`, ADR-urile și diagramele UML.
- **Ramura ta:** `m/bidding`. PR-urile tale le revizuiește **D**; tu revizuiești PR-urile lui **D** și **K**.
- **Rolul de curs:** Technical Lead. Aprobi orice schimbare de contract și ai ultimul cuvânt în disputele tehnice.
- **Primele 3 acțiuni săptămâna asta:**
  1. citește `api-contracts.md` și `architecture.md` și confirmă-le cu D (sau propune corecturi prin PR);
  2. prezintă arhitectura echipei (30 min);
  3. pornește stack-ul și rulează `bidding-service` din IntelliJ.
- **Fluxul cel mai complex al proiectului îți aparține:** `POST /api/bids`. Citește de două ori [architecture.md §6.1](../architecture.md#61-plasarea-unei-oferte) și [ADR-001](../decisions/ADR-001-bid-concurrency.md).

## 2. Rolul tău

| Responsabilitate | Frecvență |
|---|---|
| Revizuiești și aprobi orice PR care modifică `docs/api-contracts.md` | la cerere, în 24 h |
| Revizuiești PR-urile lui D și K (backend), cu atenție la contracte, tranzacții și teste | la cerere, în 24 h |
| Conduci ziua de integrare („merge day”) cu D: toate ramurile intră în `develop`, rulezi scenariul complet | o dată pe sprint, înaintea review-ului |
| Ții la zi `architecture.md` și ADR-urile; scrii un ADR pentru fiecare decizie nouă | la nevoie |
| Asamblezi diagrama de clase de ansamblu din contribuțiile tuturor | S1, apoi la schimbări |
| Stabilești convențiile de cod (vezi `CLAUDE.md`) și le aplici în review-uri | continuu |
| Decizi în disputele tehnice (după ce asculți ambele variante) | la nevoie |

## 3. Ce deții

| Al tău | Doar prin PR, cu proprietarul ca reviewer |
|---|---|
| `bidding-service/**` | `docker-compose*.yml`, `.github/` (R) |
| `docs/api-contracts.md`, `docs/architecture.md`, `docs/decisions/**`, `docs/uml/**` | `docs/database/**` (K), `docs/team/**` (D) |

**Nu atinge** `user-service/`, `auction-service/`, `notification-service/` și `frontend/`. Când ai nevoie de ceva acolo, deschide un issue pentru proprietar.

## 4. Setup (o singură dată)

1. **Instalează:**
   - Git (<https://git-scm.com/downloads>);
   - Docker Desktop cu WSL2 (<https://www.docker.com/products/docker-desktop/>);
   - JDK 21 Temurin (<https://adoptium.net/temurin/releases/?version=21>);
   - IntelliJ IDEA (licența de student: <https://www.jetbrains.com/community/education/>), cu plugin-ul **PlantUML Integration**;
   - Postman (<https://www.postman.com/downloads/>).
2. **Acceptă invitația** la repository (email de la GitHub).
3. **Clonează și configurează:**
   ```bash
   git clone https://github.com/seba-dvd/live-auction-app.git
   cd live-auction-app
   git checkout m/bidding
   cp .env.example .env
   docker compose up -d --build
   ```
4. **Deschide `bidding-service/pom.xml` în IntelliJ** (Open as Project, SDK 21).

## 5. Cum rulezi și testezi partea ta

**Varianta hibridă:** serviciul tău în IntelliJ, restul în Docker.
```bash
docker compose stop bidding-service
# în .env decomentează:  DOCKER_BIDDING_SERVICE_URL=http://host.docker.internal:8083
docker compose up -d
```
Rulează `BiddingServiceApplication` din IntelliJ. Serviciul apelează auction- și user-service pe `localhost:8082` / `8081` (porturi publicate de `docker-compose.override.yml`).

**Fără celelalte servicii:**
- **Profilul `stub`:** rulează cu el (`-Dspring-boot.run.profiles=stub` sau „Active profiles: stub” în IntelliJ), iar clienții folosesc implementările din memorie.
- **MySQL temporar:** rulează `TestBiddingServiceApplication` (din `src/test`), care pornește un MySQL Testcontainers, fără Compose.

**Testare directă**, cu header-ele pe care le pune gateway-ul:
```bash
curl -s -X POST http://localhost:8083/api/bids -H "X-User-Id: 7" -H "X-User-Name: ana.pop" \
     -H "Content-Type: application/json" -d '{"auctionId":42,"amount":150}'
curl -s "http://localhost:8083/api/bids/auction/42?page=0&size=20"
```

**Teste și imagine:**
- **Teste:** `./mvnw -B verify`. `MySqlSchemaTests` rulează doar dacă Docker merge și verifică migrațiile față de entitățile tale.
- **Reconstruiește doar containerul tău:** `docker compose up -d --build bidding-service`.

## 6. Plan pe sprinturi

### S0 · Setup (28.10–08.11)

- [ ] **M-S0-01 · Revizuiește contractele și convențiile cu D**
  - **Ce:** citești `api-contracts.md`, `architecture.md`, `CLAUDE.md` și propui corecturi prin PR.
  - **Gata când:** contractele v1 sunt confirmate în „Istoricul versiunilor”, cu tine ca aprobator.
  - **Depinde de:** —
  - **Etichete:** `area:docs` `type:docs` `priority:must`
- [ ] **M-S0-02 · Prezintă arhitectura echipei (30 min)**
  - **Ce:**
    - componentele;
    - fluxul de plasare a unei oferte;
    - regula „banii se mută doar sub lock, notificările după commit”;
    - profilul `stub`.
  - **Gata când:** prezentarea a avut loc, iar întrebările deschise sunt notate în issues.
  - **Depinde de:** M-S0-01.
  - **Etichete:** `area:docs` `type:docs` `priority:must`

### S1 · Design & fundații (09.11–22.11)

- [ ] **M-S1-01 · Entități și repository-uri: Bid, AuctionBidState**
  - **Ce:** entitățile mapate pe `V1__init.sql`, `BidRepository` (paginare), `AuctionBidStateRepository` cu `findByIdForUpdate` (lock) și `insertIfAbsent` (§7.3).
  - **Gata când:** `MySqlSchemaTests` e verde (Docker), iar serviciul pornește cu `validate`.
  - **Depinde de:** —
  - **Etichete:** `area:bidding` `type:feature` `priority:must`
- [ ] **M-S1-02 · Clienții AuctionClient, WalletClient, NotificationClient**
  - **Ce:**
    - interfețe în `client`;
    - implementări HTTP cu `RestClient` (timeouts 2 s / 5 s, `X-Internal-Key`; §7.3);
    - implementări `@Profile("stub")` în memorie;
    - traducerea erorilor: 409 → excepție de domeniu, timeout → 503 `SERVICE_UNAVAILABLE`.
  - **Gata când:** serviciul pornește cu și fără profilul `stub`; există teste pentru traducerea erorilor.
  - **Depinde de:** —
  - **Etichete:** `area:bidding` `type:feature` `priority:must`
- [ ] **M-S1-03 · Istoricul ofertelor: GET /api/bids/auction/{auctionId}**
  - **Ce:** `PagedModel<BidHistoryItem>`, cele mai noi primele, rută publică.
  - **Gata când:** cererea din Postman trece; paginarea are forma din contract.
  - **Depinde de:** M-S1-01.
  - **Etichete:** `area:bidding` `type:feature` `priority:must`
- [ ] **M-S1-04 · Tratarea erorilor (ProblemDetail + code)**
  - **Ce:** `@RestControllerAdvice` cu `ApiException(status, code, message)`, `VALIDATION_FAILED` cu `errors[]` și 500 `INTERNAL_ERROR` fără detalii interne.
  - **Gata când:** un test MockMvc verifică formatul pentru 400 și 409.
  - **Depinde de:** —
  - **Etichete:** `area:bidding` `type:feature` `priority:must`
- [ ] **M-S1-05 · Diagrama de clase de ansamblu (Ședințele 4–5)**
  - **Ce:**
    - strângi modificările de la D, K și R;
    - actualizezi `docs/uml/class-diagram.puml` și diagrama bidding;
    - regenerezi imaginile.
  - **Gata când:** diagramele sunt prezentate la Ședințele 4–5, iar PNG-urile sunt comise.
  - **Depinde de:** D-S1-07, K-S1-02.
  - **Etichete:** `area:docs` `type:uml` `priority:must`
- [ ] **M-S1-06 · Îngheață contractele v1**
  - **Ce:** ultimele corecturi și intrarea „v1 înghețat” în istoric. De aici, schimbările incompatibile se fac doar cu acordul celor afectați.
  - **Gata când:** PR-ul e integrat pe `develop` până pe 22.11.
  - **Depinde de:** M-S0-01.
  - **Etichete:** `area:docs` `type:docs` `priority:must`

### S2 · Fluxuri de bază (23.11–06.12)

- [ ] **M-S2-01 · POST /api/bids: fluxul complet**
  - **Ce:** pașii 1–6 din [architecture §6.1](../architecture.md#61-plasarea-unei-oferte), într-o singură metodă `@Transactional`:
    - validare;
    - `ensureExists` (tranzacție separată) și lock;
    - suma minimă;
    - rezervare;
    - `bid-placed`;
    - insert și actualizarea stării.
  - **Gata când:** răspunsul e 201 conform contractului, iar erorile sunt `BID_TOO_LOW`, `OWN_AUCTION`, `AUCTION_NOT_ACTIVE`, `INSUFFICIENT_FUNDS`.
  - **Depinde de:** M-S1-01, M-S1-02, D-S2-01, K-S2-03 (sau stub-urile).
  - **Etichete:** `area:bidding` `type:feature` `priority:must`
- [ ] **M-S2-02 · Compensarea și eliberarea fostului lider**
  - **Ce:**
    - la 409 de la `bid-placed`: restaurezi rezervarea anterioară (licitantul era deja lider) sau o ștergi;
    - după succes: `DELETE` pe rezervarea fostului lider, doar dacă e alt utilizator (la eroare doar loghezi).
  - **Gata când:** există teste unitare pentru ambele ramuri de compensare și pentru „același lider își mărește oferta”.
  - **Depinde de:** M-S2-01.
  - **Etichete:** `area:bidding` `type:feature` `priority:must`
- [ ] **M-S2-03 · Evenimentele după commit: OUTBID, BID_PLACED**
  - **Ce:** `ApplicationEventPublisher` plus `@TransactionalEventListener(AFTER_COMMIT)` (§7.3). Construiești anvelopele din [contracte §9](../api-contracts.md#9-websocket--stomp-și-evenimente).
  - **Gata când:** cu notification-service pornit, `tools/ws-test.html` primește `BID_PLACED`; o tranzacție eșuată nu trimite nimic.
  - **Depinde de:** M-S2-01, R-S1-02.
  - **Etichete:** `area:bidding` `type:feature` `priority:must`
- [ ] **M-S2-04 · Teste unitare cu clienții simulați**
  - **Ce:** Mockito pe `AuctionClient` / `WalletClient`. Acoperi toate erorile, sumele minime (cu și fără oferte) și compensarea.
  - **Gata când:** cel puțin 10 teste pentru `BidService`, toate verzi în CI.
  - **Depinde de:** M-S2-02.
  - **Etichete:** `area:bidding` `type:feature` `priority:must`
- [ ] **M-S2-05 · Finalizează ADR-001 și ADR-003**
  - **Ce:** confirmi deciziile (sau le schimbi) pe baza implementării. Statusul devine „Acceptat”.
  - **Gata când:** ambele ADR-uri sunt acceptate și referite în Raport.
  - **Depinde de:** M-S2-01.
  - **Etichete:** `area:docs` `type:docs` `priority:should`
- [ ] **M-S2-06 · Raport Tehnic: capitolele 4 și 6**
  - **Ce:** revizuiești și completezi `04-arhitectura.md` și `06-diagrama-de-clase.md` cu ce s-a implementat.
  - **Gata când:** capitolele sunt pe `develop` până pe 24.11, cu D ca reviewer.
  - **Depinde de:** M-S1-05.
  - **Etichete:** `area:docs` `type:docs` `priority:must`

### S3 · Timp real & integrare (07.12–20.12)

- [ ] **M-S3-01 · Test de concurență (Testcontainers MySQL)**
  - **Ce:** 50 de oferte paralele la aceeași licitație, cu clienții externi stub care răspund instant. Verifici trei lucruri:
    - un singur lider;
    - sumele acceptate strict crescătoare;
    - `bid_count` egal cu numărul de rânduri din `bids` (fără lost update).
  - **Gata când:** testul trece de 10 ori la rând local și în CI.
  - **Depinde de:** M-S2-01.
  - **Etichete:** `area:bidding` `type:feature` `priority:must`
- [ ] **M-S3-02 · GET /api/bids/mine**
  - **Ce:** ofertele apelantului, paginat, cele mai noi primele.
  - **Gata când:** cererea din Postman trece cu JWT; fără JWT, gateway-ul dă 401.
  - **Depinde de:** M-S1-03.
  - **Etichete:** `area:bidding` `type:feature` `priority:should`
- [ ] **M-S3-03 · GET /internal/bids/auction/{auctionId}/highest**
  - **Ce:** oferta maximă, sau 204 dacă nu există, cu `X-Internal-Key`.
  - **Gata când:** cererea din folderul „internal” al colecției Postman trece.
  - **Depinde de:** M-S1-01.
  - **Etichete:** `area:bidding` `type:feature` `priority:could`
- [ ] **M-S3-04 · Test end-to-end anti-sniping (cu K)**
  - **Ce:** o licitație cu sfârșitul peste 20 s; o ofertă la secunda 15 trebuie să mute sfârșitul cu +30 s, iar evenimentul `BID_PLACED` să aibă `extended: true`.
  - **Gata când:** scenariul e automatizat în Postman sau ca test de integrare.
  - **Depinde de:** K-S2-03.
  - **Etichete:** `area:bidding` `type:feature` `priority:must`
- [ ] **M-S3-05 · Postman: aserțiuni pentru bidding**
  - **Ce:** teste pentru toate cererile din folderul „bidding-service”, inclusiv cazurile de eroare.
  - **Gata când:** folderul e verde în Newman (CI).
  - **Depinde de:** R-S2-02.
  - **Etichete:** `area:bidding` `type:feature` `priority:must`

### S4 · Cloud & final (04.01–17.01)

- [ ] **M-S4-01 · (stretch) RabbitMQ pentru evenimente**
  - **Ce:** înlocuiești `POST /internal/events` cu publicarea în RabbitMQ (cu R), plus un ADR nou.
  - **Gata când:** evenimentele ajung și dacă notification-service repornește.
  - **Depinde de:** —
  - **Etichete:** `area:bidding` `type:feature` `priority:could`
- [ ] **M-S4-02 · (opțional) Test de încărcare**
  - **Ce:** un script k6 sau JMeter cu 100 de utilizatori care licitează la 5 licitații timp de 2 minute.
  - **Gata când:** rezultatele (latență p95, erori) sunt notate în Raport sau în prezentare.
  - **Depinde de:** M-S3-01.
  - **Etichete:** `area:bidding` `type:feature` `priority:could`
- [ ] **M-S4-03 · Partea ta din prezentarea finală: concurență și consistență**
  - **Ce:** 3–4 slide-uri: problema, lock-ul, testul cu 50 de oferte, limitările (saga/outbox).
  - **Gata când:** prezentarea e repetată cu echipa.
  - **Depinde de:** M-S3-01.
  - **Etichete:** `area:docs` `type:docs` `priority:must`

## 7. Specificație tehnică

### 7.1 Endpoint-uri pe care le expui

| Endpoint | Auth | Detalii |
|---|---|---|
| `POST /api/bids` | JWT (`X-User-Id`, `X-User-Name`) | [contracte §7.1](../api-contracts.md#71-post-apibids-jwt) |
| `GET /api/bids/auction/{auctionId}` | public | §7.2 |
| `GET /api/bids/mine` | JWT | §7.3 |
| `GET /internal/bids/auction/{auctionId}/highest` | `X-Internal-Key` | §8.3 |

### 7.2 Ce consumi

| Serviciu | Endpoint | Folosit la |
|---|---|---|
| auction | `GET /internal/auctions/{id}` | pasul 1: stare, vânzător, preț de pornire, increment |
| user | `PUT /internal/wallet/reservations` | pasul 3: rezervare (setează suma, nu o adună) |
| auction | `POST /internal/auctions/{id}/bid-placed` | pasul 4: preț, lider, anti-sniping |
| user | `DELETE /internal/wallet/reservations?userId&auctionId` | pasul 5 și compensare |
| notification | `POST /internal/events` | pasul 7, după commit |

**Tabelele tale (`bidding_db`):**
- `bids`: istoricul; `UQ (auction_id, amount)` este plasa de siguranță;
- `auction_bid_state`: rândul blocat.

Detaliile sunt în [database/README §5](../database/README.md#5-bidding_db-bidding-service-m).

**Clase recomandate:**
- `entity`: `Bid`, `AuctionBidState`;
- `service`: `BidService`, `BidStateInitializer`, `BidQueryService`, `BidEventPublisher`;
- `client`: interfețele și implementările HTTP / stub;
- `controller`: `BidController`, `InternalBidController`.

### 7.3 Codul care previne greșelile clasice

**Lock-ul pesimist** (`SELECT … FOR UPDATE`) și **crearea idempotentă** a rândului de stare:

```java
public interface AuctionBidStateRepository extends JpaRepository<AuctionBidState, Long> {

    @Lock(LockModeType.PESSIMISTIC_WRITE)
    @Query("select s from AuctionBidState s where s.auctionId = :auctionId")
    Optional<AuctionBidState> findByIdForUpdate(@Param("auctionId") Long auctionId);

    @Modifying
    @Query(value = "INSERT IGNORE INTO auction_bid_state (auction_id, bid_count, updated_at) VALUES (:auctionId, 0, :now)",
           nativeQuery = true)
    int insertIfAbsent(@Param("auctionId") Long auctionId, @Param("now") Instant now);
}
```

**Tranzacția separată.** `ensureExists` stă într-un bean separat, ca `REQUIRES_NEW` să fie aplicat prin proxy. Altfel, două prime oferte concurente pot face deadlock:

```java
// own, short transaction: the row exists (and is committed) before placeBid() locks it
@Transactional(propagation = Propagation.REQUIRES_NEW)
public void ensureExists(long auctionId) {
    repository.insertIfAbsent(auctionId, Instant.now(clock));
}
```

**Notificările doar după commit.** Dacă tranzacția eșuează, nimeni nu primește „ai fost depășit” fals:

```java
// runs only if placeBid() committed; inside it: applicationEventPublisher.publishEvent(new BidPlacedEvent(...))
@TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
public void onBidPlaced(BidPlacedEvent event) {
    try {
        notifications.publish(event);   // build the OUTBID / BID_PLACED envelopes here
    } catch (RuntimeException ex) {
        log.warn("Notification for auction {} not delivered: {}", event.auctionId(), ex.getMessage());
    }
}
```

**Clientul REST cu timeouts.** Fără timeouts, un serviciu blocat îți ține lock-ul la nesfârșit:

```java
@Bean
RestClient auctionServiceRestClient(@Value("${app.clients.auction-service-url}") String baseUrl,
                                    @Value("${app.internal-api-key}") String internalKey) {
    SimpleClientHttpRequestFactory factory = new SimpleClientHttpRequestFactory();
    factory.setConnectTimeout(Duration.ofSeconds(2));
    factory.setReadTimeout(Duration.ofSeconds(5));
    return RestClient.builder()
            .baseUrl(baseUrl)
            .requestFactory(factory)
            .defaultHeader("X-Internal-Key", internalKey)
            .build();
}
```

### 7.4 Decizii și capcane

- **Momentul de referință:** `bidAt = Instant.now(clock)`, luat **după** ce ai obținut lock-ul. Licitația îl compară cu `endTime`.
- **Licitantul își mărește propria ofertă:** rezervarea se **setează** la noua sumă (user-service calculează diferența). Nu chema `DELETE` pe propria rezervare.
- **Compensarea** se face înainte de a arunca excepția. `@Transactional` face rollback doar în baza ta de date, nu în celelalte servicii.
- **`@Transactional` pe o metodă `private` sau apelată din aceeași clasă nu are efect** (proxy). Ține metoda publică și apelează-o din controller.
- **`bidderUsername`** vine din `X-User-Name`, adică denormalizat. Nu chema user-service pentru el.
- **Timeouts:** un timeout de la alt serviciu devine 503 `SERVICE_UNAVAILABLE`. Nu reîncerca automat în interiorul lock-ului.

> **Spring Boot 4 vs. tutoriale Boot 3**
> - Spring Framework 7: `RestClient` și interfețele `@HttpExchange` sunt calea recomandată. `RestTemplate` e în mentenanță, iar `WebClient` nu e necesar într-un serviciu MVC.
> - Hibernate 7 / JPA 3.2: `jakarta.persistence.*`. `@Lock` și `LockModeType` sunt la fel.
> - În teste: `@MockitoBean` (nu `@MockBean`). Testcontainers 2 folosește `org.testcontainers.mysql.MySQLContainer` (artefactul `testcontainers-mysql`), iar `@ServiceConnection` configurează automat DataSource-ul.
> - Jackson 3: `tools.jackson.databind.json.JsonMapper`. Adnotările `@JsonProperty` rămân în `com.fasterxml.jackson.annotation`.

## 8. Dependențe

| Aștepți de la | Ce | Cum te deblochezi |
|---|---|---|
| K | `GET /internal/auctions/{id}`, `bid-placed` | `StubAuctionClient` (licitație activă, preț fix) |
| D | rezervările | `StubWalletClient` (acceptă tot sau respinge peste un prag) |
| R | `POST /internal/events` | `StubNotificationClient` (doar loghează) |
| D | gateway cu JWT | trimiți manual `X-User-Id` / `X-User-Name` |

| Așteaptă de la tine | Ce | Când |
|---|---|---|
| A | `POST /api/bids`, istoricul ofertelor, evenimentul `BID_PLACED` | S2–S3 |
| toți | contractele v1 înghețate, diagrama de clase | S1 |

## 9. Documentație

| Ce | Fișier | Termen |
|---|---|---|
| Diagrama de clase (ansamblu + bidding) | `docs/uml/class-diagram.puml`, `class-bidding-service.puml` | S1 (Ședințele 4–5) |
| Diagrama de componente, secvența de plasare a ofertei | `docs/uml/component.puml`, `sequence-place-bid.puml` | S2 |
| Raport cap. 4 (arhitectura) și cap. 6 (diagrama de clase) | `docs/raport-tehnic/src/04-…`, `06-…` | 24.11 |
| ADR-001, ADR-003 | `docs/decisions/` | S2 |
| `architecture.md`, `api-contracts.md` | la fiecare schimbare | continuu |

## 10. Git zilnic

```bash
git checkout m/bidding
git fetch origin && git merge origin/develop
# ... lucrezi ...
git add bidding-service/ docs/
git commit -m "feat(bidding): lock auction state before reserving funds"
git push origin m/bidding
gh pr create --base develop --head m/bidding --title "feat(bidding): place bid flow" --body "Closes #<nr>"
```

**Schimbare de contract:** în același PR modifici codul și `docs/api-contracts.md`, apoi treci versiunea în „Istoricul versiunilor”.

**Conflicte de merge:** [CONTRIBUTING §5](../../CONTRIBUTING.md#5-conflicte-de-merge).

## 11. Definition of Done

- [ ] `./mvnw -B verify` e verde, inclusiv `MySqlSchemaTests` când Docker merge;
- [ ] criteriile „Gata când…” sunt îndeplinite;
- [ ] fluxul de plasare a ofertei are teste pentru fiecare ramură de eroare și de compensare;
- [ ] contractele și colecția Postman sunt actualizate;
- [ ] PR-ul e aprobat de D, iar CI-ul e verde;
- [ ] scenariul cu două browsere merge în stack-ul complet.

## 12. Resurse și ajutor

- **Spring Data JPA, locking:** <https://docs.spring.io/spring-data/jpa/reference/jpa/locking.html>
- **Evenimente tranzacționale:** <https://docs.spring.io/spring-framework/reference/data-access/transaction/event.html>
- **RestClient:** <https://docs.spring.io/spring-framework/reference/integration/rest-clients.html>
- **Testcontainers + Spring Boot:** <https://docs.spring.io/spring-boot/reference/testing/testcontainers.html>
- **MySQL InnoDB locking:** <https://dev.mysql.com/doc/refman/8.4/en/innodb-locking.html>
- **Pe cine întrebi:**
  - portofel și JWT: **D**;
  - licitații și baza de date: **K**;
  - WebSocket, Docker și CI: **R**;
  - ce are nevoie UI-ul: **A**.
- **Dacă folosești un asistent AI:** pune-l să citească întâi `CLAUDE.md`, ghidul acesta și `docs/api-contracts.md`.
