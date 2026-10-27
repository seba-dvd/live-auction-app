# ADR-003: Clienți REST (`RestClient` / `@HttpExchange`) și profilul `stub`

- **Status:** Propus
- **Data:** 27.10.2026
- **Proprietar:** M (finalizează în S1, odată cu primii clienți din bidding-service)
- **Aprobat de:** M

## Context

**Cine pe cine apelează:**
- bidding-service apelează auction-service, user-service și notification-service;
- auction-service apelează user-service și notification-service.

Cei 5 membri lucrează în paralel, deci un serviciu trebuie să poată fi dezvoltat și testat **înainte** ca dependențele lui să fie gata. Cursul cere comunicare REST între microservicii.

## Opțiuni analizate

1. **`RestClient` din Spring Framework 7**, eventual în spatele unor interfețe `@HttpExchange` (HTTP service clients).
   - (+) Inclus în `spring-boot-starter-webmvc`, fără dependențe noi.
   - (+) API sincron, ușor de înțeles.
   - (+) Timeouts configurabile prin `ClientHttpRequestFactory`.
2. **OpenFeign** (Spring Cloud).
   - (+) Interfețe declarative.
   - (−) Încă o dependență Spring Cloud de aliniat cu Boot 4; `@HttpExchange` oferă deja același stil.
3. **`WebClient`** (reactiv).
   - (−) Aduce modelul reactiv în servicii care sunt MVC/blocante. Inutil aici.

## Decizie (propusă)

**Opțiunea 1:**

- **Interfețe Java:** fiecare dependență externă este o interfață, de exemplu `AuctionClient`, `WalletClient`, `NotificationClient`.
- **Două implementări per interfață:**
  - HTTP, cu `RestClient` sau `@HttpExchange`, activă implicit;
  - `@Profile("stub")`, în memorie, cu date fixe sau configurabile, folosită când dependența nu e gata.
- **Configurare:** URL-urile de bază vin din `USER_SERVICE_URL`, `AUCTION_SERVICE_URL`, `BIDDING_SERVICE_URL`, `NOTIFICATION_SERVICE_URL`, cu valorile implicite `http://localhost:808x`. Timeouts: connect 2 s, read 5 s.
- **Header:** toate apelurile `/internal/**` trimit `X-Internal-Key`.

## Consecințe

- **Rulare cu stub-uri:** `./mvnw spring-boot:run -Dspring-boot.run.profiles=stub` pornește serviciul fără dependențe.
- **Teste unitare:** folosesc mock-uri ale interfețelor (`@MockitoBean` sau Mockito simplu).
- **Erori:** un 409 de la serviciul apelat se traduce în aceeași eroare de domeniu (de ex. `INSUFFICIENT_FUNDS`). Un timeout sau un 5xx devine 503 `SERVICE_UNAVAILABLE`.
- **Fără circuit breaker în v1.** Resilience4j rămâne o evoluție posibilă.
