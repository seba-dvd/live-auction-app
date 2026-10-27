# Ghidul lui A — Product Owner · frontend

## 1. Pe scurt

- **Deții:**
  - `frontend/` (React 19 + TypeScript + Vite, `react-router-dom`, `@stomp/stompjs`);
  - backlog-ul de produs (`docs/product/backlog.md` și issues `type:story`);
  - diagrama de cazuri de utilizare.
- **Ramura ta:** `a/frontend`. PR-urile tale le revizuiește **K**.
- **Rolul de curs:** Product Owner. Prioritizezi backlog-ul, accepți poveștile la sprint review și pregătești scenariul de demo.
- **Primele 3 acțiuni săptămâna asta:**
  1. rafinează user stories din `docs/product/backlog.md` și issues `[US-nn]` (criterii, priorități);
  2. stabilește MVP-ul cu echipa;
  3. pornește `npm run dev` și familiarizează-te cu scheletul.
- **Regula de aur:** în cod folosești **doar URL-uri relative** (`/api/...`, `/ws`). Vite (în dezvoltare) și nginx (în Docker) le trimit la gateway.

## 2. Rolul tău

| Responsabilitate | Frecvență |
|---|---|
| Ții backlog-ul la zi: povești noi, criterii „Dat fiind / Când / Atunci”, prioritate MoSCoW | săptămânal |
| Aduci prioritățile la sprint planning și explici fiecare poveste aleasă | prima zi a sprintului |
| Accepți sau respingi poveștile la sprint review, pe baza criteriilor de acceptanță | ultima zi a sprintului |
| Răspunzi la întrebările de produs ale echipei („cum trebuie să se comporte…?”) | continuu, în 24 h |
| Diagrama use case și descrierile cazurilor de utilizare | S1, apoi la schimbări |
| Scenariul de demonstrație (două browsere) și repetițiile lui | S3–S4 |

## 3. Ce deții

| Al tău | Doar prin PR, cu proprietarul ca reviewer |
|---|---|
| `frontend/**` | `frontend/Dockerfile` și `frontend/nginx.conf`, revizuite și de R |
| `docs/product/**`, `docs/uml/use-case.puml` | `docs/api-contracts.md` (M): dacă UI-ul are nevoie de un câmp nou, ceri schimbarea prin PR |

**Nu atinge** serviciile backend. Dacă un endpoint nu se comportă conform contractului, deschide un issue de tip bug pentru proprietarul lui.

## 4. Setup (o singură dată)

1. **Instalează:**
   - Git;
   - Docker Desktop cu WSL2;
   - Node.js 24 LTS (<https://nodejs.org/>, versiunea din `frontend/.nvmrc`);
   - VS Code (<https://code.visualstudio.com/>) sau IntelliJ IDEA;
   - Postman.
2. **Acceptă invitația** la repository.
3. **Clonează și pornește:**
   ```bash
   git clone https://github.com/seba-dvd/live-auction-app.git
   cd live-auction-app
   git checkout a/frontend
   cp .env.example .env
   docker compose up -d --build        # backend-ul complet (pentru tine, totul în Docker)
   cd frontend
   npm ci
   npm run dev                         # http://localhost:5173
   ```

## 5. Cum rulezi și testezi partea ta

- **Dezvoltare:**
  - backend-ul rulează în Docker, iar `npm run dev` pornește aplicația pe <http://localhost:5173>, cu hot reload;
  - Vite trimite `/api` și `/ws` la `http://localhost:8080` (`vite.config.ts`).
- **Verificare înainte de PR:** `npm run build` (verificare TypeScript + build) și `npm run lint`.
- **Ca în producție:** `docker compose up -d --build frontend`, apoi <http://localhost:3000> (nginx face proxy la gateway).
- **Fără backend gata:** lucrezi cu date mock într-un fișier `src/api/mock.ts`, cu aceeași formă ca în [api-contracts.md](../api-contracts.md). Comutarea se face cu o variabilă `VITE_USE_MOCKS=true` (Vite expune doar variabilele cu prefixul `VITE_`).
- **Testarea WebSocket-ului fără UI:** `tools/ws-test.html` (vezi ghidul lui R).

## 6. Plan pe sprinturi

### S0 · Setup (28.10–08.11)

- [ ] **A-S0-01 · Rafinează user stories**
  - **Ce:** pentru fiecare issue `[US-nn]`, verifici povestea, criteriile de acceptanță și prioritatea MoSCoW. Adaugi ce lipsește și ștergi ce nu se face.
  - **Gata când:** toate poveștile Must au criterii clare, iar backlog-ul e ordonat după prioritate.
  - **Depinde de:** —
  - **Etichete:** `area:docs` `type:story` `priority:must`
- [ ] **A-S0-02 · MVP-ul și scenariul de demo (versiunea 1)**
  - **Ce:** stabilești cu echipa ce intră în MVP (poveștile Must) și scrii scenariul de demo pas cu pas.
  - **Gata când:** scenariul e în `docs/product/backlog.md` (secțiunea MVP) și echipa e de acord.
  - **Depinde de:** A-S0-01.
  - **Etichete:** `area:docs` `type:docs` `priority:must`

### S1 · Design & fundații (09.11–22.11)

- [ ] **A-S1-01 · Diagrama use case și descrierile cazurilor (Ședințele 4–5)**
  - **Ce:** actualizezi `docs/uml/use-case.puml` (actori, `<<include>>`, `<<extend>>`), regenerezi imaginea și completezi descrierile din Raportul cap. 5.
  - **Gata când:** diagrama e prezentată la Ședințele 4–5, iar PNG-ul e comis.
  - **Depinde de:** —
  - **Etichete:** `area:docs` `type:uml` `priority:must`
- [ ] **A-S1-02 · Structura aplicației: rute, layout, AuthContext**
  - **Ce:**
    - `AuthContext` (token, user, login/logout, persistat în `sessionStorage`);
    - rute protejate (redirect la `/login`, cu întoarcere după autentificare);
    - meniul, care arată utilizatorul autentificat.
  - **Gata când:** fără token, `/wallet` duce la `/login`; după login, utilizatorul se întoarce la `/wallet`.
  - **Depinde de:** —
  - **Etichete:** `area:frontend` `type:feature` `priority:must`
- [ ] **A-S1-03 · Clientul API**
  - **Ce:** `src/api/client.ts`:
    - un singur wrapper peste `fetch`;
    - adaugă `Authorization: Bearer`;
    - parsează JSON;
    - transformă erorile ProblemDetail într-un `ApiError` cu `status`, `code` și `detail`;
    - la 401 face logout și redirecționează.
  - **Gata când:** toate apelurile trec prin wrapper; mesajele de eroare se aleg după `code`.
  - **Depinde de:** A-S1-02.
  - **Etichete:** `area:frontend` `type:feature` `priority:must`
- [ ] **A-S1-04 · Paginile de autentificare și înregistrare**
  - **Ce:** formulare cu validare în client (aceleași reguli ca în contract) și apeluri reale prin gateway.
  - **Gata când:** se poate crea un cont și te poți autentifica în aplicație; erorile `USERNAME_TAKEN` și `INVALID_CREDENTIALS` sunt afișate clar.
  - **Depinde de:** A-S1-03, D-S1-03.
  - **Etichete:** `area:frontend` `type:feature` `priority:must`
- [ ] **A-S1-05 · Lista de licitații cu date mock**
  - **Ce:** carduri `AuctionSummary` și tab-uri SCHEDULED / ACTIVE / ENDED, cu date mock în forma din contract.
  - **Gata când:** pagina principală arată licitațiile mock, cu paginare simulată.
  - **Depinde de:** A-S1-02.
  - **Etichete:** `area:frontend` `type:feature` `priority:should`

### S2 · Fluxuri de bază (23.11–06.12)

- [ ] **A-S2-01 · Lista reală de licitații (tab-uri și paginare)**
  - **Ce:** `GET /api/auctions?status=…&page=…&size=12&sort=…` și paginarea din `page.number` / `page.totalPages`.
  - **Gata când:** US-03 e acceptată (stările de încărcare, listă goală și eroare sunt incluse).
  - **Depinde de:** K-S1-04.
  - **Etichete:** `area:frontend` `type:feature` `priority:must`
- [ ] **A-S2-02 · Pagina de detalii (statică)**
  - **Ce:** galeria de fotografii, descrierea, prețurile, istoricul ofertelor (`GET /api/bids/auction/{id}`) și cronometrul calculat cu `serverTime` (§7.3).
  - **Gata când:** US-04 e acceptată.
  - **Depinde de:** K-S1-04, M-S1-03.
  - **Etichete:** `area:frontend` `type:feature` `priority:must`
- [ ] **A-S2-03 · Formularul de creare și încărcarea fotografiilor**
  - **Ce:**
    - formularul, cu validări (start < end, durata maximă 7 zile);
    - `POST /api/auctions`, apoi `POST /api/auctions/{id}/photos` (`FormData` cu câmpul `files`);
    - previzualizarea fotografiilor.
  - **Gata când:** US-05 și US-06 sunt acceptate.
  - **Depinde de:** K-S1-03, K-S2-04.
  - **Etichete:** `area:frontend` `type:feature` `priority:must`
- [ ] **A-S2-04 · Pagina portofelului**
  - **Ce:** soldul, suma rezervată și suma disponibilă, istoricul paginat și formularul de alimentare.
  - **Gata când:** US-13 și US-14 sunt acceptate.
  - **Depinde de:** D-S2-04.
  - **Etichete:** `area:frontend` `type:feature` `priority:must`
- [ ] **A-S2-05 · Raport Tehnic: capitolele 1 și 5**
  - **Ce:** revizuiești `01-descrierea-aplicatiei.md` și `05-cazuri-de-utilizare.md`.
  - **Gata când:** cap. 1 e pe `develop` până pe 20.11, iar cap. 5 până pe 24.11.
  - **Depinde de:** A-S1-01.
  - **Etichete:** `area:docs` `type:docs` `priority:must`

### S3 · Timp real & integrare (07.12–20.12)

- [ ] **A-S3-01 · Conexiunea STOMP și abonarea la licitație**
  - **Ce:** `src/api/realtime.ts` (§7.3); te abonezi la `/topic/auctions/{id}` pe pagina licitației și te deconectezi la ieșire (cleanup în `useEffect`).
  - **Gata când:** în două browsere, o ofertă apare în celălalt în cel mult 1 secundă.
  - **Depinde de:** R-S1-02, M-S2-03.
  - **Etichete:** `area:frontend` `type:feature` `priority:must`
- [ ] **A-S3-02 · Istoric live și cronometru sincronizat**
  - **Ce:** `BID_PLACED` actualizează prețul, lista și sfârșitul (inclusiv la prelungire); `AUCTION_ENDED` afișează câștigătorul; offset-ul se recalculează din fiecare `serverTime`.
  - **Gata când:** US-09 și US-11 sunt acceptate, inclusiv testul cu ceasul calculatorului decalat cu 2 minute.
  - **Depinde de:** A-S3-01.
  - **Etichete:** `area:frontend` `type:feature` `priority:must`
- [ ] **A-S3-03 · Formularul de ofertă și mesajele după `code`**
  - **Ce:** suma minimă sugerată (`currentPrice + minIncrement`, sau `startingPrice` dacă nu există oferte) și mesaje pentru `BID_TOO_LOW`, `OWN_AUCTION`, `AUCTION_NOT_ACTIVE`, `INSUFFICIENT_FUNDS`.
  - **Gata când:** US-07 și US-08 sunt acceptate.
  - **Depinde de:** M-S2-01.
  - **Etichete:** `area:frontend` `type:feature` `priority:must`
- [ ] **A-S3-04 · Notificări toast pentru OUTBID, WON și SOLD**
  - **Ce:** o conexiune autentificată (JWT în `connectHeaders`) pe toată aplicația, abonată la `/user/queue/notifications`; toast-uri cu link spre licitație.
  - **Gata când:** US-10 și US-16 sunt acceptate.
  - **Depinde de:** R-S2-01, K-S3-02.
  - **Etichete:** `area:frontend` `type:feature` `priority:should`
- [ ] **A-S3-05 · Build-ul de producție în Docker (cu R)**
  - **Ce:** verifici `frontend/Dockerfile` și `nginx.conf` (fallback SPA, proxy `/api` și `/ws`) pe <http://localhost:3000>.
  - **Gata când:** toate paginile, inclusiv refresh pe `/auctions/5`, merg din containerul nginx.
  - **Depinde de:** —
  - **Etichete:** `area:frontend` `type:infra` `priority:must`
- [ ] **A-S3-06 · Scenariul de demo (versiunea finală)**
  - **Ce:** pașii exacți, conturile de test și datele inițiale (cu folderul Postman „Demo setup” al lui R).
  - **Gata când:** echipa a rulat scenariul cap-coadă cel puțin o dată.
  - **Depinde de:** R-S3-05.
  - **Etichete:** `area:docs` `type:docs` `priority:must`

### S4 · Cloud & final (04.01–17.01)

- [ ] **A-S4-01 · Finisare: stări de încărcare, gol și eroare; responsive**
  - **Ce:** fiecare pagină are stările de încărcare, listă goală și eroare; layout-ul funcționează pe telefon (360 px).
  - **Gata când:** o verificare completă pe desktop și pe mobil nu găsește pagini „rupte”.
  - **Depinde de:** —
  - **Etichete:** `area:frontend` `type:feature` `priority:should`
- [ ] **A-S4-02 · Testarea de acceptanță a tuturor poveștilor**
  - **Ce:** parcurgi criteriile fiecărei povești Must și Should în mediul din cloud și închizi sau redeschizi issues-urile.
  - **Gata când:** toate poveștile Must sunt acceptate.
  - **Depinde de:** R-S4-01.
  - **Etichete:** `area:docs` `type:story` `priority:must`
- [ ] **A-S4-03 · Repetiția demo-ului**
  - **Ce:** două repetiții complete cu timp măsurat, plus un plan B (video înregistrat) dacă rețeaua cade.
  - **Gata când:** demo-ul încape în timpul alocat, iar video-ul de rezervă există.
  - **Depinde de:** A-S3-06.
  - **Etichete:** `area:docs` `type:docs` `priority:must`

## 7. Specificație tehnică

### 7.1 Ce consumi (toate prin `/api` și `/ws`, relativ)

| Pagina | Endpoint-uri | Contract |
|---|---|---|
| `/login`, `/register` | `POST /api/auth/login`, `POST /api/auth/register` | [§5.1–5.2](../api-contracts.md#5-user-service-api-public) |
| `/` | `GET /api/auctions?status&page&size&sort` | §6.4 |
| `/auctions/:id` | `GET /api/auctions/{id}`, `GET /api/bids/auction/{id}`, `POST /api/bids`, STOMP `/topic/auctions/{id}` | §6.5, §7.1–7.2, §9 |
| `/auctions/new` | `POST /api/auctions`, `POST /api/auctions/{id}/photos` | §6.1–6.2 |
| `/wallet` | `GET /api/wallet`, `GET /api/wallet/transactions`, `POST /api/wallet/top-up` | §5.6–5.8 |
| global | STOMP `/user/queue/notifications` (cu JWT) | §9 |

**Structura recomandată:**
- `src/api/`: `client.ts`, `auth.ts`, `auctions.ts`, `bids.ts`, `wallet.ts`, `realtime.ts`, `types.ts` (tipurile din contracte);
- `src/context/AuthContext.tsx`;
- `src/pages/`: o pagină per rută;
- `src/components/`: `AuctionCard`, `Countdown`, `BidForm`, `BidHistory`, `Toasts`.

### 7.2 Erori

Răspunsurile de eroare au forma ProblemDetail:

```json
{ "status": 409, "detail": "...", "code": "INSUFFICIENT_FUNDS" }
```

Afișezi un mesaj în română ales după `code`, nu textul din `detail`. Un 401 pe o cerere protejată înseamnă token expirat: faci logout și redirecționezi la `/login`.

### 7.3 Codul care previne greșelile clasice

**Conexiunea STOMP relativă la pagină și cronometrul sincronizat cu serverul.** Codul a fost verificat cu `tsc`, cu setările proiectului:

```ts
import { Client, type IMessage } from '@stomp/stompjs'

export type AuctionEvent = {
  type: string
  auctionId: number
  serverTime: string
  data: Record<string, unknown>
}

export function connectToAuction(
  auctionId: number,
  token: string | null,
  onEvent: (event: AuctionEvent) => void,
): Client {
  const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws'
  const client = new Client({
    brokerURL: `${protocol}://${window.location.host}/ws`, // relative to the page: Vite / nginx proxy it
    connectHeaders: token ? { Authorization: `Bearer ${token}` } : {},
    reconnectDelay: 3000,
  })
  client.onConnect = () => {
    client.subscribe(`/topic/auctions/${auctionId}`, (message: IMessage) =>
      onEvent(JSON.parse(message.body) as AuctionEvent),
    )
  }
  client.activate()
  return client // call client.deactivate() when the page unmounts (useEffect cleanup)
}

// > 0 when the server clock is ahead of the browser clock
export function clockOffsetMs(serverTime: string): number {
  return Date.parse(serverTime) - Date.now()
}

export function remainingMs(endTime: string, offsetMs: number): number {
  return Math.max(0, Date.parse(endTime) - (Date.now() + offsetMs))
}
```

### 7.4 Decizii și capcane

- **Nu scrie niciodată `http://localhost:8080` în cod.** Totul e relativ. Altfel aplicația nu mai merge în Docker și în cloud.
- **Fără conexiuni duble:**
  - `StrictMode` montează componentele de două ori în dezvoltare, deci cleanup-ul din `useEffect` (`client.deactivate()`) e obligatoriu;
  - fă o singură conexiune pentru notificările private (în layout), nu una per pagină.
- **După reconectare** reîncarci prin REST detaliile și istoricul, ca să nu pierzi evenimente.
- **Cronometrul** folosește `endTime` din cel mai recent eveniment, pentru că anti-sniping-ul îl schimbă.
- **Fotografiile** se trimit cu `FormData` (fără `Content-Type` setat manual), câmpul `files`, cel mult 5.
- **Tokenul** stă în memorie plus `sessionStorage` (nu `localStorage`), iar la logout îl ștergi.
- **TypeScript 7:** proiectul are `verbatimModuleSyntax`, deci importurile de tipuri se scriu `import { type X }`.

## 8. Dependențe

| Aștepți de la | Ce | Cum te deblochezi |
|---|---|---|
| D | login, register, portofel, gateway cu JWT | date mock + un token fals în `AuthContext` |
| K | listele, detaliile, crearea, fotografiile | date mock în forma din contract |
| M | ofertele, istoricul | mock + formularul care afișează erorile simulate |
| R | WebSocket-ul și notificările | `tools/ws-test.html` + evenimente trimise din Postman |

| Așteaptă de la tine | Ce | Când |
|---|---|---|
| echipa | prioritățile fiecărui sprint, acceptanța poveștilor | la fiecare sprint |
| toți | diagrama use case | S1 (Ședințele 4–5) |
| D | scenariul de demo | S3–S4 |

## 9. Documentație

| Ce | Fișier | Termen |
|---|---|---|
| Diagrama use case | `docs/uml/use-case.puml` | S1 (Ședințele 4–5) |
| Raport cap. 1 (descrierea aplicației) | `docs/raport-tehnic/src/01-descrierea-aplicatiei.md` | 20.11 |
| Raport cap. 5 (cazuri de utilizare) | `docs/raport-tehnic/src/05-cazuri-de-utilizare.md` | 24.11 |
| Backlog-ul și scenariul de demo | `docs/product/backlog.md` | continuu / S3 |

## 10. Git zilnic

```bash
git checkout a/frontend
git fetch origin && git merge origin/develop
cd frontend && npm ci          # după merge, dacă package-lock.json s-a schimbat
# ... lucrezi ...
npm run build && npm run lint
git add frontend/ docs/product/
git commit -m "feat(frontend): live bid history with synced countdown"
git push origin a/frontend
gh pr create --base develop --head a/frontend --title "feat(frontend): live auction page" --body "Closes #<nr>"
```

**Conflicte de merge:** [CONTRIBUTING §5](../../CONTRIBUTING.md#5-conflicte-de-merge). Dacă conflictul e în `package-lock.json`, acceptă versiunea din `develop`, rulează `npm install`, apoi comite lock-ul regenerat.

## 11. Definition of Done

- [ ] `npm run build` și `npm run lint` trec;
- [ ] criteriile „Dat fiind / Când / Atunci” ale poveștii sunt îndeplinite;
- [ ] pagina are stări de încărcare, gol și eroare;
- [ ] doar URL-uri relative; nu există secrete în cod;
- [ ] PR-ul e aprobat de K, iar CI-ul e verde;
- [ ] funcționează și pe <http://localhost:3000> (nginx).

## 12. Resurse și ajutor

- **React:** <https://react.dev/learn>
- **React Router:** <https://reactrouter.com/>
- **Vite, server proxy:** <https://vite.dev/config/server-options#server-proxy>
- **STOMP.js:** <https://stomp-js.github.io/guide/stompjs/using-stompjs-v5.html>
- **TypeScript:** <https://www.typescriptlang.org/docs/>
- **User stories și criterii de acceptanță:** Scrum Guide (<https://scrumguides.org>)
- **Pe cine întrebi:**
  - contractele API: **M**;
  - login, JWT și portofel: **D**;
  - licitațiile și fotografiile: **K**;
  - WebSocket, nginx și Docker: **R**;
  - procesul Scrum și board-ul: **K**.
- **Dacă folosești un asistent AI:** pune-l să citească întâi `CLAUDE.md`, ghidul acesta și `docs/api-contracts.md`.
