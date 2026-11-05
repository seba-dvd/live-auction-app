# Ghidul lui R — DevOps Engineer · notification-service + infrastructură

## 1. Pe scurt

- **Deții:**
  - `notification-service` (STOMP peste WebSocket, `/internal/events`);
  - `docker-compose*.yml`, Dockerfile-urile, `db/`, `.github/` (CI/CD);
  - mediul de cloud;
  - colecția Postman și `tools/ws-test.html`.
- **Ramura ta:** `r/devops`. PR-urile tale le revizuiește **D**.
- **Rolul de curs:** DevOps Engineer. Ești **primul ajutor** pentru problemele de Docker ale colegilor.
- **Primele 3 acțiuni săptămâna asta:**
  1. ajută fiecare coleg să ruleze `docker compose up -d --build`;
  2. verifică faptul că CI-ul e verde pe toate ramurile;
  3. citește `docker-compose.yml` și `.github/workflows/ci.yml`.
- **Atenție:** pe calculatorul lui D, Docker Desktop nu pornea din cauza unor fișiere rămase de la o sesiune veche. Soluția este în [README §8](README.md#8-depanare). Verifică devreme dacă și alți colegi au aceeași problemă.

## 2. Rolul tău

| Responsabilitate | Frecvență |
|---|---|
| Ajuți colegii cu Docker Desktop, WSL2, porturi, memorie | la cerere, în aceeași zi |
| Revizuiești orice PR care atinge Dockerfile-urile, Compose sau CI (CODEOWNERS te cere automat) | la cerere |
| Ții CI-ul verde: investighezi eșecurile care nu țin de codul cuiva | continuu |
| Gestionezi variabilele de mediu și secretele (`.env.example`, GitHub Secrets, `.env` pe VM) | la schimbări |
| Ții structura colecției Postman; fiecare proprietar își adaugă aserțiunile | S2–S3 |
| Operezi mediul de cloud și livrarea automată | S3–S4 |

## 3. Ce deții

| Al tău | Doar prin PR, cu proprietarul ca reviewer |
|---|---|
| `notification-service/**` | `docs/api-contracts.md` (M): de exemplu §9, evenimentele |
| `docker-compose.yml`, `docker-compose.override.yml`, `docker-compose.prod.yml`, `*/Dockerfile`, `*/.dockerignore`, `db/**` | codul celorlalte servicii |
| `.github/workflows/**`, `postman/**`, `tools/ws-test.html` | `frontend/` (A); nginx-ul îl revizuiești împreună cu A |

## 4. Setup (o singură dată)

1. **Instalează:**
   - Git;
   - Docker Desktop cu WSL2 (<https://docs.docker.com/desktop/setup/install/windows-install/>);
   - JDK 21 Temurin;
   - IntelliJ IDEA;
   - Postman și Newman (`npm install -g newman`; Newman are nevoie de Node 24 LTS);
   - GitHub CLI (<https://cli.github.com/>).
2. **Acceptă invitația** la repository.
3. **Clonează și pornește stack-ul:**
   ```bash
   git clone https://github.com/seba-dvd/live-auction-app.git
   cd live-auction-app
   git checkout r/devops
   cp .env.example .env
   docker compose up -d --build --wait     # așteaptă ca toate containerele să fie „healthy”
   docker compose ps
   ```
4. **Verifică:** `curl -s localhost:8080/actuator/health` (și pe porturile 8081–8084).

## 5. Cum rulezi și testezi partea ta

**notification-service din IntelliJ:**
```bash
docker compose stop notification-service
# în .env decomentează DOCKER_NOTIFICATION_SERVICE_URL=... și DOCKER_NOTIFICATION_SERVICE_WS_URL=...
docker compose up -d
```

**Testare manuală a WebSocket-ului:**
1. Servește pagina de test:
   ```bash
   python -m http.server 5500 --directory tools      # sau: npx --yes http-server tools -p 5500
   ```
2. Deschide <http://localhost:5500/ws-test.html>. Fișierul deschis direct (`file://`) are originea `null`, care e respinsă.
3. Conectează-te la `ws://localhost:8080/ws` și abonează-te la `/topic/auctions/1`.
4. Trimite un eveniment din Postman: „internal API (direct ports)” → „[notification] Publish event”.

**Colecția Postman în linie de comandă:**
```bash
newman run postman/live-auction.postman_collection.json -e postman/local.postman_environment.json
```

**Teste:** `./mvnw -B verify` în `notification-service`.

**Infrastructură:**
- **Validarea fișierelor Compose:** `docker compose config --quiet`.
- **Imaginea unui serviciu:** `docker compose build <serviciu>`.
- **Varianta de producție, local:** `docker compose -f docker-compose.yml -f docker-compose.prod.yml config`.

## 6. Plan pe sprinturi

### S0 · Setup (28.10–08.11)

- [ ] **R-S0-01 · Stack-ul rulează pe laptopul fiecăruia**
  - **Ce:** sesiune de 30 de minute cu fiecare coleg care are probleme: WSL2, memorie (`.wslconfig`), porturi (MySQL local pe 3306 → `MYSQL_HOST_PORT`), CRLF.
  - **Gata când:** toți 5 au `docker compose ps` cu toate containerele „healthy”.
  - **Depinde de:** D-S0-01.
  - **Etichete:** `area:devops` `type:infra` `priority:must`
- [ ] **R-S0-02 · CI verde pe toate ramurile**
  - **Ce:** verifici primul run pe `main`, `develop` și pe ramurile personale și corectezi problemele de workflow.
  - **Gata când:** ultimul run pe fiecare ramură e verde.
  - **Depinde de:** —
  - **Etichete:** `area:devops` `type:infra` `priority:must`
- [ ] **R-S0-03 · Verifică stack-ul complet în Docker**
  - **Ce:** rulezi `docker compose up -d --build --wait`, verifici healthcheck-urile 8080–8084 și rulezi `MySqlSchemaTests` (bidding) cu Docker pornit.
  - **Gata când:** toate containerele sunt „healthy”, iar rezultatul e notat în issue.
  - **Depinde de:** —
  - **Etichete:** `area:devops` `type:infra` `priority:must`

### S1 · Design & fundații (09.11–22.11)

- [ ] **R-S1-01 · POST /internal/events cu X-Internal-Key**
  - **Ce:**
    - controller cu validarea anvelopei (`type` în enum, `auctionId` obligatoriu, `targetUserId` obligatoriu la OUTBID / WON / SOLD);
    - filtru pentru `X-Internal-Key`;
    - răspuns 202.
  - **Gata când:** cererea din Postman dă 202; fără cheie dă 401; un corp invalid dă 400 `VALIDATION_FAILED`.
  - **Depinde de:** —
  - **Etichete:** `area:notification` `type:feature` `priority:must`
- [ ] **R-S1-02 · Rutarea evenimentelor: topic sau coadă privată**
  - **Ce:** `EventRouter` cu `SimpMessagingTemplate`:
    - evenimentele publice merg la `convertAndSend("/topic/auctions/" + id, envelope)`;
    - cele private la `convertAndSendToUser(userId, "/queue/notifications", envelope)`;
    - `serverTime` se suprascrie cu ceasul serviciului.
  - **Gata când:** `tools/ws-test.html` primește evenimentul pe topic; un test unitar verifică destinațiile.
  - **Depinde de:** R-S1-01.
  - **Etichete:** `area:notification` `type:feature` `priority:must`
- [ ] **R-S1-03 · `tools/ws-test.html` prin gateway**
  - **Ce:** conexiunea `ws://localhost:8080/ws` trece prin gateway până la notification-service, inclusiv cu originile `http://localhost:5173` și `3000`.
  - **Gata când:** pagina se conectează prin gateway și primește evenimente.
  - **Depinde de:** R-S1-02.
  - **Etichete:** `area:notification` `type:feature` `priority:must`
- [ ] **R-S1-04 · Healthcheck-uri și memorie în Compose**
  - **Ce:** reglezi `start_period`, `retries` și `mem_limit` după ce măsori consumul real (`docker stats`).
  - **Gata când:** `docker compose up --wait` termină sub 3 minute pe un laptop cu 16 GB.
  - **Depinde de:** —
  - **Etichete:** `area:devops` `type:infra` `priority:should`

### S2 · Fluxuri de bază (23.11–06.12)

- [ ] **R-S2-01 · JWT pe STOMP CONNECT și cozile private**
  - **Ce:** `ChannelInterceptor` (§7.3): numele principalului este userId. Conexiunile anonime pot face SUBSCRIBE doar la `/topic/auctions/**`; refuzi abonarea la `/user/**` fără principal.
  - **Gata când:**
    - cu JWT valid, `/user/queue/notifications` primește evenimentul privat;
    - fără JWT, abonarea la coada privată e refuzată;
    - un JWT invalid refuză conexiunea.
  - **Depinde de:** R-S1-02, D-S1-03.
  - **Etichete:** `area:notification` `type:feature` `priority:must`
- [ ] **R-S2-02 · Colecția Postman finalizată**
  - **Ce:** mediile `local` și `cloud`, scriptul de login, exemple de răspuns salvate, ordinea folderelor pentru un run complet. Proprietarii își adaugă aserțiunile în S3.
  - **Gata când:** `newman run` trece cap-coadă pe stack-ul local, cel puțin pentru status-uri.
  - **Depinde de:** —
  - **Etichete:** `area:devops` `type:feature` `priority:must`
- [ ] **R-S2-03 · ADR-005: alegerea platformei cloud**
  - **Ce:** compari 2–3 opțiuni (de exemplu Azure for Students, oferte din GitHub Student Developer Pack, un VM cu nivel gratuit) după cost, resurse (2 vCPU și 4 GB RAM sau mai mult), acces SSH și IP public.
  - **Gata când:** ADR-005 are statusul „Acceptat”, iar contul e creat.
  - **Depinde de:** —
  - **Etichete:** `area:devops` `type:docs` `priority:must`
- [ ] **R-S2-04 · Raport Tehnic: capitolul 8 și diagrama de deployment**
  - **Ce:** revizuiești `08-infrastructura.md` și `docs/uml/deployment.puml` după alegerea platformei cloud.
  - **Gata când:** capitolul e pe `develop` până pe 24.11.
  - **Depinde de:** R-S2-03.
  - **Etichete:** `area:docs` `type:docs` `priority:must`

### S3 · Timp real & integrare (07.12–20.12)

- [ ] **R-S3-01 · Imaginile Docker în GHCR la push pe main**
  - **Ce:** un workflow care construiește cele 6 imagini și le publică ca `ghcr.io/<owner>/live-auction-<serviciu>:<sha>` și `:latest`, cu `permissions: packages: write`.
  - **Gata când:** după un push pe `main`, imaginile apar în pagina Packages a repository-ului.
  - **Depinde de:** —
  - **Etichete:** `area:devops` `type:infra` `priority:must`
- [ ] **R-S3-02 · Newman în CI, pe stack-ul Compose**
  - **Ce:** un job care rulează `docker compose up -d --build --wait`, apoi `newman run` cu mediul local, apoi `docker compose down`. Rulează pe PR-urile spre `develop` și `main`.
  - **Gata când:** job-ul e verde și eșuează la orice aserțiune Postman picată.
  - **Depinde de:** R-S2-02.
  - **Etichete:** `area:devops` `type:infra` `priority:must`
- [ ] **R-S3-03 · Required status checks**
  - **Ce:** în protecția ramurilor `develop` și `main`, verificările CI devin obligatorii, prin `gh api` sau din setări (cu D).
  - **Gata când:** un PR cu CI roșu nu mai poate fi integrat.
  - **Depinde de:** R-S3-02.
  - **Etichete:** `area:devops` `type:infra` `priority:should`
- [ ] **R-S3-04 · Prima implementare manuală pe VM**
  - **Ce:** VM-ul cu Docker; completezi `docker-compose.prod.yml` (imagini din GHCR, `ports: !reset []` pe gateway, doar front-end-ul publicat) și pui pe VM un `.env` cu secrete noi.
  - **Gata când:** aplicația răspunde la IP-ul public, iar scenariul de demo trece în cloud.
  - **Depinde de:** R-S3-01, R-S2-03.
  - **Etichete:** `area:devops` `type:infra` `priority:must`
- [ ] **R-S3-05 · Folderul Postman „Demo setup”**
  - **Ce:** cereri care creează conturile de demo, alimentează portofelele și creează 2–3 licitații cu sfârșit apropiat.
  - **Gata când:** un singur `newman run --folder "Demo setup"` pregătește datele pentru demo.
  - **Depinde de:** R-S2-02.
  - **Etichete:** `area:devops` `type:feature` `priority:should`

### S4 · Cloud & final (04.01–17.01)

- [ ] **R-S4-01 · CD la push pe main**
  - **Ce:** după publicarea imaginilor, un job face SSH pe VM (cheia în GitHub Secrets) și rulează `docker compose -f docker-compose.yml -f docker-compose.prod.yml pull && … up -d`.
  - **Gata când:** un commit pe `main` ajunge în cloud fără pași manuali.
  - **Depinde de:** R-S3-04.
  - **Etichete:** `area:devops` `type:infra` `priority:must`
- [ ] **R-S4-02 · Porturile 80/443/22 și HTTPS**
  - **Ce:** firewall-ul VM-ului lasă deschise doar aceste porturi. HTTPS se configurează cu Let's Encrypt (nginx sau Caddy), dacă există un domeniu.
  - **Gata când:** porturile 8080–8084 și 3306 nu sunt accesibile din exterior (verificat cu `nmap` sau din browser).
  - **Depinde de:** R-S4-01.
  - **Etichete:** `area:devops` `type:infra` `priority:should`
- [ ] **R-S4-03 · Test de verificare (smoke test) după fiecare livrare**
  - **Ce:** pasul final din CD: `curl` pe `/actuator/health` și pe pagina principală, cu eșec vizibil dacă nu răspund.
  - **Gata când:** o livrare stricată apare ca job roșu.
  - **Depinde de:** R-S4-01.
  - **Etichete:** `area:devops` `type:infra` `priority:should`
- [ ] **R-S4-04 · Mediul final de demo**
  - **Ce:** datele de demo pregătite, conturile notate, un backup al bazei de date înainte de prezentare.
  - **Gata când:** repetiția de demo (A-S4-03) merge în cloud.
  - **Depinde de:** R-S3-05.
  - **Etichete:** `area:devops` `type:infra` `priority:must`

## 7. Specificație tehnică

### 7.1 Ce expui

| Endpoint | Auth | Detalii |
|---|---|---|
| `POST /internal/events` | `X-Internal-Key` | [contracte §8.4](../api-contracts.md#84-notification-service-responsabil-r) |
| STOMP `/ws`: `/topic/auctions/{id}`, `/user/queue/notifications` | JWT opțional la CONNECT | [contracte §9](../api-contracts.md#9-websocket--stomp-și-evenimente) |

**Cine îți trimite evenimente:**
- bidding-service: `BID_PLACED`, `OUTBID`;
- auction-service: `AUCTION_STARTED`, `AUCTION_ENDED`, `AUCTION_WON`, `AUCTION_SOLD`.

Tu nu apelezi alte servicii.

**Clase recomandate:**
- `controller`: `InternalEventController`;
- `dto`: `EventEnvelope` (record), `EventType` (enum);
- `service`: `EventRouter`;
- `config`: `WebSocketConfig` (există), `JwtChannelInterceptor`, `InternalKeyFilter`.

### 7.2 Infrastructura pe scurt

| Fișier | Rol |
|---|---|
| `docker-compose.yml` | MySQL 8.4 + 5 servicii + front-end; healthcheck-uri; `mem_limit` 512m; rețeaua `auction-net`; volumele `mysql-data` și `auction-uploads`; publică doar 8080 și 3000 |
| `docker-compose.override.yml` | dezvoltare: publică 3306 (`MYSQL_HOST_PORT`) și 8081–8084 |
| `docker-compose.prod.yml` | placeholder: imagini GHCR, nimic publicat în afară de front-end (S3) |
| `db/init/01-init.sh` | creează schemele și un utilizator per serviciu (doar la primul start, cu volumul gol) |
| `.github/workflows/ci.yml` | detectează componentele modificate; matrix Maven + build front-end |
| `*/Dockerfile` | multi-stage (Temurin 21 JDK → JRE), utilizator fără drepturi de root, cache BuildKit pentru Maven |
| `postman/` | colecția (API public + intern) și mediul `local` |

### 7.3 Codul care previne greșelile clasice

**Validarea JWT la CONNECT.** Folosește `MessageHeaderAccessor.getAccessor`; un `StompHeaderAccessor.wrap` ar modifica o copie, iar utilizatorul nu s-ar mai seta:

```java
@Override
public Message<?> preSend(Message<?> message, MessageChannel channel) {
    // getAccessor returns the mutable accessor of this message; StompHeaderAccessor.wrap(message) would be a copy
    StompHeaderAccessor accessor = MessageHeaderAccessor.getAccessor(message, StompHeaderAccessor.class);
    if (accessor != null && StompCommand.CONNECT.equals(accessor.getCommand())) {
        String header = accessor.getFirstNativeHeader("Authorization");
        if (header != null && header.startsWith("Bearer ")) {
            Jwt jwt = jwtDecoder.decode(header.substring(7));   // invalid token -> exception -> CONNECT refused
            Principal user = jwt::getSubject;                   // principal name = userId
            accessor.setUser(user);
        }
    }
    return message;
}
```

**Decodorul și înregistrarea interceptorului** în `WebSocketConfig`. Dependența `spring-security-oauth2-jose` este deja în `pom.xml`:

```java
// în constructorul interceptorului
SecretKey key = new SecretKeySpec(secret.getBytes(StandardCharsets.UTF_8), "HmacSHA256");
this.jwtDecoder = NimbusJwtDecoder.withSecretKey(key).macAlgorithm(MacAlgorithm.HS256).build();

// în WebSocketConfig
@Override
public void configureClientInboundChannel(ChannelRegistration registration) {
    registration.interceptors(jwtChannelInterceptor);
}
```

### 7.4 Decizii și capcane

- **Nu adăuga `spring-boot-starter-security`** în notification-service. Ar bloca toate endpoint-urile cu login implicit. JWT-ul se validează doar cu biblioteca JOSE, în interceptor.
- **`convertAndSendToUser(userId, …)`:** primul argument este numele principalului, adică userId ca text (`"7"`), nu username-ul.
- **Simple broker-ul este în memorie:** la repornirea serviciului, clienții se reconectează singuri (`reconnectDelay`), iar front-end-ul reîncarcă datele prin REST.
- **Originile WebSocket:** `WS_ALLOWED_ORIGIN_PATTERNS` trebuie să includă originea paginii (în cloud, domeniul public).
- **nginx:** pentru `/ws` sunt necesare `proxy_http_version 1.1`, `Upgrade` și `Connection "upgrade"`, plus `proxy_read_timeout` mare. Toate sunt deja în `frontend/nginx.conf`.
- **Compose:**
  - `depends_on: condition: service_healthy` așteaptă doar pornirea, nu și recuperarea după o cădere;
  - healthcheck-ul MySQL folosește TCP (`-h 127.0.0.1`), ca să nu fie „healthy” în timpul scripturilor de inițializare.
- **Secrete:**
  - niciodată în workflow-uri în clar, doar `${{ secrets.X }}`;
  - în producție, `.env` stă doar pe VM, cu valori diferite de `.env.example`.
- **CRLF:** scripturile `.sh` și `mvnw` trebuie să aibă LF (`.gitattributes` se ocupă) și drept de execuție în git (`git update-index --chmod=+x`).

> **Spring Boot 4 vs. tutoriale Boot 3**
> - Starterul WebSocket este `spring-boot-starter-websocket`, iar starterul web este `spring-boot-starter-webmvc` (nu `spring-boot-starter-web`).
> - Jackson 3 serializează `Instant` ca text ISO-8601 în mod implicit; nu mai trebuie `WRITE_DATES_AS_TIMESTAMPS=false`.
> - Actuator: endpoint-urile expuse se setează cu `management.endpoints.web.exposure.include` (aici `health,info`). Healthcheck-urile Compose folosesc `/actuator/health`.
> - În teste: `@MockitoBean` în loc de `@MockBean`.

## 8. Dependențe

| Aștepți de la | Ce | Cum te deblochezi |
|---|---|---|
| D | JWT-ul emis de user-service (secretul comun) | generezi un token de test cu același secret (jwt.io, HS256) |
| M, K | evenimentele reale | le trimiți manual din Postman |
| D | acces de administrator pentru secrete și protecție | îi ceri lui D să ruleze comenzile `gh api` |

| Așteaptă de la tine | Ce | Când |
|---|---|---|
| toți | stack-ul care rulează local, CI verde | S0 |
| M, K | `POST /internal/events` | S1 (ei au stub-uri până atunci) |
| A | WebSocket prin gateway, cozile private | S1–S2 |
| D | implementarea în cloud pentru prezentări | S3–S4 |

## 9. Documentație

| Ce | Fișier | Termen |
|---|---|---|
| Raport cap. 8 (infrastructura) | `docs/raport-tehnic/src/08-infrastructura.md` | 24.11 |
| Diagrama de deployment, diagrama de clase notification-service | `docs/uml/deployment.puml`, `class-notification-service.puml` | S2 / S1 |
| ADR-005 (cloud) | `docs/decisions/ADR-005-cloud-platform.md` | S2 |
| Depanare Docker (README-ul echipei) | `docs/team/README.md` §8 | continuu |

## 10. Git zilnic

```bash
git checkout r/devops
git fetch origin && git merge origin/develop
# ... lucrezi ...
git add notification-service/ docker-compose*.yml .github/ postman/
git commit -m "ci: run newman against docker compose"
git push origin r/devops
gh pr create --base develop --head r/devops --title "ci: newman in CI" --body "Closes #<nr>"
```

**Conflicte de merge:** [CONTRIBUTING §5](../../CONTRIBUTING.md#5-conflicte-de-merge). Pentru fișierele YAML, verifică după rezolvare cu `docker compose config --quiet`.

## 11. Definition of Done

- [ ] `./mvnw -B verify` e verde (notification-service); `docker compose config --quiet` trece;
- [ ] criteriile „Gata când…” sunt îndeplinite;
- [ ] colecția Postman rulează în Newman;
- [ ] nu există secrete în fișiere sau în loguri de CI;
- [ ] PR-ul are CI-ul verde;
- [ ] `docker compose up -d --build --wait` trece pe un calculator „curat”.

## 12. Resurse și ajutor

- **Spring WebSocket / STOMP:** <https://docs.spring.io/spring-framework/reference/web/websocket/stomp.html>
- **Autentificarea STOMP cu token:** <https://docs.spring.io/spring-framework/reference/web/websocket/stomp/authentication-token-based.html>
- **Docker Compose:** <https://docs.docker.com/compose/>
- **Healthcheck-uri:** <https://docs.docker.com/reference/compose-file/services/#healthcheck>
- **GitHub Actions:** <https://docs.github.com/en/actions>
- **Publicarea imaginilor în GHCR:** <https://docs.github.com/en/packages/managing-github-packages-using-github-actions-workflows/publishing-and-installing-a-package-with-github-actions>
- **Newman:** <https://learning.postman.com/docs/collections/using-newman-cli/command-line-integration-with-newman/>
- **Pe cine întrebi:**
  - JWT, gateway și secrete: **D**;
  - contractele evenimentelor: **M**;
  - închiderea licitațiilor: **K**;
  - front-end și nginx: **A**.
- **Dacă folosești un asistent AI:** pune-l să citească întâi `CLAUDE.md`, ghidul acesta și `docs/api-contracts.md`.
