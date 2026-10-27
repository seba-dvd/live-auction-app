# Contracte API — v1 — 27.10.2026

Acest document este **sursa unică de adevăr** pentru endpoint-uri, payload-uri, header-e, coduri de eroare și evenimentele în timp real. Codul se adaptează după acest document, nu invers.

**Reguli de modificare:**
- Orice schimbare de contract (câmp nou, câmp redenumit, cod de stare, cod de eroare, eveniment) se face **prin PR** care modifică acest fișier și codul în același timp.
- PR-ul trebuie **aprobat de M** (Technical Lead).
- Contractele v1 se „îngheață” la finalul S1 (22.11.2026). După aceea, schimbările incompatibile cer acordul tuturor celor afectați.
- Fiecare modificare se trece în [Istoricul versiunilor](#11-istoricul-versiunilor).

## Cuprins

1. [Convenții generale](#1-convenții-generale)
2. [Autentificare și header-e](#2-autentificare-și-header-e)
3. [Erori (ProblemDetail)](#3-erori-problemdetail)
4. [Paginare](#4-paginare)
5. [user-service: API public](#5-user-service-api-public)
6. [auction-service: API public](#6-auction-service-api-public)
7. [bidding-service: API public](#7-bidding-service-api-public)
8. [API intern (/internal/**)](#8-api-intern-internal)
9. [WebSocket / STOMP și evenimente](#9-websocket--stomp-și-evenimente)
10. [Catalogul codurilor de eroare](#10-catalogul-codurilor-de-eroare)
11. [Istoricul versiunilor](#11-istoricul-versiunilor)

## 1. Convenții generale

| Subiect | Regulă |
|---|---|
| URL public | `http://localhost:8080` (api-gateway). Front-end-ul folosește doar URL-uri relative (`/api/...`, `/ws`). |
| URL intern | `http://<serviciu>:<port>` în rețeaua Docker `auction-net` (ex. `http://user-service:8081`); din IntelliJ: `http://localhost:808x` |
| Format | JSON, UTF-8. Câmpuri `camelCase`. Câmpurile fără valoare se trimit `null`, nu se omit. |
| Timp | `Instant` în UTC, format ISO-8601: `"2026-11-20T18:30:00Z"` (fracțiunile de secundă sunt permise) |
| Bani | monede virtuale, numere întregi (`long`), fără zecimale |
| Identificatori | `long` (ex. `"id": 42`), `sub` din JWT este string (`"7"`) |
| Validare | Bean Validation pe toate corpurile cererilor; eroare 400 cu `code: "VALIDATION_FAILED"` |
| Username | `^[a-zA-Z0-9_.-]{3,30}$` |

## 2. Autentificare și header-e

### 2.1 JWT

- **Emitere:** user-service emite JWT la `POST /api/auth/login`, semnat cu **HS256**. Secretul este `JWT_SECRET`, de minimum 32 de octeți, partajat cu api-gateway și notification-service. Valabilitatea este de **60 de minute**.
- **Claims:**

```json
{
  "iss": "live-auction-user-service",
  "sub": "7",
  "username": "ana.pop",
  "roles": ["USER"],
  "iat": 1795183200,
  "exp": 1795186800
}
```

- **Trimitere:** clientul trimite tokenul în header-ul `Authorization: Bearer <token>`.

### 2.2 Ce face api-gateway

1. Validează JWT-ul (semnătură, `exp`) pentru tot traficul HTTP.
2. **Șterge** header-ele trimise de client: `X-User-Id`, `X-User-Name`, `X-Internal-Key`.
3. Dacă tokenul e valid, **adaugă** `X-User-Id: <sub>` și `X-User-Name: <username>`.
4. Rutele publice merg mai departe și fără token. Rutele protejate fără token valid primesc **401** (ProblemDetail, `code: "UNAUTHORIZED"`).

**Serviciile din spatele gateway-ului au încredere în `X-User-Id` / `X-User-Name` și nu parsează JWT-uri.** Excepția este notification-service, care validează JWT-ul din cadrul STOMP `CONNECT` (vezi §9).

### 2.3 Rute publice (fără JWT)

| Metodă | Cale |
|---|---|
| POST | `/api/auth/**` |
| GET | `/api/auctions/**`, **cu excepția** `GET /api/auctions/mine` |
| GET | `/api/bids/auction/**` |
| orice | `/ws/**` (autentificarea se face în cadrul STOMP `CONNECT`) |
| GET | `/actuator/health` |

Tot restul de sub `/api/**` cere un JWT valid. Gateway-ul nu are rută pentru `/internal/**`, așa că răspunde **404**.

**Token expirat pe o rută publică:** cererea trece ca anonimă (fără `X-User-*`), ca navigarea să nu se blocheze. D documentează decizia finală în ADR-002.

### 2.4 Header-e

| Header | Cine îl pune | Cine îl citește | Rol |
|---|---|---|---|
| `Authorization: Bearer <jwt>` | front-end | api-gateway; notification-service (STOMP CONNECT) | autentificare |
| `X-User-Id` | doar api-gateway | user, auction, bidding | identitatea apelantului (long) |
| `X-User-Name` | doar api-gateway | bidding (bidderUsername) | username-ul apelantului |
| `X-Internal-Key` | serviciul apelant | serviciul apelat | autorizează `/internal/**` (valoarea din `INTERNAL_API_KEY`) |

## 3. Erori (ProblemDetail)

Toate erorile respectă RFC 9457 (`application/problem+json`). Fiecare serviciu le produce dintr-un `@RestControllerAdvice` și adaugă proprietatea **`code`**:

```json
{
  "type": "about:blank",
  "title": "Bad Request",
  "status": 400,
  "detail": "Oferta trebuie să fie de cel puțin 170 de monede.",
  "instance": "/api/bids",
  "code": "BID_TOO_LOW"
}
```

Erorile de validare adaugă lista câmpurilor:

```json
{
  "type": "about:blank",
  "title": "Bad Request",
  "status": 400,
  "detail": "Cererea conține câmpuri invalide.",
  "instance": "/api/auth/register",
  "code": "VALIDATION_FAILED",
  "errors": [
    { "field": "username", "message": "trebuie să respecte ^[a-zA-Z0-9_.-]{3,30}$" }
  ]
}
```

Front-end-ul decide mesajul afișat după `code`, nu după `detail`. Lista completă este în §10.

## 4. Paginare

Parametrii de interogare sunt `page` (de la 0), `size` (implicit 20, maximum 50) și `sort` (ex. `sort=endTime,asc`). Răspunsul are forma `PagedModel` din Spring Data: controller-ul returnează `new PagedModel<>(page.map(...))`.

```json
{
  "content": [ { "...": "..." } ],
  "page": { "size": 12, "number": 0, "totalElements": 37, "totalPages": 4 }
}
```

## 5. user-service: API public

Responsabil: **D**. Prin gateway, pe rutele `/api/auth/**`, `/api/users/**`, `/api/wallet/**`.

### 5.1 `POST /api/auth/register` (public)

Creează contul și portofelul cu **1000 de monede** (tranzacție `SIGNUP_BONUS`).

**Cerere**
```json
{ "username": "ana.pop", "email": "ana@example.com", "password": "parola-sigura-123", "displayName": "Ana Pop" }
```

**Validare:**
- `username`: regex-ul de mai sus;
- `email`: email valid, maximum 254 de caractere;
- `password`: 8–72 de caractere (limita BCrypt);
- `displayName`: 1–60 de caractere.

**Răspuns 201** `UserDto`, cu header-ul `Location: /api/users/7`:
```json
{ "id": 7, "username": "ana.pop", "email": "ana@example.com", "displayName": "Ana Pop", "role": "USER", "createdAt": "2026-11-12T09:15:02.123456Z" }
```

**Erori:** 400 `VALIDATION_FAILED` · 409 `USERNAME_TAKEN` · 409 `EMAIL_TAKEN`

### 5.2 `POST /api/auth/login` (public)

**Cerere**
```json
{ "usernameOrEmail": "ana.pop", "password": "parola-sigura-123" }
```

**Răspuns 200**
```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI3Ii...",
  "tokenType": "Bearer",
  "expiresIn": 3600,
  "user": { "id": 7, "username": "ana.pop", "email": "ana@example.com", "displayName": "Ana Pop", "role": "USER", "createdAt": "2026-11-12T09:15:02.123456Z" }
}
```

**Erori:** 400 `VALIDATION_FAILED` · 401 `INVALID_CREDENTIALS` (același mesaj pentru utilizator inexistent și parolă greșită)

### 5.3 `GET /api/users/me` (JWT)

**Răspuns 200** `UserDto`. **Erori:** 401 `UNAUTHORIZED` · 404 `USER_NOT_FOUND`

### 5.4 `PUT /api/users/me` (JWT)

**Cerere**
```json
{ "displayName": "Ana P.", "email": "ana.p@example.com" }
```
**Răspuns 200** `UserDto`. **Erori:** 400 `VALIDATION_FAILED` · 409 `EMAIL_TAKEN`

### 5.5 `GET /api/users/{id}` (JWT)

Profil public. **Răspuns 200**
```json
{ "id": 7, "username": "ana.pop", "displayName": "Ana Pop" }
```
**Erori:** 404 `USER_NOT_FOUND`

### 5.6 `GET /api/wallet` (JWT)

**Răspuns 200** `WalletDto`. Invariant: `0 ≤ reserved ≤ balance`, `available = balance − reserved`.
```json
{ "balance": 1000, "reserved": 170, "available": 830 }
```

### 5.7 `GET /api/wallet/transactions?page=0&size=20` (JWT)

Cele mai noi primele. Tipuri: `SIGNUP_BONUS`, `TOP_UP`, `PAYMENT` (scade soldul), `PAYOUT` (crește soldul). `amount` este mereu pozitiv.

**Răspuns 200**
```json
{
  "content": [
    { "id": 31, "type": "PAYMENT", "amount": 170, "auctionId": 42, "createdAt": "2026-11-20T19:00:31.004Z" },
    { "id": 12, "type": "SIGNUP_BONUS", "amount": 1000, "auctionId": null, "createdAt": "2026-11-12T09:15:02.123Z" }
  ],
  "page": { "size": 20, "number": 0, "totalElements": 2, "totalPages": 1 }
}
```

### 5.8 `POST /api/wallet/top-up` (JWT)

Alimentare demo: `amount` între 1 și 10000. Înregistrează o tranzacție `TOP_UP`.

**Cerere**
```json
{ "amount": 500 }
```
**Răspuns 200** `WalletDto`. **Erori:** 400 `VALIDATION_FAILED`

## 6. auction-service: API public

Responsabil: **K**. Prin gateway, pe ruta `/api/auctions/**`.

### 6.1 `POST /api/auctions` (JWT)

**Cerere**
```json
{
  "title": "Aparat foto vintage",
  "description": "Funcțional, cu husa originală.",
  "startingPrice": 100,
  "minIncrement": 10,
  "startTime": "2026-11-20T18:00:00Z",
  "endTime": "2026-11-20T19:00:00Z"
}
```

**Validare:**
- `title`: 3–120 de caractere;
- `description`: 1–2000 de caractere;
- `startingPrice` ≥ 1 și `minIncrement` ≥ 1;
- `startTime` ≥ acum − 1 minut (toleranță pentru ceasul clientului);
- `endTime` > `startTime`;
- durata între 1 minut și 7 zile.

**Răspuns 201** `AuctionDetails` (§6.5), cu header-ul `Location: /api/auctions/42`. Statusul devine `ACTIVE` dacă `startTime ≤ acum`, altfel `SCHEDULED`. Inițial `currentPrice = startingPrice` și `bidCount = 0`.

**Erori:** 400 `VALIDATION_FAILED` · 400 `INVALID_AUCTION_TIMES`

### 6.2 `POST /api/auctions/{id}/photos` (JWT, doar vânzătorul)

- **Format:** `multipart/form-data`, unul sau mai multe câmpuri `files`.
- **Limite:** maximum **5 fotografii** per licitație în total; tipuri `image/jpeg`, `image/png`, `image/webp`; maximum **5 MB** per fișier.
- **Stocare:** fișierele se salvează sub nume **UUID aleatoare**, niciodată sub numele trimis de client. Prima fotografie (`position = 0`) este fotografia principală.

**Răspuns 200**
```json
{ "photoUrls": ["/api/auctions/photos/5b0e3c1e-8c1f-4f7a-9a51-2f1f0c3d9e10.jpg"] }
```

**Erori:**
- 403 `NOT_AUCTION_OWNER`
- 404 `AUCTION_NOT_FOUND`
- 400 `TOO_MANY_PHOTOS`
- 415 `UNSUPPORTED_PHOTO_TYPE`
- 413 `PHOTO_TOO_LARGE`
- 409 `AUCTION_ENDED`

### 6.3 `GET /api/auctions/photos/{filename}` (public)

Răspunde cu octeții imaginii și `Content-Type` corect. **Erori:** 404 `PHOTO_NOT_FOUND`

### 6.4 `GET /api/auctions?status=ACTIVE&page=0&size=12&sort=endTime,asc` (public)

`status` (`SCHEDULED` | `ACTIVE` | `ENDED`) este opțional: fără el se returnează toate. **Răspuns 200** `PagedModel<AuctionSummary>`:
```json
{
  "content": [
    {
      "id": 42,
      "title": "Aparat foto vintage",
      "mainPhotoUrl": "/api/auctions/photos/5b0e3c1e-8c1f-4f7a-9a51-2f1f0c3d9e10.jpg",
      "currentPrice": 170,
      "bidCount": 3,
      "status": "ACTIVE",
      "startTime": "2026-11-20T18:00:00Z",
      "endTime": "2026-11-20T19:00:30Z"
    }
  ],
  "page": { "size": 12, "number": 0, "totalElements": 1, "totalPages": 1 }
}
```
`mainPhotoUrl` este `null` dacă licitația nu are fotografii.

### 6.5 `GET /api/auctions/{id}` (public)

**Răspuns 200** `AuctionDetails`: câmpurile din `AuctionSummary`, plus:
```json
{
  "id": 42,
  "title": "Aparat foto vintage",
  "mainPhotoUrl": "/api/auctions/photos/5b0e3c1e-8c1f-4f7a-9a51-2f1f0c3d9e10.jpg",
  "currentPrice": 170,
  "bidCount": 3,
  "status": "ACTIVE",
  "startTime": "2026-11-20T18:00:00Z",
  "endTime": "2026-11-20T19:00:30Z",
  "description": "Funcțional, cu husa originală.",
  "photoUrls": ["/api/auctions/photos/5b0e3c1e-8c1f-4f7a-9a51-2f1f0c3d9e10.jpg"],
  "sellerId": 3,
  "startingPrice": 100,
  "minIncrement": 10,
  "highestBidderId": 7,
  "extensionCount": 1,
  "winnerId": null,
  "finalPrice": null,
  "serverTime": "2026-11-20T18:59:12.512Z"
}
```
`serverTime` permite front-end-ului să calculeze diferența dintre ceasul serverului și cel al clientului. **Erori:** 404 `AUCTION_NOT_FOUND`

### 6.6 `GET /api/auctions/mine?page=0&size=12` (JWT)

Licitațiile create de apelant, ca vânzător. **Răspuns 200** `PagedModel<AuctionSummary>`.

## 7. bidding-service: API public

Responsabil: **M**. Prin gateway, pe ruta `/api/bids/**`.

### 7.1 `POST /api/bids` (JWT)

Fluxul complet este descris în [architecture.md §6.1](architecture.md#61-plasarea-unei-oferte).

**Cerere**
```json
{ "auctionId": 42, "amount": 180 }
```

**Regula sumei minime:** dacă licitația nu are oferte, suma trebuie să fie cel puțin `startingPrice`. Altfel, cel puțin `highestAmount + minIncrement`.

**Răspuns 201**
```json
{ "bidId": 981, "auctionId": 42, "amount": 180, "endTime": "2026-11-20T19:01:00Z", "extended": true }
```

**Erori:**

| Status | `code` | Când |
|---|---|---|
| 400 | `VALIDATION_FAILED` | corp invalid (`amount` < 1 etc.) |
| 400 | `BID_TOO_LOW` | sub minimul de mai sus |
| 403 | `OWN_AUCTION` | licitantul este vânzătorul |
| 404 | `AUCTION_NOT_FOUND` | licitația nu există |
| 409 | `AUCTION_NOT_ACTIVE` | licitația nu e `ACTIVE` sau timpul a expirat |
| 409 | `INSUFFICIENT_FUNDS` | `available` (+ rezervarea curentă) < `amount` |
| 503 | `SERVICE_UNAVAILABLE` | user-service sau auction-service nu răspunde (timeout) |

### 7.2 `GET /api/bids/auction/{auctionId}?page=0&size=20` (public)

Istoricul ofertelor, cele mai noi primele. **Răspuns 200** `PagedModel<BidHistoryItem>`:
```json
{
  "content": [
    { "bidId": 981, "amount": 180, "bidderId": 7, "bidderUsername": "ana.pop", "createdAt": "2026-11-20T18:59:41.200Z" }
  ],
  "page": { "size": 20, "number": 0, "totalElements": 4, "totalPages": 1 }
}
```

### 7.3 `GET /api/bids/mine?page=0&size=20` (JWT)

Ofertele apelantului, cele mai noi primele. **Răspuns 200** `PagedModel<MyBidItem>`:
```json
{
  "content": [ { "bidId": 981, "auctionId": 42, "amount": 180, "createdAt": "2026-11-20T18:59:41.200Z" } ],
  "page": { "size": 20, "number": 0, "totalElements": 1, "totalPages": 1 }
}
```

## 8. API intern (`/internal/**`)

- **Cine apelează:** serviciile între ele, direct în rețeaua Docker, cu header-ul `X-Internal-Key: ${INTERNAL_API_KEY}`.
- **Cheie lipsă sau greșită:** **401** `INTERNAL_KEY_INVALID`.
- **Gateway:** nu rutează aceste căi.
- **Timeouts pe client:** connect 2 s, read 5 s. După timeout, apelantul răspunde 503 `SERVICE_UNAVAILABLE` sau reîncearcă, după caz.

### 8.1 user-service (responsabil D)

#### `PUT /internal/wallet/reservations`

**Setează** rezervarea utilizatorului pentru licitație la `amount` (nu adună). Operația este **idempotentă** și cere `available + rezervareaCurentă ≥ amount`.

**Cerere**
```json
{ "userId": 7, "auctionId": 42, "amount": 180 }
```
**Răspuns 200**
```json
{ "userId": 7, "auctionId": 42, "amount": 180, "balance": 1000, "reserved": 180, "available": 820 }
```
**Erori:** 409 `INSUFFICIENT_FUNDS` · 404 `USER_NOT_FOUND`

#### `DELETE /internal/wallet/reservations?userId=7&auctionId=42`

Eliberează rezervarea (`reserved −= amount`, rândul se șterge). **204** și când nu există rezervare (idempotent).

#### `POST /internal/wallet/settlements`

Decontarea unei licitații încheiate, **idempotentă per `auctionId`** (tabelul `wallet_settlements`).

**Cerere cu câștigător**
```json
{ "auctionId": 42, "winnerId": 7, "sellerId": 3, "amount": 180 }
```
**Cerere fără oferte**
```json
{ "auctionId": 43, "winnerId": null, "sellerId": 3, "amount": null }
```

**Pași, într-o singură tranzacție:**
1. Dacă există deja un rând în `wallet_settlements` pentru `auctionId`, răspunde 200 cu `alreadySettled: true` și nu modifică nimic.
2. Blochează portofelele implicate cu `PESSIMISTIC_WRITE`, **în ordinea crescătoare a `userId`**, pentru a evita deadlock-urile.
3. Câștigătorul: `balance −= amount`, `reserved −= amount`, șterge rezervarea lui, tranzacție `PAYMENT`.
4. Vânzătorul: `balance += amount`, tranzacție `PAYOUT`.
5. Eliberează **toate celelalte** rezervări ale licitației.
6. Inserează rândul în `wallet_settlements`.

**Răspuns 200**
```json
{ "auctionId": 42, "alreadySettled": false }
```

### 8.2 auction-service (responsabil K)

#### `GET /internal/auctions/{id}`

**Răspuns 200**
```json
{
  "id": 42, "title": "Aparat foto vintage", "sellerId": 3, "status": "ACTIVE",
  "startingPrice": 100, "minIncrement": 10, "currentPrice": 170, "highestBidderId": 5,
  "startTime": "2026-11-20T18:00:00Z", "endTime": "2026-11-20T19:00:30Z"
}
```
**Erori:** 404 `AUCTION_NOT_FOUND`

#### `POST /internal/auctions/{id}/bid-placed`

Apelat de bidding-service cât timp ține lock-ul pe starea licitației. Blochează rândul `auctions` (`PESSIMISTIC_WRITE`).

**Cerere**
```json
{ "amount": 180, "bidderId": 7, "bidAt": "2026-11-20T19:00:12.000Z" }
```

**Comportament:**
- 409 `AUCTION_NOT_ACTIVE` dacă `status ≠ ACTIVE` sau `bidAt ≥ endTime`.
- Altfel: `currentPrice = amount`, `highestBidderId = bidderId`, `bidCount += 1`.
- **Anti-sniping:** dacă `endTime − bidAt < 30 s`, atunci `endTime += 30 s` și `extensionCount += 1`.

**Răspuns 200**
```json
{ "endTime": "2026-11-20T19:01:00Z", "extended": true }
```

### 8.3 bidding-service (responsabil M)

#### `GET /internal/bids/auction/{auctionId}/highest`

**Răspuns 200** `{ "bidderId": 7, "amount": 180 }`, sau **204** dacă nu există oferte. Se folosește la verificări și reconciliere.

### 8.4 notification-service (responsabil R)

#### `POST /internal/events`

**Cerere** (anvelopa din §9.2, plus `targetUserId`):
```json
{
  "type": "OUTBID",
  "auctionId": 42,
  "targetUserId": 5,
  "serverTime": "2026-11-20T19:00:12.051Z",
  "data": { "auctionId": 42, "title": "Aparat foto vintage", "yourAmount": 170, "newAmount": 180 }
}
```

- **Răspuns:** **202** (livrarea e asincronă, „best effort”).
- **Validare:**
  - `type` trebuie să fie unul dintre tipurile din §9.3;
  - `auctionId` este obligatoriu;
  - `targetUserId` este obligatoriu pentru `OUTBID`, `AUCTION_WON` și `AUCTION_SOLD` și trebuie să fie `null` pentru celelalte.
- **Erori:** 400 `VALIDATION_FAILED` · 401 `INTERNAL_KEY_INVALID`

## 9. WebSocket / STOMP și evenimente

### 9.1 Conexiune

| Element | Valoare |
|---|---|
| Endpoint | `ws://localhost:8080/ws` (prin gateway); în browser: `ws(s)://<host-ul paginii>/ws` (relativ) |
| Protocol | STOMP 1.2 peste WebSocket simplu (fără SockJS) |
| Autentificare | opțională: header STOMP `Authorization: Bearer <jwt>` în cadrul `CONNECT`. notification-service validează tokenul; numele `Principal` = **userId** |
| Topic public | `/topic/auctions/{auctionId}`, abonare permisă oricui |
| Coadă privată | `/user/queue/notifications`, doar conexiuni autentificate; serverul trimite cu `convertAndSendToUser(userId, "/queue/notifications", event)` |
| Heartbeat recomandat | 10000 ms / 10000 ms |

### 9.2 Anvelopa mesajului

Aceeași anvelopă se folosește în corpul `POST /internal/events` (cu `targetUserId` în plus) și în mesajul WebSocket:

```json
{
  "type": "BID_PLACED",
  "auctionId": 42,
  "serverTime": "2026-11-20T19:00:12.060Z",
  "data": { }
}
```

- **Cine completează `serverTime`:** emitentul. notification-service îl **suprascrie** cu ceasul propriu în momentul difuzării, ca front-end-ul să-și calculeze offset-ul față de momentul livrării.
- **Cronometrele din front-end** folosesc `endTime` + offset-ul calculat din `serverTime`, niciodată ceasul brut al clientului.

### 9.3 Tipuri de evenimente

| `type` | Trimis de | Destinație | `data` |
|---|---|---|---|
| `AUCTION_STARTED` | auction-service | `/topic/auctions/{id}` | `startTime, endTime` |
| `BID_PLACED` | bidding-service | `/topic/auctions/{id}` | `bidId, amount, bidderId, bidderUsername, bidCount, endTime, extended` |
| `OUTBID` | bidding-service | coada privată a liderului anterior | `auctionId, title, yourAmount, newAmount` |
| `AUCTION_ENDED` | auction-service | `/topic/auctions/{id}` | `winnerId, finalPrice` (ambele `null` dacă nu au existat oferte) |
| `AUCTION_WON` | auction-service | coada privată a câștigătorului | `auctionId, title, finalPrice` |
| `AUCTION_SOLD` | auction-service | coada privată a vânzătorului | `auctionId, title, finalPrice, winnerId` |

**Exemple de `data`:**

```json
{ "type": "BID_PLACED", "auctionId": 42, "serverTime": "2026-11-20T19:00:12.060Z",
  "data": { "bidId": 981, "amount": 180, "bidderId": 7, "bidderUsername": "ana.pop", "bidCount": 4, "endTime": "2026-11-20T19:01:00Z", "extended": true } }
```
```json
{ "type": "AUCTION_ENDED", "auctionId": 42, "serverTime": "2026-11-20T19:01:00.912Z",
  "data": { "winnerId": 7, "finalPrice": 180 } }
```

## 10. Catalogul codurilor de eroare

| `code` | Status | Serviciu | Semnificație |
|---|---|---|---|
| `VALIDATION_FAILED` | 400 | toate | corp sau parametri invalizi (`errors[]`) |
| `UNAUTHORIZED` | 401 | gateway | lipsește JWT-ul sau e invalid/expirat pe o rută protejată |
| `FORBIDDEN` | 403 | gateway | autentificat, dar fără drept |
| `INTERNAL_KEY_INVALID` | 401 | toate (intern) | `X-Internal-Key` lipsă sau greșit |
| `NOT_FOUND` | 404 | toate | rută inexistentă |
| `SERVICE_UNAVAILABLE` | 503 | bidding, auction | un serviciu dependent nu răspunde |
| `INTERNAL_ERROR` | 500 | toate | eroare neprevăzută (detaliile doar în log) |
| `USERNAME_TAKEN` | 409 | user | username deja folosit |
| `EMAIL_TAKEN` | 409 | user | email deja folosit |
| `INVALID_CREDENTIALS` | 401 | user | login eșuat |
| `USER_NOT_FOUND` | 404 | user | utilizator inexistent |
| `INSUFFICIENT_FUNDS` | 409 | user, bidding | fonduri disponibile insuficiente |
| `AUCTION_NOT_FOUND` | 404 | auction, bidding | licitație inexistentă |
| `INVALID_AUCTION_TIMES` | 400 | auction | start/sfârșit invalide sau durată în afara intervalului 1 min–7 zile |
| `NOT_AUCTION_OWNER` | 403 | auction | doar vânzătorul poate modifica licitația |
| `TOO_MANY_PHOTOS` | 400 | auction | s-ar depăși 5 fotografii |
| `UNSUPPORTED_PHOTO_TYPE` | 415 | auction | doar jpeg/png/webp |
| `PHOTO_TOO_LARGE` | 413 | auction | fișier > 5 MB |
| `PHOTO_NOT_FOUND` | 404 | auction | fotografie inexistentă |
| `AUCTION_ENDED` | 409 | auction | licitația s-a încheiat |
| `AUCTION_NOT_ACTIVE` | 409 | auction, bidding | licitația nu e activă sau timpul a expirat |
| `BID_TOO_LOW` | 400 | bidding | suma e sub minimul permis |
| `OWN_AUCTION` | 403 | bidding | nu poți licita la propria licitație |

## 11. Istoricul versiunilor

| Versiune | Data | Modificare | Aprobat |
|---|---|---|---|
| v1 | 27.10.2026 | Versiunea inițială (bootstrap) | M (de confirmat la S0) |
