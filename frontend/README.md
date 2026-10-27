# frontend

Aplicația React a proiectului Live Auction. Responsabil: **A** (ramura `a/frontend`). Ghidul complet este în [../docs/team/A.md](../docs/team/A.md).

**Tehnologii:**
- React 19 + TypeScript, construit cu Vite
- `react-router-dom` pentru rute
- `@stomp/stompjs` pentru actualizările live prin WebSocket
- nginx în imaginea Docker

## Comenzi

Toate se rulează din folderul `frontend/`, cu Node 24 LTS (vezi `.nvmrc`):

```bash
npm ci            # instalează exact versiunile din package-lock.json
npm run dev       # http://localhost:5173 (pornește întâi backend-ul cu docker compose)
npm run build     # verificare TypeScript + build de producție în dist/
npm run lint      # oxlint
```

În Docker (din rădăcina repo-ului): `docker compose up -d --build frontend`, apoi deschide <http://localhost:3000>.

## Reguli

- **Doar URL-uri relative** (`/api/...`, `/ws`). În dezvoltare, Vite le trimite la `http://localhost:8080` (`vite.config.ts`); în Docker, nginx le trimite la `api-gateway:8080` (`nginx.conf`).
- **Contractele** endpoint-urilor și ale evenimentelor sunt în [../docs/api-contracts.md](../docs/api-contracts.md).
- **Cronometrul** licitației se calculează din `endTime` plus offset-ul față de `serverTime`, niciodată din ceasul brut al clientului.

## Structură

| Cale | Conținut |
|---|---|
| `src/main.tsx` | Punctul de intrare (`BrowserRouter`) |
| `src/App.tsx` | Rutele: `/`, `/login`, `/register`, `/auctions/:id`, `/auctions/new`, `/wallet` |
| `src/components/` | `Layout` (meniu), `Placeholder` (temporar) |
| `src/pages/` | O pagină per rută; acum sunt doar schelete marcate „TODO (A)” |
| `src/api/` | Clientul HTTP și clientul STOMP (de implementat în S1–S3) |
