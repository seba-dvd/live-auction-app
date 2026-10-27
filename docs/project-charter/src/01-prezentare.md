# Prezentarea proiectului

## Informații generale

Tabelul: Date de identificare a proiectului

| Element | Valoare |
|---|---|
| Denumirea proiectului | Live Auction App: platformă de licitații live cu monede virtuale |
| Disciplina | Proiect de Software pentru Telecomunicații, anul IV, Facultatea de Inginerie Electrică și Știința Calculatoarelor, Universitatea Transilvania din Brașov |
| Coordonator (sponsor) | Ș.L. Dr. Ing. Horia Modran |
| Project Manager | Pilat David Sebastian (D) |
| Echipa | 5 membri: D (Project Manager), M (Technical Lead), K (Scrum Master), A (Product Owner), R (DevOps Engineer) |
| Perioada | 28.10.2026 – 17.01.2027 (prezentarea finală, la data stabilită de coordonator) |
| Metodologie | Agile / Scrum, sprinturi de două săptămâni |
| Depozit de cod | GitHub, privat: `seba-dvd/live-auction-app` |
| Versiunea cartei | 1.0, 27.10.2026 |

## Scop și justificare

**Scopul proiectului** este realizarea unei aplicații web de licitații în timp real:
- utilizatorii creează licitații și licitează cu monede virtuale;
- toți cei care urmăresc o licitație văd prețul, istoricul ofertelor și cronometrul actualizate instantaneu, fără reîncărcarea paginii;
- fondurile se rezervă la licitare, iar la final câștigătorul plătește și vânzătorul încasează automat.

**De ce o platformă de licitații live:** tema acoperă natural toate cerințele disciplinei:
- **microservicii Spring Boot:** utilizatori și portofel, licitații, oferte, notificări;
- **comunicare REST** între servicii;
- **bază de date relațională**, în care corectitudinea mișcărilor de bani contează;
- **containerizare** cu Docker și Docker Compose;
- **implementare în cloud**.

**Probleme tehnice reale, care pot fi demonstrate:**
- **concurența:** mai mulți utilizatori licitează în aceeași secundă;
- **consistența datelor între servicii:** rezervarea și eliberarea fondurilor;
- **comunicarea în timp real:** WebSocket/STOMP;
- **corectitudinea timpului:** prelungirea anti-sniping și sincronizarea cronometrelor.

**Monedele virtuale** elimină complexitatea și riscurile plăților reale, dar păstrează logica de business: rezervări, decontare, idempotență.

## Obiective

Tabelul: Obiectivele proiectului (SMART)

| Cod | Obiectiv | Indicator de realizare | Termen |
|---|---|---|---|
| O1 | Scheletul aplicației rulează integral pe calculatorul fiecărui membru | `docker compose up` pornește cele 5 servicii, baza de date și front-end-ul; CI verde | 08.11.2026 |
| O2 | Raportul Tehnic: Proiectare este predat complet | conține metodologia, rolurile, structura bazei de date, diagramele de clase și use case | 30.11.2026 |
| O3 | Fluxurile de bază funcționează integrat | înregistrare, autentificare, creare licitație, licitare cu rezervarea fondurilor, actualizare live | 06.12.2026 |
| O4 | MVP-ul complet poate fi demonstrat cu două browsere | anti-sniping, închidere automată, plata câștigătorului, încasarea vânzătorului, notificări „depășit” | 20.12.2026 |
| O5 | Calitatea fluxurilor critice este verificată automat | testul de concurență (ofertele paralele produc un singur lider), teste pentru decontarea idempotentă, colecția Postman cu aserțiuni rulată în CI | 20.12.2026 |
| O6 | Aplicația rulează în cloud, cu livrare automată | implementare publică, actualizată automat la push pe `main`, test de verificare după fiecare livrare | 17.01.2027 |
