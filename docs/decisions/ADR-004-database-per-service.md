# ADR-004: Database-per-service pe o singură instanță MySQL

- **Status:** Propus
- **Data:** 27.10.2026
- **Proprietar:** K (finalizează în S1, odată cu designul bazei de date)
- **Aprobat de:** M

## Context

**Constrângeri:**
- Cursul cere o bază de date SQL și o arhitectură cu microservicii.
- Trei servicii au date persistente: user, auction și bidding.
- Laptopurile echipei au memorie limitată: Docker Desktop cu WSL2 și 5 servicii Java.
- Un singur mediu de cloud, ieftin (credite de student).

## Opțiuni analizate

1. **O schemă comună pentru toate serviciile.**
   - (+) Join-uri și chei străine între toate tabelele.
   - (−) Cuplare puternică: orice serviciu poate citi sau scrie datele altuia. Nu mai sunt microservicii reale.
2. **O instanță MySQL per serviciu.**
   - (+) Izolare completă.
   - (−) Aproximativ 3 × 400 MB RAM, trei volume, trei backup-uri. Prea scump pentru laptopuri și pentru VM-ul de cloud.
3. **O instanță MySQL, o schemă și un utilizator per serviciu.**
   - (+) Izolare logică garantată de drepturile MySQL.
   - (+) Un singur container de operat.
   - (+) Se poate trece oricând la opțiunea 2, schimbând doar URL-ul.

## Decizie (propusă)

**Opțiunea 3:**

- **Scheme și utilizatori:** `user_db`, `auction_db`, `bidding_db`, create de `db/init/01-init.sh`. Fiecare utilizator are `GRANT ALL` doar pe schema lui.
- **Fără chei străine între scheme:** identificatorii externi sunt referințe logice (`BIGINT`).
- **Migrații:** fiecare serviciu își migrează singur schema cu Flyway și o validează cu Hibernate (`ddl-auto: validate`).

## Consecințe

- **Fără join-uri între servicii.** Datele altor servicii se obțin prin API, iar unde e nevoie se denormalizează controlat (de exemplu `bids.bidder_username`).
- **Consistența între scheme** se asigură prin fluxuri: lock, idempotență, decontare cu reîncercare. Nu se folosesc tranzacții distribuite.
- **Instanță unică:** o singură instanță MySQL este un punct unic de defectare, acceptabil pentru proiect.
- **Raportul tehnic** (cap. 7) prezintă câte o diagramă ER per schemă, plus vederea de ansamblu cu referințele logice.
