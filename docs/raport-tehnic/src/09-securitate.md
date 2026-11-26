<!-- Responsabil: D. -->

# Securitate

Capitolul descrie **modelul de securitate proiectat** pentru aplicație. La data predării, o parte din măsuri sunt deja în cod, iar restul sunt planificate pe sprinturi; situația exactă este în secțiunea „Stadiul implementării” de la finalul capitolului.

## Autentificare

**Înregistrarea:** user-service salvează parola doar ca **hash BCrypt**, niciodată în clar.

**Autentificarea:**
- user-service verifică parola și emite un **JSON Web Token** [7], semnat cu algoritmul HS256 și valabil 60 de minute.
- Tokenul conține identificatorul utilizatorului (`sub`), numele de utilizator și rolurile.
- Front-end-ul trimite tokenul în header-ul `Authorization: Bearer …` la fiecare cerere protejată.

![Autentificarea și propagarea identității prin gateway](../../diagrams/png/sequence-login.png)

## Autorizare și propagarea identității

**api-gateway este singurul punct de intrare** și validează tokenul pentru tot traficul HTTP:
- **Rute publice:** autentificarea, citirea licitațiilor și a istoricului de oferte, conexiunea WebSocket, starea aplicației. Funcționează și fără token.
- **Rute protejate:** orice altă rută `/api/**` fără token valid primește **401**, cu un răspuns în format RFC 9457 [8].

**Propagarea identității:**
1. Gateway-ul **șterge** header-ele `X-User-Id`, `X-User-Name` și `X-Internal-Key` trimise de client. Astfel, nimeni nu se poate da drept alt utilizator.
2. Apoi adaugă `X-User-Id` și `X-User-Name` din tokenul validat.
3. Serviciile din spatele gateway-ului folosesc aceste header-e și nu mai parsează tokenul (ADR-002).

## API-ul intern

**Protecția căilor `/internal/**`:**
- nu sunt rutate de gateway, deci primesc 404 din exterior;
- cer header-ul `X-Internal-Key`, cu o cheie secretă partajată de servicii.

**În producție:** porturile serviciilor nu sunt publicate. Ele sunt accesibile doar în rețeaua internă Docker.

## Comunicarea WebSocket

Gateway-ul doar transmite conexiunea WebSocket, deci notification-service validează el însuși tokenul trimis în cadrul STOMP `CONNECT`:
- **cu token valid:** numele conexiunii devine identificatorul utilizatorului, iar coada privată de notificări devine disponibilă;
- **fără token:** conexiunea se poate abona doar la topicurile publice ale licitațiilor;
- **origini acceptate:** conexiunile sunt acceptate doar de la originile configurate.

## Protecția datelor și a fișierelor

- **Validare:** fiecare cerere este validată (Bean Validation). Erorile au un format uniform, cu un cod stabil (de exemplu `BID_TOO_LOW`), fără detalii interne.
- **Fotografii:**
  - se acceptă doar tipurile jpeg, png și webp, de maximum 5 MB și cel mult 5 per licitație;
  - fișierele se salvează sub nume UUID aleatoare, niciodată sub numele trimis de client, ceea ce previne atacurile prin căi de fișier.
- **CORS:** se configurează doar la gateway, pentru originile front-end-ului.
- **Secrete:** cheia JWT, cheia internă și parolele bazei de date vin din variabile de mediu; fișierul `.env` nu intră în depozit.
- **Baza de date:** fiecare serviciu are un utilizator MySQL cu drepturi doar pe schema proprie.

## Stadiul implementării

Tabelul: Stadiul măsurilor de securitate la 26.11.2026

| Măsură | Stadiu | Responsabil, sarcină |
|---|---|---|
| Secretele (cheia JWT, cheia internă, parolele bazei de date) vin din variabile de mediu; `.env` nu intră în depozit | implementat | R, S0 |
| Câte un utilizator MySQL cu drepturi doar pe schema proprie | implementat (`db/init/01-init.sh`) | R, S0 |
| Căile `/internal/**` nu sunt rutate de gateway (404 din exterior) | implementat (rutele gateway-ului) | D, S0 |
| CORS configurat doar la gateway, pentru originile front-end-ului | implementat | D, S0 |
| Originile acceptate pentru conexiunea WebSocket | implementat | R, S0 |
| Hash BCrypt pentru parole | parțial: encoder-ul BCrypt este configurat, înregistrarea urmează | D, D-S1-02 |
| Emiterea JWT HS256 la autentificare | proiectat | D, D-S1-03 |
| Validarea JWT la gateway, rutele publice, 401 în format RFC 9457 | proiectat; deocamdată gateway-ul permite toate cererile | D, D-S1-05 |
| Ștergerea și propagarea header-elor de identitate | proiectat | D, D-S1-06 |
| Verificarea `X-Internal-Key` pe `/internal/**` | proiectat; cheia este deja configurată în toate serviciile | D, D-S2-03 și proprietarii serviciilor |
| Validarea JWT din cadrul STOMP `CONNECT` | proiectat | R, S2 |
| Validarea cererilor și erorile uniforme cu cod stabil | proiectat | fiecare proprietar de serviciu, S1–S2 |
| Validarea și denumirea UUID a fotografiilor | proiectat | K, S2 |
| Porturi nepublicate și HTTPS în producție | proiectat (`docker-compose.prod.yml`) | R, S3–S4 |

Măsurile marcate „proiectat” sunt descrise în sarcinile din ghidurile membrilor (`docs/team/`) și au câte un issue pe GitHub. Capitolul se actualizează la fiecare sprint review.

## Riscuri de securitate și măsuri

Tabelul de mai jos leagă riscurile OWASP de măsurile proiectate. Stadiul fiecărei măsuri este cel din tabelul anterior.

Tabelul: Riscuri de securitate (după OWASP Top 10) și măsurile proiectate

| Risc [9] | Măsură |
|---|---|
| Control de acces defectuos | validarea JWT la gateway; identitatea vine doar din token; vânzătorul nu își poate licita propria licitație; doar vânzătorul își modifică licitația |
| Defecte criptografice | BCrypt pentru parole; secret JWT de cel puțin 32 de octeți; HTTPS în producție |
| Injecție | interogări parametrizate prin JPA; validarea tuturor datelor de intrare |
| Design nesigur | rezervarea fondurilor și lock-urile împiedică cheltuirea dublă; operațiile financiare sunt idempotente |
| Configurare greșită | nimic publicat în producție în afară de front-end; Swagger UI doar în dezvoltare |
| Identificare și autentificare | mesaj identic pentru utilizator inexistent și parolă greșită; tokenuri cu expirare |
| Componente vulnerabile | versiuni actuale (Spring Boot 4.1.2, Java 21); actualizări prin pull request-uri verificate în CI |

**Limitări acceptate:**
- tokenul nu poate fi revocat înainte de expirare;
- secretul JWT este partajat între servicii.

O evoluție posibilă este semnarea cu RS256 și publicarea cheii publice (JWKS), plus tokenuri de reîmprospătare.
