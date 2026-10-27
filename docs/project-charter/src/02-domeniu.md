# Domeniul proiectului

## Ce include proiectul

**Conturi și portofel**
- Înregistrare și autentificare cu JWT.
- Portofel de monede virtuale, cu 1000 de monede bonus la înregistrare și alimentare demo.
- Istoricul tranzacțiilor.

**Licitații**
- Creare licitație cu titlu, descriere, până la 5 fotografii, preț de pornire, increment minim, dată de început și de sfârșit.
- Răsfoirea licitațiilor programate, active și încheiate, cu paginare.
- Pagina unei licitații, cu istoricul ofertelor.

**Licitare și finalizare**
- Licitare live: prețul, istoricul și cronometrul se actualizează pentru toți cei care urmăresc licitația.
- Fondurile se rezervă la licitare și se eliberează la depășire. Utilizatorul depășit primește o notificare.
- **Anti-sniping:** o ofertă din ultimele 30 de secunde prelungește licitația cu 30 de secunde.
- **Închidere automată:** câștigătorul plătește, vânzătorul încasează, iar ambii primesc o notificare.

**Livrabile tehnice**
- Arhitectură cu microservicii, containere Docker, Docker Compose, CI/CD și implementare în cloud.
- Documentație: arhitectură, contracte API, bază de date, decizii de arhitectură, diagrame UML, Raport Tehnic, ghidurile membrilor.

## Ce nu include proiectul

- Plăți cu bani reali, facturare, verificarea identității (KYC).
- Aplicație mobilă nativă. Interfața web este responsive.
- Funcții de comunitate: chat între utilizatori, recenzii, recomandări.
- Administrare și moderare avansată a conținutului.
- Notificări prin email sau SMS.
- Disponibilitate ridicată și scalare orizontală (mai multe instanțe ale aceluiași serviciu).
- Internaționalizare: interfața este în limba română.

Cererile noi intră în backlog-ul gestionat de Product Owner (A). Ele se prioritizează la sprint planning și nu modifică angajamentele sprintului în curs.

## Cerințe de nivel înalt

Tabelul: Cerințele obligatorii ale disciplinei și modul în care sunt acoperite

| Cerința disciplinei | Cum o acoperim |
|---|---|
| Cel puțin 2 microservicii Spring Boot | 5 servicii: api-gateway, user-service, auction-service, bidding-service, notification-service (Spring Boot 4.1, Java 21) |
| Comunicare REST între microservicii | API intern `/internal/**` (rezervări, decontări, actualizarea licitației, evenimente), protejat cu cheie internă |
| Bază de date SQL | MySQL 8.4, câte o schemă per serviciu (`user_db`, `auction_db`, `bidding_db`), migrații Flyway |
| Docker și Docker Compose | Dockerfile multi-stage per serviciu, `docker-compose.yml` cu healthcheck-uri; fișiere separate pentru dezvoltare și producție |
| Implementare în cloud | mașină virtuală în cloud, imagini în GitHub Container Registry, livrare automată prin GitHub Actions |
| Testare cu Postman sau front-end | colecție Postman cu aserțiuni (rulată și în CI cu Newman), plus front-end React |
| Diagrame UML de clase și use case | diagramele de clase (de ansamblu și per serviciu) și diagrama use case; în plus: componente, implementare, secvență, activitate, stări |
| Raport Tehnic: Proiectare (30.11.2026) | structura bazei de date și modelarea arhitecturii, generat în formatul șablonului UNITBV |

**Cerințe de calitate:**
- **Timp real:** o ofertă nouă apare la ceilalți utilizatori în cel mult o secundă.
- **Corectitudinea banilor:**
  - nicio ofertă acceptată nu poate depăși fondurile disponibile;
  - ofertele simultane produc un singur lider;
  - decontarea se execută o singură dată.
- **Securitate:**
  - parolele se salvează ca hash BCrypt;
  - accesul la funcțiile protejate se face cu token JWT;
  - endpoint-urile interne nu sunt accesibile din exterior;
  - secretele nu ajung în depozitul de cod.
- **Portabilitate:** aplicația pornește cu o singură comandă pe Windows, Linux și macOS.

## Livrabile

Tabelul: Livrabilele proiectului

| Livrabil | Responsabil | Termen |
|---|---|---|
| Depozitul GitHub, scheletul aplicației, ghidurile membrilor | D, R | 08.11.2026 (S0) |
| Prezentarea temei și a rolurilor (Ședința 3) | D | 02/09.11.2026 |
| Înregistrarea temei în tabelul coordonatorului | D | 09.11.2026 |
| Diagrama use case și diagrama de clase (Ședințele 4–5) | A, M | S1 |
| Raport Tehnic: Proiectare | D (asamblare), toți membrii | 30.11.2026 (intern 27.11) |
| Fluxurile de bază integrate în Docker Compose | toți | 06.12.2026 (S2) |
| MVP complet, colecție Postman finalizată | toți | 20.12.2026 (S3) |
| Prezentarea stadiului proiectului (Ședințele 6–7) | D, toți | S3 |
| Implementare în cloud, livrare automată | R | 17.01.2027 (S4) |
| Prezentarea finală și demonstrația | D, toți | data stabilită de coordonator |
