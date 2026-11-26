# Ghidul lui D — Project Manager · user-service + api-gateway

## 1. Pe scurt

- **Deții:** `user-service` (autentificare, JWT, portofel, rezervări, decontări) și `api-gateway` (validare JWT, propagarea identității, rutare, CORS).
- **Ramura ta:** `d/user-gateway`. PR-urile tale spre `develop` le revizuiește **M**.
- **Rolul de curs:** Project Manager, adică termene, riscuri, release-uri, Raportul Tehnic și prezentările.
- **Primele 3 acțiuni săptămâna asta:**
  1. invită colegii (`scripts/github/add-members.sh`);
  2. verifică că fiecare rulează stack-ul local;
  3. pregătește prezentarea temei și a rolurilor pentru Ședința 3 (02/09.11).
- **Termen important:** înregistrează tema în tabelul coordonatorului **până la 09.11.2026**.

## 2. Rolul tău

| Responsabilitate | Frecvență |
|---|---|
| Administrezi repository-ul: invitații, protecția ramurilor, setări, secrete GitHub | la nevoie |
| Faci PR-ul `develop → main` la final de sprint, apoi merge și tag `v0.<sprint>.0` | la 2 săptămâni |
| Check-in cu Scrum Master-ul (K): blocaje, riscuri, termene | săptămânal, 15 min |
| Actualizezi registrul riscurilor ([README](README.md#6-registrul-riscurilor)) | la fiecare sprint review |
| Urmărești termenele disciplinei (09.11, 30.11, prezentările) și le anunți cu o săptămână înainte | continuu |
| Coordonezi Raportul Tehnic: împarți capitolele, asamblezi documentul și îl predai (intern 27.11, predare 30.11) | S1–S2 |
| Pregătești prezentările de stadiu și finală, împreună cu toată echipa | S0, S3, S4 |
| Revizuiești PR-urile lui M și R | la cerere, în 24 h |

## 3. Ce deții

| Al tău (modifici liber pe ramura ta) | Doar prin PR, cu proprietarul ca reviewer |
|---|---|
| `user-service/**`, `api-gateway/**` | `docs/api-contracts.md` (M), `docker-compose*.yml` și `.github/` (R) |
| `docs/team/**`, `docs/project-charter/**`, `docs/raport-tehnic/**` (asamblarea) | capitolele altora din Raport (autorii lor) |
| fișierele din rădăcină (`README.md`, `CONTRIBUTING.md`, `CLAUDE.md`) | `docs/database/**` (K) |

**Nu atinge** `bidding-service/`, `auction-service/`, `notification-service/` și `frontend/`. Dacă ai nevoie de ceva acolo, deschide un issue pentru proprietar.

## 4. Setup (o singură dată)

1. **Instalează:**
   - Git (<https://git-scm.com/downloads>);
   - Docker Desktop cu WSL2 (<https://www.docker.com/products/docker-desktop/>);
   - JDK 21 Temurin (<https://adoptium.net/temurin/releases/?version=21>);
   - IntelliJ IDEA (licența de student: <https://www.jetbrains.com/community/education/>);
   - Postman (<https://www.postman.com/downloads/>);
   - GitHub CLI (<https://cli.github.com/>).
2. **Autentifică GitHub CLI:** `gh auth login`. Pentru board, cere și scope-ul `project`: `gh auth refresh -s project`.
3. **Clonează și configurează:**
   ```bash
   git clone https://github.com/seba-dvd/live-auction-app.git
   cd live-auction-app
   git checkout d/user-gateway
   cp .env.example .env
   docker compose up -d --build
   ```
4. **Verifică:** <http://localhost:8080/actuator/health> trebuie să arate `{"status":"UP"}`.
5. **Deschide în IntelliJ** folderele `user-service` și `api-gateway` (File → Open → `pom.xml` → Open as Project). Setează SDK-ul la 21.

## 5. Cum rulezi și testezi partea ta

**user-service din IntelliJ, restul în Docker:**
```bash
docker compose stop user-service
# în .env decomentează:  DOCKER_USER_SERVICE_URL=http://host.docker.internal:8081
docker compose up -d                  # gateway-ul și celelalte servicii te apelează pe calculatorul tău
```
Apoi rulează `UserServiceApplication` din IntelliJ. Se conectează la MySQL din Compose pe `localhost:3306`, cu valorile implicite din `application.yml`.

**Testează direct pe portul tău**, fără gateway, trimițând manual header-ele pe care le pune gateway-ul:
```bash
curl -s http://localhost:8081/api/users/me -H "X-User-Id: 1" -H "X-User-Name: ana.pop"
curl -s -X PUT http://localhost:8081/internal/wallet/reservations -H "X-Internal-Key: dev-only-internal-api-key" \
     -H "Content-Type: application/json" -d '{"userId":1,"auctionId":42,"amount":150}'
```

**Apoi prin gateway:** în Postman folosește folderul „user-service”, cu „Register” și apoi „Login”. Tokenul se salvează automat.

**Gateway-ul** îl rulezi tot din IntelliJ, după ce faci `docker compose stop api-gateway`. Rutele lui implicite sunt `localhost:808x`.

**Teste și imagine:**
- **Teste:** `./mvnw -B verify` în folderul serviciului (nu au nevoie de MySQL).
- **Reconstruiește doar containerul tău:** `docker compose up -d --build user-service` (sau `api-gateway`).

## 6. Plan pe sprinturi

### S0 · Setup (28.10–08.11)

- [ ] **D-S0-01 · Invită colegii și finalizează setările GitHub**
  - **Ce:**
    - rulezi `scripts/github/add-members.sh` cu username-urile colegilor;
    - după ce acceptă invitațiile, rulezi `scripts/github/assign-issues.sh`;
    - activezi liniile lor din `.github/CODEOWNERS` (prin PR).
  - **Gata când:** toți 5 au acces de scriere, issue-urile sunt atribuite, iar CODEOWNERS cere review-ul corect.
  - **Depinde de:** username-urile colegilor.
  - **Etichete:** `area:devops` `type:chore` `priority:must`
- [ ] **D-S0-02 · Verifică mediul de lucru al fiecărui membru**
  - **Ce:** fiecare rulează `docker compose up -d --build`, deschide `/actuator/health` și Postman „Gateway health”.
  - **Gata când:** toți au confirmat în chat „setup gata”; problemele rămase au issues atribuite lui R.
  - **Depinde de:** D-S0-01.
  - **Etichete:** `area:devops` `type:chore` `priority:must`
- [ ] **D-S0-03 · Prezintă tema și rolurile la Ședința 3**
  - **Ce:** slide-uri cu tema, arhitectura, rolurile și calendarul. Folosește [Carta proiectului](../project-charter/README.md) și diagrama de componente.
  - **Gata când:** prezentarea a avut loc (02/09.11), iar feedback-ul coordonatorului e notat într-un issue.
  - **Depinde de:** —
  - **Etichete:** `area:docs` `type:docs` `priority:must`
- [ ] **D-S0-04 · Înregistrează tema în tabelul coordonatorului**
  - **Ce:** treci echipa, tema și rolurile în tabelul partajat de coordonator.
  - **Gata când:** înregistrarea e făcută până la **09.11.2026**, iar captura e pusă în chat.
  - **Depinde de:** —
  - **Etichete:** `area:docs` `type:chore` `priority:must`

### S1 · Design & fundații (09.11–22.11)

- [ ] **D-S1-01 · Entități și repository-uri: users, wallets, wallet_transactions**
  - **Ce:** `User`, `Wallet`, `WalletTransaction` (+ enum-urile `Role`, `TransactionType`) mapate pe tabelele din `V1__init.sql`, plus repository-urile Spring Data.
  - **Gata când:** serviciul pornește cu `ddl-auto: validate` pe MySQL din Compose, iar `./mvnw verify` e verde.
  - **Depinde de:** —
  - **Etichete:** `area:user` `type:feature` `priority:must`
- [ ] **D-S1-02 · Înregistrare cont**
  - **Ce:** `POST /api/auth/register`, într-o singură tranzacție:
    - validare și hash BCrypt;
    - verificarea unicității username-ului și a emailului;
    - crearea portofelului cu 1000 de monede și a tranzacției `SIGNUP_BONUS`.
  - **Gata când:** răspunde 201 cu `UserDto` și `Location`, 409 `USERNAME_TAKEN` / `EMAIL_TAKEN` și 400 `VALIDATION_FAILED`; are teste unitare.
  - **Depinde de:** D-S1-01.
  - **Etichete:** `area:user` `type:feature` `priority:must`
- [ ] **D-S1-03 · Autentificare și emiterea JWT**
  - **Ce:** `POST /api/auth/login` acceptă username sau email. Emite un JWT HS256 (§7.3) cu `sub`, `username`, `roles` și `exp` de 60 de minute.
  - **Gata când:** răspunde 200 `{accessToken, tokenType, expiresIn, user}` și 401 `INVALID_CREDENTIALS` (același mesaj pentru ambele cazuri); tokenul se decodează pe <https://jwt.io> cu claims corecte.
  - **Depinde de:** D-S1-02.
  - **Etichete:** `area:user` `type:feature` `priority:must`
- [ ] **D-S1-04 · Profil și portofel: GET/PUT /api/users/me, GET /api/users/{id}, GET /api/wallet**
  - **Ce:** endpoint-urile citesc identitatea din `X-User-Id` și răspund conform [api-contracts §5](../api-contracts.md#5-user-service-api-public).
  - **Gata când:** cererile din Postman trec prin gateway, iar 404 `USER_NOT_FOUND` e tratat.
  - **Depinde de:** D-S1-01.
  - **Etichete:** `area:user` `type:feature` `priority:must`
- [ ] **D-S1-05 · Gateway: validarea JWT și rutele publice**
  - **Ce:**
    - resource server reactiv cu decodor HS256 (§7.3);
    - lista de rute publice din [api-contracts §2.3](../api-contracts.md#23-rute-publice-fără-jwt);
    - 401/403 ca ProblemDetail JSON.
  - **Gata când:**
    - `GET /api/wallet` fără token dă 401, cu token dă 200;
    - `GET /api/auctions` merge fără token;
    - `GET /api/auctions/mine` fără token dă 401.
  - **Depinde de:** D-S1-03.
  - **Etichete:** `area:gateway` `type:feature` `priority:must`
- [ ] **D-S1-06 · Gateway: ștergerea și propagarea header-elor; tokenul expirat pe rute publice**
  - **Ce:**
    - un `GlobalFilter` (sau `WebFilter`) șterge `X-User-Id`, `X-User-Name` și `X-Internal-Key` primite de la client;
    - adaugă `X-User-Id` / `X-User-Name` din JWT;
    - decide și documentează în ADR-002 ce se întâmplă cu un token expirat pe o rută publică.
  - **Gata când:**
    - un `X-User-Id` falsificat de client nu ajunge la servicii;
    - pe rutele publice, cu token expirat, navigarea merge;
    - ADR-002 are statusul „Acceptat”.
  - **Depinde de:** D-S1-05.
  - **Etichete:** `area:gateway` `type:feature` `priority:must`
- [ ] **D-S1-07 · Diagrama de clase pentru user-service**
  - **Ce:** actualizezi `docs/uml/class-user-service.puml` după implementarea reală și îi trimiți lui M ce s-a schimbat.
  - **Gata când:** diagrama e regenerată (`bash tools/diagrams/render.sh`) și e inclusă în diagrama de ansamblu.
  - **Depinde de:** D-S1-01.
  - **Etichete:** `area:docs` `type:uml` `priority:must`
- [ ] **D-S1-08 · Release v0.1.0**
  - **Ce:** PR `develop → main` la finalul S1, merge și tag `v0.1.0` cu notele de release.
  - **Gata când:** tag-ul există, iar `main` rulează cu `docker compose up`.
  - **Depinde de:** sprint review S1.
  - **Etichete:** `area:devops` `type:chore` `priority:must`

### S2 · Fluxuri de bază (23.11–06.12)

- [ ] **D-S2-01 · Rezervări interne: PUT și DELETE /internal/wallet/reservations**
  - **Ce:**
    - entitatea `WalletReservation`;
    - setarea idempotentă a rezervării: `available + rezervareaCurentă ≥ amount`, altfel 409;
    - eliberarea idempotentă;
    - lock `PESSIMISTIC_WRITE` pe portofel.
  - **Gata când:**
    - rezervarea de 150, apoi 200 pe aceeași licitație dă `reserved = 200` (nu 350);
    - DELETE de două ori dă 204 de fiecare dată;
    - există teste unitare.
  - **Depinde de:** D-S1-01.
  - **Etichete:** `area:user` `type:feature` `priority:must`
- [ ] **D-S2-02 · Decontări idempotente: POST /internal/wallet/settlements**
  - **Ce:** decontarea respectă [api-contracts §8.1](../api-contracts.md#81-user-service-responsabil-d):
    - plata câștigătorului (`PAYMENT`) și încasarea vânzătorului (`PAYOUT`);
    - eliberarea celorlalte rezervări ale licitației;
    - rândul `wallet_settlements`;
    - lock-uri în ordinea crescătoare a userId.
  - **Gata când:**
    - al doilea apel cu același `auctionId` dă `alreadySettled: true`, fără mișcări de bani;
    - licitația fără oferte nu mută bani;
    - există teste unitare.
  - **Depinde de:** D-S2-01.
  - **Etichete:** `area:user` `type:feature` `priority:must`
- [ ] **D-S2-03 · Filtrul X-Internal-Key**
  - **Ce:** un filtru pe `/internal/**` compară header-ul cu `app.internal-api-key`. Dacă diferă, răspunde 401 ProblemDetail `INTERNAL_KEY_INVALID`.
  - **Gata când:** fără header dă 401, cu header corect merge; există un test cu MockMvc.
  - **Depinde de:** D-S2-01.
  - **Etichete:** `area:user` `type:feature` `priority:must`
- [ ] **D-S2-04 · Istoric tranzacții (paginat) și alimentare demo**
  - **Ce:** `GET /api/wallet/transactions` (`PagedModel`, cele mai noi primele) și `POST /api/wallet/top-up` (1–10000, tranzacție `TOP_UP`).
  - **Gata când:** paginarea respectă forma `PagedModel`, iar 0 sau 10001 dă 400.
  - **Depinde de:** D-S1-04.
  - **Etichete:** `area:user` `type:feature` `priority:should`
- [ ] **D-S2-05 · Teste unitare pentru portofel**
  - **Ce:** acoperi cazurile:
    - fonduri insuficiente;
    - mărirea propriei oferte (rezervarea se înlocuiește);
    - eliberare idempotentă;
    - decontare idempotentă;
    - licitație fără oferte;
    - invariantul `0 ≤ reserved ≤ balance`.
  - **Gata când:** toate cazurile au teste verzi în CI.
  - **Depinde de:** D-S2-02.
  - **Etichete:** `area:user` `type:feature` `priority:must`
- [ ] **D-S2-06 · Raport Tehnic: capitolele 3 și 9, apoi asamblarea**
  - **Ce:**
    - revizuiești `docs/raport-tehnic/src/03-roluri.md` și `09-securitate.md`;
    - strângi capitolele colegilor până pe 27.11;
    - regenerezi documentul (`bash tools/docgen/build.sh raport`) și îl predai pe 30.11.
  - **Gata când:** documentul e predat la termen, iar PDF-ul e comis pe `main`.
  - **Depinde de:** capitolele colegilor.
  - **Etichete:** `area:docs` `type:docs` `priority:must`
- [ ] **D-S2-07 · Release v0.2.0**
  - **Ce:** PR `develop → main`, merge și tag `v0.2.0`.
  - **Gata când:** tag-ul există, iar fluxurile S2 merg pe `main`.
  - **Depinde de:** sprint review S2.
  - **Etichete:** `area:devops` `type:chore` `priority:must`

### S3 · Timp real & integrare (07.12–20.12)

- [ ] **D-S3-01 · Test de concurență pentru portofel**
  - **Ce:** rezervări paralele pentru același utilizator, la licitații diferite (de exemplu 20 de fire). Suma rezervărilor acceptate nu depășește niciodată soldul. Folosește Testcontainers MySQL.
  - **Gata când:** testul trece de 10 ori la rând, iar invariantul e verificat în baza de date.
  - **Depinde de:** D-S2-01.
  - **Etichete:** `area:user` `type:feature` `priority:should`
- [ ] **D-S3-02 · Postman: aserțiuni pentru auth, users și wallet**
  - **Ce:** teste în tab-ul „Tests” pentru fiecare cerere a ta: status, câmpuri, coduri de eroare.
  - **Gata când:** folderul rulează verde în Newman (CI-ul lui R).
  - **Depinde de:** R-S2-02.
  - **Etichete:** `area:user` `type:feature` `priority:must`
- [ ] **D-S3-03 · Verificarea CORS și WebSocket prin gateway (cu A și R)**
  - **Ce:** front-end-ul pe 5173 și 3000, conexiunea `/ws` prin gateway, coada privată cu JWT.
  - **Gata când:** pagina live merge din ambele origini, fără erori CORS în consolă.
  - **Depinde de:** R-S2-01, A-S3-01.
  - **Etichete:** `area:gateway` `type:feature` `priority:must`
- [ ] **D-S3-04 · Prezentarea stadiului proiectului**
  - **Ce:** slide-uri și demo scurt cu fluxurile S2–S3, pregătite cu toată echipa.
  - **Gata când:** prezentarea a avut loc la Ședințele 6–7.
  - **Depinde de:** —
  - **Etichete:** `area:docs` `type:docs` `priority:must`
- [ ] **D-S3-05 · Release v0.3.0**
  - **Ce:** PR `develop → main`, merge și tag `v0.3.0` (MVP-ul complet).
  - **Gata când:** scenariul de demo merge pe `main`.
  - **Depinde de:** sprint review S3.
  - **Etichete:** `area:devops` `type:chore` `priority:must`

### S4 · Cloud & final (04.01–17.01)

- [ ] **D-S4-01 · Revizuirea securității (OWASP Top 10)**
  - **Ce:** parcurgi lista OWASP Top 10 pentru aplicație și notezi constatările și corecturile în issues.
  - **Gata când:** fiecare punct are „ok” sau un issue rezolvat; capitolul 9 din Raport e actualizat.
  - **Depinde de:** —
  - **Etichete:** `area:gateway` `type:docs` `priority:should`
- [ ] **D-S4-02 · Secretele de producție (cu R)**
  - **Ce:** `JWT_SECRET`, `INTERNAL_API_KEY` și parolele MySQL noi, generate aleator, în `.env` pe VM și în GitHub Secrets.
  - **Gata când:** producția nu folosește nicio valoare din `.env.example`.
  - **Depinde de:** R-S3-04.
  - **Etichete:** `area:devops` `type:infra` `priority:must`
- [ ] **D-S4-03 · Prezentarea finală și demo-ul**
  - **Ce:** conduci prezentarea finală. Scenariul de demo îl pregătește A, cu repetiție completă în cloud.
  - **Gata când:** prezentarea a avut loc, iar release-ul `v1.0.0` e pe `main`.
  - **Depinde de:** A-S4-03.
  - **Etichete:** `area:docs` `type:docs` `priority:must`
- [ ] **D-S4-04 · (opțional) Swagger UI agregat în gateway**
  - **Ce:** `springdoc-openapi-starter-webflux-ui` în gateway, cu `urls` către `/v3/api-docs` ale serviciilor.
  - **Gata când:** <http://localhost:8080/swagger-ui.html> listează toate serviciile.
  - **Depinde de:** —
  - **Etichete:** `area:gateway` `type:feature` `priority:could`

## 7. Specificație tehnică

### 7.1 Endpoint-uri pe care le expui

| Serviciu | Endpoint | Auth | Detalii |
|---|---|---|---|
| user | `POST /api/auth/register`, `POST /api/auth/login` | public | [contracte §5.1–5.2](../api-contracts.md#5-user-service-api-public) |
| user | `GET/PUT /api/users/me`, `GET /api/users/{id}` | JWT | §5.3–5.5 |
| user | `GET /api/wallet`, `GET /api/wallet/transactions`, `POST /api/wallet/top-up` | JWT | §5.6–5.8 |
| user | `PUT/DELETE /internal/wallet/reservations`, `POST /internal/wallet/settlements` | `X-Internal-Key` | [§8.1](../api-contracts.md#81-user-service-responsabil-d) |
| gateway | rutele `/api/**` și `/ws/**` | JWT (cu excepția rutelor publice) | `api-gateway/src/main/resources/application.yml` |

**Cine te apelează:**
- bidding-service: rezervări (PUT/DELETE);
- auction-service: decontări.

**Tu nu apelezi** niciun alt serviciu.

### 7.2 Tabelele tale (`user_db`)

`users`, `wallets`, `wallet_reservations`, `wallet_transactions`, `wallet_settlements`, cu detaliile în [database/README §3](../database/README.md#3-user_db-user-service-d).

**Reguli:**
- **Invariant:** `0 ≤ reserved ≤ balance`; `available = balance − reserved` se calculează, nu se stochează.
- **Sume:** `amount` din tranzacții este mereu pozitiv, iar tipul dă sensul.
- **Clase recomandate:**
  - `entity`: `User`, `Wallet`, `WalletReservation`, `WalletTransaction`, `WalletSettlement`;
  - `service`: `AuthService`, `JwtService`, `UserService`, `WalletService`, `ReservationService`, `SettlementService`;
  - `controller`: `AuthController`, `UserController`, `WalletController`, `InternalWalletController`.

### 7.3 Codul care previne greșelile clasice

**Emiterea JWT HS256.** Fără `JwsHeader` cu HS256, Nimbus caută o cheie RSA și eșuează cu „Failed to select a JWK signing key”:

```java
@Bean
JwtEncoder jwtEncoder(@Value("${app.jwt.secret}") String secret) {
    SecretKey key = new SecretKeySpec(secret.getBytes(StandardCharsets.UTF_8), "HmacSHA256");
    return new NimbusJwtEncoder(new ImmutableSecret<>(key));
}

// în JwtService
JwtClaimsSet claims = JwtClaimsSet.builder()
        .issuer("live-auction-user-service")
        .subject(String.valueOf(userId))
        .issuedAt(now)
        .expiresAt(now.plus(Duration.ofMinutes(60)))
        .claim("username", username)
        .claim("roles", List.of(role))
        .build();
JwsHeader header = JwsHeader.with(MacAlgorithm.HS256).build();
String token = jwtEncoder.encode(JwtEncoderParameters.from(header, claims)).getTokenValue();
```

**Decodorul din gateway și ordinea rutelor.** `/api/auctions/mine` trebuie declarată **înaintea** lui `/api/auctions/**`, pentru că prima regulă potrivită câștigă:

```java
@Bean
ReactiveJwtDecoder reactiveJwtDecoder(@Value("${app.jwt.secret}") String secret) {
    SecretKey key = new SecretKeySpec(secret.getBytes(StandardCharsets.UTF_8), "HmacSHA256");
    return NimbusReactiveJwtDecoder.withSecretKey(key).macAlgorithm(MacAlgorithm.HS256).build();
}

// în SecurityConfig
.authorizeExchange(exchanges -> exchanges
        .pathMatchers(HttpMethod.OPTIONS).permitAll()
        .pathMatchers(HttpMethod.POST, "/api/auth/**").permitAll()
        .pathMatchers(HttpMethod.GET, "/api/auctions/mine").authenticated()   // before /api/auctions/**
        .pathMatchers(HttpMethod.GET, "/api/auctions/**", "/api/bids/auction/**").permitAll()
        .pathMatchers("/ws/**", "/actuator/health").permitAll()
        .anyExchange().authenticated())
.oauth2ResourceServer(oauth2 -> oauth2.jwt(Customizer.withDefaults()))
```

**Erorile în format ProblemDetail**, cu proprietatea `code`. `ApiException` este o excepție proprie, cu `status` și `code`:

```java
@ExceptionHandler(ApiException.class)
ProblemDetail handleApi(ApiException ex) {
    ProblemDetail problem = ProblemDetail.forStatusAndDetail(ex.getStatus(), ex.getMessage());
    problem.setProperty("code", ex.getCode());
    return problem;
}
```

### 7.4 Decizii și capcane

- **Token expirat pe o rută publică.** Cu `oauth2ResourceServer`, un token invalid este respins cu 401 **chiar și** pe rutele `permitAll`, pentru că filtrul de bearer token rulează înaintea autorizării. Ca navigarea să nu se blocheze:
  - fie ignori header-ul `Authorization` pe rutele publice, cu un `ServerAuthenticationConverter` propriu;
  - fie îl elimini înainte de filtrul de securitate.
  
  Documentează alegerea în ADR-002.
- **Ordinea filtrelor din gateway:** ștergerea header-elor se face pe **toate** cererile, iar adăugarea doar după autentificare. Un `GlobalFilter` cu ordine mică citește `ReactiveSecurityContextHolder`.
- **Lock-ul portofelului:** folosește `@Lock(PESSIMISTIC_WRITE)` pe `findByUserIdForUpdate`. În decontare, blochezi portofelele **sortate după userId**, altfel două decontări simultane pot face deadlock.
- **Tranzacții:** înregistrarea (user + portofel + bonus) și decontarea se fac fiecare într-o singură tranzacție (`@Transactional` pe metoda din service, nu pe controller).
- **Parole:** BCrypt are limita de 72 de octeți (validează `@Size(max = 72)`). Nu loga niciodată parole sau tokenuri.
- **Login:** caută după username **sau** email (`findByUsernameOrEmail`), cu același mesaj de eroare pentru ambele cazuri.

> **Spring Boot 4 vs. tutoriale Boot 3**
> - Spring Security 7 acceptă doar DSL-ul lambda: nu există `.and()` sau `authorizeRequests()`, ci doar `authorizeHttpRequests(...)` / `authorizeExchange(...)`.
> - Starterul se numește `spring-boot-starter-security-oauth2-resource-server` (nu `spring-boot-starter-oauth2-resource-server`).
> - Jackson 3: `ObjectMapper` / `JsonMapper` sunt în `tools.jackson.databind`; adnotările rămân `com.fasterxml.jackson.annotation`.
> - În teste, folosește `@MockitoBean` în loc de `@MockBean` (eliminat). `@WebMvcTest` este în `org.springframework.boot.webmvc.test.autoconfigure`.
> - Proprietățile gateway-ului sunt sub `spring.cloud.gateway.server.webflux.*`, iar starterul este `spring-cloud-starter-gateway-server-webflux`.

## 8. Dependențe

| Aștepți de la | Ce | Cum te deblochezi |
|---|---|---|
| R | Compose, CI, cheile din `.env` | există deja în schelet |
| M | confirmarea contractelor v1 | contractele din `api-contracts.md` sunt deja scrise; urmează-le |

| Așteaptă de la tine | Ce | Când |
|---|---|---|
| A | login și register prin gateway, JWT | S1 |
| M | rezervările (PUT/DELETE) | S2 (M are stub până atunci) |
| K | decontările | S2–S3 (K are stub până atunci) |
| toți | gateway-ul cu JWT și propagarea header-elor | S1 |

Până când gateway-ul validează JWT, ceilalți își testează serviciile trimițând manual `X-User-Id`.

## 9. Documentație

| Ce | Fișier | Termen |
|---|---|---|
| Raport cap. 3 (roluri) și cap. 9 (securitate) | `docs/raport-tehnic/src/03-roluri.md`, `09-securitate.md` | 20.11 / 24.11 |
| Raport cap. 10 + acronime, bibliografie, rezumat, abstract | `docs/raport-tehnic/src/10-…`, `00-…`, `90-…`, `95-…`, `96-…` | 26.11 |
| Asamblarea și predarea Raportului | `bash tools/docgen/build.sh raport` | intern 27.11, predare **30.11** |
| Diagrama de clase user-service, secvența de autentificare | `docs/uml/class-user-service.puml`, `sequence-login.puml` | S1 / S2 |
| ADR-002 (finalizare) | `docs/decisions/ADR-002-gateway-auth-internal-key.md` | 22.11 |
| Carta proiectului (actualizări) | `docs/project-charter/src/` | la schimbări |

## 10. Git zilnic

```bash
git checkout d/user-gateway
git fetch origin && git merge origin/develop          # la începutul zilei și după orice merge în develop
# ... lucrezi ...
git add user-service/ api-gateway/
git commit -m "feat(user): add wallet top-up endpoint"
git push origin d/user-gateway
gh pr create --base develop --head d/user-gateway --title "feat(user): wallet top-up" --body "Closes #<nr>"
```

**Release la final de sprint (doar tu):**
```bash
gh pr create --base main --head develop --title "release: v0.1.0" --body "Sprint S1"
# după merge:
git fetch origin && git tag -a v0.1.0 origin/main -m "Sprint S1" && git push origin v0.1.0
```

**Conflicte de merge:** urmează [CONTRIBUTING §5](../../CONTRIBUTING.md#5-conflicte-de-merge).

## 11. Definition of Done

- [ ] `./mvnw -B verify` e verde în `user-service` / `api-gateway`;
- [ ] criteriile „Gata când…” ale task-ului sunt îndeplinite;
- [ ] fiecare regulă de bani are test: rezervare, eliberare, decontare;
- [ ] contractele și colecția Postman sunt actualizate;
- [ ] nu există secrete în cod sau în loguri;
- [ ] PR-ul spre `develop` are CI-ul verde;
- [ ] funcționează în stack-ul complet (`docker compose up -d --build`).

## 12. Resurse și ajutor

- **Spring Security, resource server JWT:** <https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/jwt.html> și varianta reactivă: <https://docs.spring.io/spring-security/reference/reactive/oauth2/resource-server/jwt.html>
- **Spring Cloud Gateway (Server WebFlux):** <https://docs.spring.io/spring-cloud-gateway/reference/>
- **Spring Data JPA, locking:** <https://docs.spring.io/spring-data/jpa/reference/jpa/locking.html>
- **ProblemDetail (RFC 9457):** <https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-ann-rest-exceptions.html>
- **Pe cine întrebi:**
  - contracte și arhitectură: **M**;
  - baza de date: **K**;
  - Docker, CI și cloud: **R**;
  - front-end și ce așteaptă UI-ul: **A**.
- **Dacă folosești un asistent AI:** pune-l să citească întâi `CLAUDE.md`, ghidul acesta și `docs/api-contracts.md`.
