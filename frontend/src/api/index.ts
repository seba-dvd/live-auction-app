// API module: TODO (A) S1, see docs/team/A.md and docs/api-contracts.md.
//
// Planned structure:
//   client.ts    - one fetch wrapper: adds "Authorization: Bearer <token>", sends/parses JSON,
//                  turns RFC 9457 ProblemDetail errors ({ status, detail, code }) into a typed ApiError
//   auth.ts      - register, login
//   auctions.ts  - list (paged), details, create, upload photos
//   bids.ts      - place bid, bid history
//   wallet.ts    - wallet, transactions, top-up
//   realtime.ts  - @stomp/stompjs Client for "/ws" (topic /topic/auctions/{id}, queue /user/queue/notifications)
//
// Always use relative URLs ("/api/...", "/ws"): Vite (dev) and nginx (Docker) proxy them to the api-gateway.
export {}
