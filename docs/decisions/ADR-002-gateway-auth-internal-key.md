# ADR-002: Autentificare la gateway + cheie internă între servicii

- **Status:** Propus
- **Data:** 27.10.2026
- **Proprietar:** D (finalizează în S1, odată cu filtrul JWT din gateway)
- **Aprobat de:** M

## Context

**Cerințe:**
- Toate cererile din browser trec prin api-gateway.
- Serviciile trebuie să știe **cine** face cererea (userId, username).
- Endpoint-urile `/internal/**` trebuie să fie apelabile doar de celelalte servicii.
- Echipa are 5 membri cu experiență diferită în Spring Security, iar Spring Boot 4 / Security 7 diferă de tutorialele pentru Boot 3.

## Opțiuni analizate

1. **Gateway-ul validează JWT-ul și propagă identitatea prin header-e** (`X-User-Id`, `X-User-Name`). Serviciile au încredere în header-e. Apelurile interne folosesc o cheie partajată (`X-Internal-Key`).
   - (+) Un singur loc de configurat și de testat pentru securitate.
   - (+) Serviciile rămân simple: citesc un header.
   - (−) Serviciile nu trebuie expuse direct în producție, pentru că oricine le-ar putea trimite header-e false. Asta se rezolvă cu porturi nepublicate și cu ștergerea header-elor la gateway.
2. **Fiecare serviciu validează JWT-ul** (resource server peste tot).
   - (+) Apărare în profunzime.
   - (−) Configurație de securitate duplicată de 4 ori, mai multe locuri pentru greșeli și secretul JWT distribuit peste tot.
3. **mTLS / service mesh între servicii.**
   - (+) Identitate criptografică a serviciilor.
   - (−) Mult prea complex pentru proiect.

## Decizie (propusă)

**Opțiunea 1:**

- **Gateway-ul:**
  - folosește `oauth2ResourceServer` reactiv, cu decodor HS256;
  - **șterge** header-ele `X-User-Id`, `X-User-Name` și `X-Internal-Key` venite de la client, apoi adaugă `X-User-Id` / `X-User-Name` din token;
  - nu are rută pentru `/internal/**`.
- **Excepția WebSocket:** notification-service validează JWT-ul din cadrul STOMP `CONNECT`, pentru că gateway-ul doar face proxy pe conexiunea WebSocket.
- **Token expirat pe o rută publică:** cererea trece **ca anonimă**, fără header-ele de identitate. Navigarea nu se blochează, iar front-end-ul cere re-autentificare doar pe acțiunile protejate. D confirmă această regulă în S1 și testează ambele cazuri.

## Consecințe

- **Producție:** se publică doar front-end-ul și gateway-ul (`docker-compose.prod.yml`). `INTERNAL_API_KEY` și `JWT_SECRET` sunt secrete diferite de valorile de dezvoltare.
- **Testare:** testele serviciilor trimit direct header-ul `X-User-Id`. Colecția Postman are un folder pentru apeluri directe pe porturile 8081–8084.
- **Limitare:** nu există revocare de token (logout = ștergerea tokenului din client). Evoluție posibilă: RS256 + JWKS și refresh tokens.
