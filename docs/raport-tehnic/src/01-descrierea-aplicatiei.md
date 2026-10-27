<!-- Responsabil: A (Product Owner). Draft v0.1 generat la bootstrap: verifică, completează, actualizează. -->

# Descrierea aplicației

## Context și motivație

Licitațiile online sunt un mecanism de vânzare în care prețul se formează prin concurența dintre cumpărători. Pe platformele clasice, licitația se încheie la o oră fixă. Asta încurajează practica numită „sniping”: o ofertă plasată în ultimele secunde, care nu le mai lasă celorlalți participanți timp să răspundă. Unele platforme folosesc o închidere „soft”: orice ofertă din ultimul interval prelungește licitația.

**Live Auction App** este o platformă web de licitații în timp real. Toate operațiile financiare se fac cu **monede virtuale**:

- **Fără bani reali:** nu există plăți, facturi sau riscuri financiare.
- **Aceeași logică de business:**
  - fondurile se rezervă când licitezi și se eliberează când ești depășit;
  - câștigătorul plătește, iar vânzătorul încasează automat la final.
- **Timp real:** toți utilizatorii care urmăresc o licitație văd instantaneu fiecare ofertă nouă, istoricul și cronometrul.

**De ce această temă:** ea permite demonstrarea cerințelor disciplinei pe probleme tehnice reale:
- **concurența:** mai mulți utilizatori licitează în aceeași secundă;
- **consistența datelor:** datele sunt distribuite între mai multe microservicii;
- **comunicarea în timp real:** prin WebSocket;
- **corectitudinea timpului:** prelungirea anti-sniping și sincronizarea cronometrelor.

## Obiectivele proiectului

**Obiective funcționale:**
- O platformă în care orice utilizator înregistrat poate vinde și cumpăra prin licitație.
- Licitare live, cu actualizare instantanee pentru toți cei care urmăresc licitația.
- Mișcări de bani corecte: nicio ofertă acceptată nu depășește fondurile disponibile, iar decontarea se face o singură dată.

**Obiective tehnice și didactice:**
- Arhitectură cu microservicii Spring Boot care comunică prin REST.
- Bază de date relațională (MySQL), câte o schemă per serviciu.
- Containerizare cu Docker, orchestrare locală cu Docker Compose, implementare în cloud.
- Testare automată, colecție Postman și integrare continuă.

## Funcționalități principale

Tabelul: Funcționalitățile aplicației

| Funcționalitate | Descriere | Prioritate |
|---|---|---|
| Înregistrare și autentificare | cont nou cu 1000 de monede bonus; autentificare cu username sau email; token JWT valabil 60 de minute | Must |
| Portofel | sold, sumă rezervată, sumă disponibilă; istoricul tranzacțiilor; alimentare demo | Must |
| Creare licitație | titlu, descriere, până la 5 fotografii, preț de pornire, increment minim, început și sfârșit | Must |
| Răsfoire licitații | liste separate pentru licitațiile programate, active și încheiate, cu paginare | Must |
| Licitare live | ofertă minimă calculată automat; preț, istoric și cronometru actualizate fără reîncărcare | Must |
| Rezervarea fondurilor | oferta rezervă suma; depășirea o eliberează; oferta proprie mărită își actualizează rezervarea | Must |
| Anti-sniping | o ofertă în ultimele 30 de secunde prelungește licitația cu 30 de secunde | Must |
| Închidere automată | câștigătorul plătește, vânzătorul încasează, celelalte rezervări se eliberează | Must |
| Notificări | „Ai fost depășit”, „Ai câștigat”, „Licitația ta s-a vândut” | Should |
| Licitațiile și ofertele mele | listele personale ale utilizatorului | Should |

## Utilizatori și scenariu de utilizare

**Tipuri de utilizatori:**
- **Vizitatorul** (neautentificat) poate răsfoi licitațiile și le poate urmări live.
- **Utilizatorul autentificat** poate fi, în același timp, **vânzător** (își creează licitațiile) și **licitant** (licitează la licitațiile altora).
- **Planificatorul** este un actor de sistem: pornește și închide licitațiile la momentele stabilite.

**Scenariul de demonstrație** (două browsere):
1. Ana și Bogdan își creează conturi. Fiecare primește 1000 de monede.
2. Ana creează o licitație de 3 minute pentru un aparat foto, cu prețul de pornire 100.
3. Bogdan și un al treilea utilizator licitează alternativ. Prețul și istoricul se actualizează instantaneu în ambele browsere. Cel depășit primește notificarea „Ai fost depășit”, iar banii lui se eliberează.
4. Cu 10 secunde înainte de final, Bogdan licitează. Licitația se prelungește cu 30 de secunde, iar cronometrul se actualizează la toți.
5. La expirare, licitația se închide automat:
   - Bogdan plătește și primește „Ai câștigat”;
   - Ana încasează și primește „Licitația ta s-a vândut”;
   - istoricele tranzacțiilor arată plata și încasarea.

## Cerințe nefuncționale

Tabelul: Cerințele nefuncționale

| Categorie | Cerință |
|---|---|
| Performanță | o ofertă nouă apare la ceilalți utilizatori în cel mult o secundă |
| Corectitudine | ofertele simultane produc un singur lider; sumele acceptate cresc strict; decontarea este idempotentă |
| Timp | cronometrele se sincronizează cu ceasul serverului, nu cu cel al clientului |
| Securitate | parole doar ca hash BCrypt; funcții protejate cu JWT; API-ul intern inaccesibil din exterior; secrete doar în variabile de mediu |
| Portabilitate | întreaga aplicație pornește cu `docker compose up`, pe Windows, Linux și macOS |
| Mentenabilitate | contracte API documentate, teste automate, CI pe fiecare modificare, decizii documentate în ADR-uri |

## Cerințele disciplinei

Tabelul: Cerințele disciplinei și modul în care sunt acoperite

| Cerință | Soluție |
|---|---|
| Cel puțin două microservicii Spring Boot | cinci servicii: api-gateway, user-service, auction-service, bidding-service, notification-service |
| Comunicare REST între microservicii | API intern `/internal/**`, protejat cu cheie internă (capitolul 4) |
| Bază de date SQL | MySQL 8.4, câte o schemă per serviciu (capitolul 7) |
| Docker și Docker Compose | imagini multi-stage, Compose cu healthcheck-uri (capitolul 8) |
| Implementare în cloud | mașină virtuală, imagini în GHCR, livrare automată (capitolul 8) |
| Testare cu Postman sau front-end | colecție Postman cu aserțiuni și front-end React |
| Diagrame de clase și use case | capitolele 5 și 6 |
