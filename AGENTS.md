# CLAUDE.md: guidance for AI coding assistants

**Live Auction App** is a 5-person university project (Universitatea Transilvania din Brașov, course "Proiect de Software pentru Telecomunicații", Agile/Scrum). Users run live auctions with fake coins. The repo is a monorepo:
- 5 Spring Boot **4.1** microservices (Java 21, Maven, no Lombok)
- a React + Vite + TypeScript front-end
- MySQL 8.4
- Docker Compose and GitHub Actions CI

Team docs are in **Romanian**. Code, identifiers, comments and commit messages are in **English**.

## Before you change anything

1. Read these first:
   - [`docs/api-contracts.md`](docs/api-contracts.md), the single source of truth for endpoints, payloads, headers and events
   - the owner's guide [`docs/team/<ID>.md`](docs/team/README.md)
   - [`docs/architecture.md`](docs/architecture.md)
2. Only touch the folders owned by the person you are helping (table below). Shared files change through a PR reviewed by their owner.
3. If an endpoint, payload, header, error `code` or event changes, update `docs/api-contracts.md` in the same PR. The Technical Lead (M) approves contract changes.
4. Respect the skeleton's intent. The members implement the business logic themselves because it is graded. Explain, review and suggest; do not dump whole features.

## Folder map and ownership

| Path | Owner | Content |
|---|---|---|
| `api-gateway/` | D | Spring Cloud Gateway Server WebFlux, JWT validation, header propagation, CORS |
| `user-service/` | D | Auth (register/login, JWT issuing), users, wallet, reservations, settlements |
| `auction-service/` | K | Auctions, photos, lifecycle scheduler, anti-sniping |
| `bidding-service/` | M | Place bid (locking, reservations, compensation), bid history |
| `notification-service/` | R | STOMP over WebSocket, `/internal/events` routing |
| `frontend/` | A | React SPA (router, auth context, live auction page) |
| `db/`, `docker-compose*.yml`, `.github/`, `postman/`, `tools/ws-test.html` | R | Infrastructure, CI/CD, Postman |
| `docs/api-contracts.md`, `docs/architecture.md`, `docs/decisions/`, `docs/uml/` | M | Contracts, architecture, ADRs, UML |
| `docs/database/` | K | Database design (each service owner keeps its own `V*__*.sql`) |
| `docs/product/` | A | Backlog, user stories |
| `docs/team/`, `docs/project-charter/`, `docs/raport-tehnic/`, root files | D | Team organization, charter, technical report assembly |

## Ports

gateway 8080 · user 8081 · auction 8082 · bidding 8083 · notification 8084 · MySQL 3306 · front-end 5173 (Vite dev) / 3000 (nginx in Docker).

## Conventions (non-negotiable)

**Code structure**
- **Packages:** `ro.unitbv.liveauction.<gateway|user|auction|bidding|notification>`, with layered sub-packages `config, controller, dto, entity, repository, service, client, exception`.
- **DTOs:** Java **records**. Never expose JPA entities from controllers. Bean Validation on every request body. Usernames match `^[a-zA-Z0-9_.-]{3,30}$`.

**Security**
- **Authentication:** user-service issues HS256 JWTs with `sub` = userId, `username`, `roles`, 60 min, secret `JWT_SECRET` ≥ 32 bytes.
- **Gateway duties:** the **api-gateway** validates JWTs. It strips client-sent `X-User-Id`, `X-User-Name` and `X-Internal-Key`, then adds `X-User-Id` / `X-User-Name` from the token. Downstream services trust these headers and **never parse JWTs**.
- **WebSocket exception:** notification-service validates the JWT sent in the STOMP `CONNECT` frame (`Authorization: Bearer …`) to enable private queues.
- **Public routes:** `POST /api/auth/**`, `GET /api/auctions/**` except `GET /api/auctions/mine`, `GET /api/bids/auction/**`, `/ws/**`, `/actuator/health`. Everything else under `/api/**` requires a JWT.
- **Internal API:** `/internal/**` with header `X-Internal-Key: ${INTERNAL_API_KEY}`. Called service-to-service on the Docker network and **never routed by the gateway**, which answers 404.

**Service-to-service calls**
- **Clients:** Spring `RestClient` or `@HttpExchange` interfaces. Base URLs come from `USER_SERVICE_URL`, `AUCTION_SERVICE_URL`, `BIDDING_SERVICE_URL` and `NOTIFICATION_SERVICE_URL`, defaulting to `http://localhost:808x`. Timeouts: connect 2 s, read 5 s.
- **Stubs:** every client is an interface with a `@Profile("stub")` in-memory implementation.

**API behaviour**
- **Errors:** RFC 9457 `ProblemDetail` with an extra property `code` (e.g. `BID_TOO_LOW`), produced by a `@RestControllerAdvice`.
- **Time:** `Instant` in UTC everywhere and ISO-8601 in JSON. Inject the `Clock` bean and never call `Instant.now()` directly. Hibernate runs with `jdbc.time_zone: UTC` and `type.preferred_instant_jdbc_type: TIMESTAMP`, so `Instant` maps to `DATETIME(6)` columns.
- **Money:** coins are `long` / `BIGINT`, no decimals. Wallet invariant: `0 ≤ reserved ≤ balance`, `available = balance − reserved`.
- **Pagination:** Spring Data `Pageable`. Responses use the `PagedModel` JSON shape: `content` + `page{size, number, totalElements, totalPages}`.

**Persistence and configuration**
- **Migrations:** Flyway in `src/main/resources/db/migration`, with `ddl-auto: validate`. `V1__init.sql` may be edited until **30.11.2026**; after that, only new `V<n>__<desc>.sql` files.
- **Configuration:** `application.yml` uses `${ENV_VAR:local-default}`. Every service runs from IntelliJ against the Compose MySQL with zero extra setup.
- **Tests:** the default context-load test uses the `test` profile (H2 in MySQL mode, Flyway off, `create-drop`), so `./mvnw verify` needs neither MySQL nor Docker. Real-MySQL tests use Testcontainers and need Docker.

### Spring Boot 4 vs. Boot 3 tutorials
Most online tutorials target Boot 3. The differences that matter here:
- **Jackson:** Jackson 3, packages `tools.jackson.*`. Annotations stay `com.fasterxml.jackson.annotation.*`.
- **Spring Framework / Security:** Spring Framework 7 and Spring Security 7. Security uses the lambda DSL only: no `.and()`, no `authorizeRequests`, no `AntPathRequestMatcher`.
- **Hibernate:** Hibernate 7 (JPA 3.2).
- **Modular starters:** e.g. `spring-boot-starter-webmvc`, `spring-boot-starter-flyway`, and test starters such as `spring-boot-starter-webmvc-test`. Test annotations moved packages, e.g. `org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest`.
- **Mocks:** `@MockitoBean` replaces the removed `@MockBean`.
- **Testcontainers:** Testcontainers 2 renames artifacts and packages (`org.testcontainers.mysql.MySQLContainer`).
- **Gateway:** the gateway uses `spring-cloud-starter-gateway-server-webflux` and properties under `spring.cloud.gateway.server.webflux.*`.

## Commands

```bash
# whole stack
cp .env.example .env
docker compose up -d --build            # http://localhost:3000, gateway http://localhost:8080
docker compose up -d --build <service>  # rebuild one service
docker compose logs -f <service>
docker compose down                     # keep data;  down -v resets MySQL

# one backend service (from its folder)
./mvnw -B verify                        # build + tests (no MySQL needed)
./mvnw spring-boot:run                  # needs MySQL from Compose (port 3306 published by the override file)
./mvnw spring-boot:run -Dspring-boot.run.profiles=stub   # use in-memory stub clients

# front-end
cd frontend && npm ci && npm run dev    # http://localhost:5173, proxies /api and /ws to :8080
npm run build

# diagrams and Word documents
bash tools/diagrams/render.sh           # PlantUML -> docs/diagrams/png
bash tools/docgen/build.sh              # Markdown -> UNITBV-style .docx (+ PDF via Word)
```

## Git workflow

- **Branches:** `main` (stable; only PRs from `develop`, merged by D at sprint end). `develop` (integration; only PRs from personal branches). Personal branches: `d/user-gateway`, `m/bidding`, `k/auction`, `a/frontend`, `r/devops`.
- **Commits and PRs:** Conventional Commits with scope (`feat(bidding): add bid history endpoint`). The PR body contains `Closes #<issue>`. Merge commits only.
- **After every merge into `develop`:** `git fetch origin && git merge origin/develop` on your branch.
- **Never** commit `.env`, secrets or tokens, and never force-push.
