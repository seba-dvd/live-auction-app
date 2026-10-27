# ADR-001: Concurența la plasarea ofertelor: `FOR UPDATE` vs. `@Version`

- **Status:** Propus
- **Data:** 27.10.2026
- **Proprietar:** M (finalizează în S2, după testul de concurență)
- **Aprobat de:** M

## Context

**Problema:** mai mulți utilizatori pot licita **în aceeași secundă** la aceeași licitație, mai ales în ultimele secunde, din cauza anti-sniping-ului. Fără control, două cereri citesc aceeași „ofertă maximă”, ambele trec validarea și ambele se salvează. Rezultatul este un **lost update**: doi lideri, două rezervări pentru aceeași poziție, istoric incorect.

**Constrângeri:**
- Validarea depinde de starea curentă (`highestAmount + minIncrement`).
- Plasarea ofertei implică apeluri către alte două servicii: rezervarea fondurilor în user-service și actualizarea licitației în auction-service.
- Sumele acceptate trebuie să crească strict, iar banii trebuie mutați o singură dată.

## Opțiuni analizate

1. **Lock pesimist (`SELECT … FOR UPDATE`, `@Lock(PESSIMISTIC_WRITE)`)** pe un rând per licitație (`auction_bid_state`), ținut pe toată durata validării, a rezervării și a actualizării licitației.
   - (+) Ordine strictă a ofertelor la aceeași licitație.
   - (+) Ușor de explicat și de testat.
   - (+) Ofertele la licitații diferite nu se blochează între ele.
   - (−) Cererile concurente așteaptă; timpul de așteptare include apelurile HTTP interne, maximum câteva sute de ms în condiții normale.
   - (−) Trebuie evitate apelurile lente cât timp se ține lock-ul (timeouts: read 5 s).
2. **Optimistic locking (`@Version`) + reîncercare.** Se citește starea fără lock, iar la scriere se verifică versiunea; la conflict (`OptimisticLockException`) se reia de la capăt.
   - (+) Fără așteptare la încărcare mică.
   - (−) Apelurile externe (rezervare, `bid-placed`) au loc **înainte** de detectarea conflictului, deci fiecare reîncercare cere compensări în alte servicii.
   - (−) Sub încărcare mare (finalul licitației), reîncercările se înmulțesc.
3. **Serializare printr-o coadă** (o licitație = un consumator).
   - (+) Ordine strictă fără lock-uri în baza de date.
   - (−) Cere un broker de mesaje și un răspuns asincron către client; prea complex pentru proiect.

## Decizie (propusă)

**Opțiunea 1:** lock pesimist pe `auction_bid_state`.

- **Ce ține lock-ul:** tot ce mișcă bani (rezervarea, `bid-placed`, eliberarea fostului lider) se execută cât timp se ține lock-ul.
- **Ce se face după commit:** doar notificările.
- **Prima ofertă:** rândul de stare se creează idempotent, cu `INSERT IGNORE` într-o tranzacție separată, înaintea lock-ului. Astfel se evită deadlock-ul a două inserări concurente.

## Consecințe

- **Testul de concurență (M, S3, Testcontainers MySQL):** 50 de oferte paralele la aceeași licitație trebuie să ducă la exact un lider, sume acceptate strict crescătoare și niciun lost update. Rezultatul confirmă sau infirmă decizia.
- **Plasă de siguranță:** constrângerea `UQ (auction_id, amount)` din `bids` face un eventual bug vizibil imediat.
- **Lock-uri secundare:** auction-service blochează și el rândul `auctions` în `bid-placed`, iar user-service blochează portofelul la rezervare. Ordinea lock-urilor este mereu bidding → auction → user, deci nu apar cicluri.
- **Limitare acceptată:** un eșec la commit după apelurile externe lasă o rezervare neeliberată până la decontare. Evoluția este un transactional outbox / saga (vezi [architecture.md §10](../architecture.md#10-limitări-cunoscute-și-evoluții)).
