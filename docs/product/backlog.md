# Product backlog

Responsabil: **A** (Product Owner). A ține backlog-ul la zi, stabilește prioritățile la fiecare sprint planning și acceptă poveștile la sprint review.

**Prioritate MoSCoW:**
- **Must:** fără ea nu avem MVP-ul.
- **Should:** importantă, dar MVP-ul funcționează și fără.
- **Could:** dacă rămâne timp.
- **Won't:** nu în acest proiect.

Fiecare poveste are un issue GitHub `[US-nn] …` cu eticheta `type:story`. Task-urile tehnice din ghidurile membrilor trimit la aceste povești.

**MVP-ul pentru demo:**
- înregistrare și autentificare;
- creare licitație;
- licitare live între două browsere;
- anti-sniping;
- închidere automată cu plata câștigătorului și încasarea vânzătorului.

### US-01 · Înregistrare cont
**Prioritate:** Must · **Sprint țintă:** S1 · **Componente:** frontend, user-service

**Ca** vizitator, **vreau** să-mi creez un cont, **pentru ca** să pot vinde și licita.

**Criterii de acceptanță**
- **Date valide:** **Dat fiind** că username-ul și emailul nu sunt folosite, **când** trimit formularul de înregistrare, **atunci** contul e creat, portofelul primește 1000 de monede (tranzacție `SIGNUP_BONUS`) și sunt dus la autentificare.
- **Username ocupat:** **Dat fiind** că username-ul există deja, **când** trimit formularul, **atunci** văd mesajul „Username-ul este deja folosit”, iar contul nu se creează.
- **Date invalide:** **Dat fiind** un username cu spații sau o parolă sub 8 caractere, **când** trimit formularul, **atunci** văd eroarea lângă câmpul greșit.

### US-02 · Autentificare
**Prioritate:** Must · **Sprint țintă:** S1 · **Componente:** frontend, user-service, api-gateway

**Ca** utilizator înregistrat, **vreau** să mă autentific cu username-ul sau emailul, **pentru ca** să pot folosi funcțiile protejate.

**Criterii de acceptanță**
- **Credențiale corecte:** **Dat fiind** un cont existent, **când** introduc datele corecte, **atunci** sunt autentificat, văd numele meu în meniu și pot deschide pagina Portofel.
- **Credențiale greșite:** **Dat fiind** o parolă greșită, **când** încerc să mă autentific, **atunci** văd „Date de autentificare incorecte”, fără să aflu dacă username-ul există.
- **Token expirat:** **Dat fiind** că sesiunea mea a expirat (60 de minute), **când** fac o acțiune protejată, **atunci** sunt trimis la autentificare, iar după login revin la pagina în care eram.

### US-03 · Răsfoire licitații
**Prioritate:** Must · **Sprint țintă:** S2 · **Componente:** frontend, auction-service

**Ca** vizitator, **vreau** să văd licitațiile programate, active și încheiate, **pentru ca** să găsesc ce mă interesează.

**Criterii de acceptanță**
- **Licitații active:** **Dat fiind** că există licitații active, **când** deschid pagina principală, **atunci** văd tab-ul „Active”, cu fotografia principală, titlul, prețul curent, numărul de oferte și timpul rămas.
- **Paginare:** **Dat fiind** că există peste 12 licitații într-un tab, **când** apăs „Pagina următoare”, **atunci** văd următoarele licitații.
- **Listă goală:** **Dat fiind** că nu există licitații într-un tab, **când** îl deschid, **atunci** văd un mesaj clar, nu o pagină goală.

### US-04 · Detalii licitație
**Prioritate:** Must · **Sprint țintă:** S2 · **Componente:** frontend, auction-service, bidding-service

**Ca** vizitator, **vreau** să văd toate detaliile unei licitații, **pentru ca** să decid dacă licitez.

**Criterii de acceptanță**
- **Detalii:** **Dat fiind** o licitație existentă, **când** o deschid, **atunci** văd fotografiile, descrierea, prețul de pornire, incrementul minim, prețul curent, timpul rămas și istoricul ofertelor (cele mai noi primele).
- **Licitație inexistentă:** **Dat fiind** un id inexistent, **când** deschid adresa, **atunci** văd „Licitația nu există”.

### US-05 · Creare licitație
**Prioritate:** Must · **Sprint țintă:** S2 · **Componente:** frontend, auction-service

**Ca** utilizator autentificat, **vreau** să creez o licitație, **pentru ca** să vând un obiect.

**Criterii de acceptanță**
- **Date valide:** **Dat fiind** titlu, descriere, preț de pornire, increment, început și sfârșit valide, **când** salvez, **atunci** licitația apare ca „Programată” (sau „Activă” dacă începe acum) și sunt dus la pagina ei.
- **Interval invalid:** **Dat fiind** că sfârșitul este înaintea începutului sau durata depășește 7 zile, **când** salvez, **atunci** văd eroarea și licitația nu se creează.

### US-06 · Fotografii pentru licitație
**Prioritate:** Should · **Sprint țintă:** S2 · **Componente:** frontend, auction-service

**Ca** vânzător, **vreau** să adaug până la 5 fotografii, **pentru ca** obiectul să fie atractiv.

**Criterii de acceptanță**
- **Fotografii valide:** **Dat fiind** fișiere jpeg, png sau webp de maximum 5 MB, **când** le încarc, **atunci** le văd în pagina licitației, iar prima devine fotografia principală.
- **Fișier respins:** **Dat fiind** un fișier PDF, un fișier mai mare de 5 MB sau a 6-a fotografie, **când** încerc să-l încarc, **atunci** văd motivul refuzului.
- **Alt utilizator:** **Dat fiind** că nu sunt vânzătorul, **când** încerc să încarc fotografii, **atunci** cererea este refuzată (403).

### US-07 · Plasare ofertă
**Prioritate:** Must · **Sprint țintă:** S2 · **Componente:** frontend, bidding-service, auction-service, user-service

**Ca** licitant, **vreau** să plasez o ofertă, **pentru ca** să câștig obiectul.

**Criterii de acceptanță**
- **Ofertă validă:** **Dat fiind** o licitație activă și fonduri suficiente, **când** ofer cel puțin minimul sugerat, **atunci** devin lider, iar prețul curent și istoricul se actualizează.
- **Ofertă prea mică:** **Dat fiind** o sumă sub minim (prețul curent + increment), **când** trimit oferta, **atunci** văd „Oferta minimă este X monede”.
- **Propria licitație:** **Dat fiind** că sunt vânzătorul, **când** încerc să licitez, **atunci** văd „Nu poți licita la propria licitație”.
- **Licitație inactivă:** **Dat fiind** o licitație programată sau încheiată, **când** încerc să licitez, **atunci** oferta este refuzată.

### US-08 · Rezervarea și eliberarea fondurilor
**Prioritate:** Must · **Sprint țintă:** S2 · **Componente:** user-service, bidding-service, frontend

**Ca** licitant, **vreau** ca banii pentru oferta mea să fie rezervați și eliberați automat când sunt depășit, **pentru ca** să nu pot promite bani pe care nu îi am și să nu-mi rămână blocați.

**Criterii de acceptanță**
- **Rezervare:** **Dat fiind** 1000 de monede disponibile, **când** ofer 300, **atunci** portofelul arată sold 1000, rezervat 300, disponibil 700.
- **Eliberare:** **Dat fiind** că am oferta maximă, de 300, **când** alt licitant oferă 320, **atunci** rezervarea mea de 300 se eliberează.
- **Fonduri insuficiente:** **Dat fiind** 200 de monede disponibile, **când** ofer 300, **atunci** văd „Fonduri insuficiente”, iar oferta nu se plasează.
- **Propria ofertă mărită:** **Dat fiind** că sunt lider cu 300, **când** ofer 350, **atunci** rezervarea mea devine 350, nu 650.

### US-09 · Licitație live
**Prioritate:** Must · **Sprint țintă:** S3 · **Componente:** frontend, notification-service, bidding-service

**Ca** vizitator care urmărește o licitație, **vreau** să văd ofertele noi și cronometrul fără refresh, **pentru ca** să pot reacționa la timp.

**Criterii de acceptanță**
- **Ofertă nouă:** **Dat fiind** două browsere deschise pe aceeași licitație, **când** în primul se plasează o ofertă, **atunci** în al doilea prețul, istoricul și numărul de oferte se actualizează în cel mult 1 secundă.
- **Ceas decalat:** **Dat fiind** că ceasul calculatorului meu e decalat cu 2 minute, **când** urmăresc licitația, **atunci** cronometrul arată timpul corect (sincronizat cu `serverTime`).
- **Încheiere:** **Dat fiind** că licitația se încheie, **când** timpul expiră, **atunci** văd „Licitație încheiată” și câștigătorul, fără refresh.

### US-10 · Notificare „Ai fost depășit”
**Prioritate:** Should · **Sprint țintă:** S3 · **Componente:** frontend, notification-service, bidding-service

**Ca** licitant, **vreau** să fiu anunțat când cineva îmi depășește oferta, **pentru ca** să pot licita din nou.

**Criterii de acceptanță**
- **Depășire:** **Dat fiind** că sunt lider și sunt autentificat în aplicație, **când** alt utilizator oferă mai mult, **atunci** primesc o notificare cu titlul licitației, suma mea și suma nouă, chiar dacă sunt pe altă pagină.
- **Notificări private:** **Dat fiind** că nu sunt autentificat, **când** urmăresc o licitație, **atunci** nu primesc notificările private ale altora.

### US-11 · Anti-sniping
**Prioritate:** Must · **Sprint țintă:** S3 · **Componente:** auction-service, bidding-service, frontend

**Ca** licitant, **vreau** ca o ofertă din ultimele 30 de secunde să prelungească licitația, **pentru ca** să am timp să răspund.

**Criterii de acceptanță**
- **Prelungire:** **Dat fiind** că mai sunt 10 secunde, **când** cineva plasează o ofertă validă, **atunci** sfârșitul se mută cu 30 de secunde mai târziu și toți văd noul cronometru.
- **Fără prelungire:** **Dat fiind** că mai sunt 5 minute, **când** cineva licitează, **atunci** sfârșitul rămâne neschimbat.

### US-12 · Închidere automată și decontare
**Prioritate:** Must · **Sprint țintă:** S3 · **Componente:** auction-service, user-service, notification-service

**Ca** vânzător, **vreau** ca licitația să se încheie automat și să primesc banii, **pentru ca** tranzacția să fie corectă fără intervenție manuală.

**Criterii de acceptanță**
- **Cu oferte:** **Dat fiind** o licitație activă cu oferte, **când** expiră timpul, **atunci**:
  - starea devine „Încheiată”;
  - câștigătorului i se scade suma (tranzacție `PAYMENT`);
  - vânzătorul primește suma (tranzacție `PAYOUT`);
  - toate celelalte rezervări ale licitației se eliberează.
- **Fără oferte:** **Dat fiind** o licitație fără oferte, **când** expiră timpul, **atunci** se încheie fără câștigător și fără mișcări de bani.
- **Repornire:** **Dat fiind** că user-service era oprit la închidere, **când** repornește, **atunci** decontarea se face o singură dată, automat.

### US-13 · Portofel
**Prioritate:** Must · **Sprint țintă:** S2 · **Componente:** frontend, user-service

**Ca** utilizator autentificat, **vreau** să-mi văd soldul și istoricul tranzacțiilor, **pentru ca** să știu câți bani am disponibili.

**Criterii de acceptanță**
- **Sold:** **Dat fiind** un portofel cu rezervări, **când** deschid pagina Portofel, **atunci** văd soldul, suma rezervată și suma disponibilă.
- **Istoric:** **Dat fiind** mai multe tranzacții, **când** derulez istoricul, **atunci** le văd paginat, cele mai noi primele, cu tipul, suma, licitația și data.

### US-14 · Alimentare demo
**Prioritate:** Should · **Sprint țintă:** S2 · **Componente:** frontend, user-service

**Ca** utilizator, **vreau** să-mi alimentez portofelul cu monede demo, **pentru ca** să pot continua să testez aplicația.

**Criterii de acceptanță**
- **Sumă validă:** **Dat fiind** o sumă între 1 și 10000, **când** confirm alimentarea, **atunci** soldul crește și apare o tranzacție `TOP_UP`.
- **Sumă invalidă:** **Dat fiind** o sumă de 0 sau peste 10000, **când** confirm, **atunci** văd eroarea.

### US-15 · Licitațiile și ofertele mele
**Prioritate:** Should · **Sprint țintă:** S3 · **Componente:** frontend, auction-service, bidding-service

**Ca** utilizator autentificat, **vreau** să văd licitațiile create de mine și ofertele mele, **pentru ca** să le urmăresc ușor.

**Criterii de acceptanță**
- **Licitațiile mele:** **Dat fiind** că am creat licitații, **când** deschid „Licitațiile mele”, **atunci** le văd pe toate, cu starea lor.
- **Ofertele mele:** **Dat fiind** că am licitat, **când** deschid „Ofertele mele”, **atunci** văd ofertele, cu suma și licitația.

### US-16 · Notificări de câștig și de vânzare
**Prioritate:** Should · **Sprint țintă:** S3 · **Componente:** frontend, notification-service, auction-service

**Ca** câștigător sau vânzător, **vreau** să fiu anunțat la încheierea licitației, **pentru ca** să știu rezultatul imediat.

**Criterii de acceptanță**
- **Câștigător:** **Dat fiind** că am oferta maximă la final, **când** licitația se încheie, **atunci** primesc „Ai câștigat <titlu> cu X monede”.
- **Vânzător:** **Dat fiind** că sunt vânzătorul, **când** licitația se încheie cu oferte, **atunci** primesc „<titlu> s-a vândut cu X monede”.

### US-17 · Editare profil
**Prioritate:** Could · **Sprint țintă:** S4 · **Componente:** frontend, user-service

**Ca** utilizator, **vreau** să-mi schimb numele afișat și emailul, **pentru ca** datele mele să fie corecte.

**Criterii de acceptanță**
- **Date valide:** **Dat fiind** date valide, **când** salvez profilul, **atunci** noile date apar în meniu și în profilul public.
- **Email ocupat:** **Dat fiind** un email folosit de alt cont, **când** salvez, **atunci** văd „Emailul este deja folosit”.

### US-18 · Anularea unei licitații programate
**Prioritate:** Could · **Sprint țintă:** S4 · **Componente:** frontend, auction-service

**Ca** vânzător, **vreau** să anulez o licitație care nu a început, **pentru ca** să corectez o greșeală.

**Criterii de acceptanță**
- **Licitație programată:** **Dat fiind** o licitație programată, **când** o anulez, **atunci** dispare din liste.
- **Licitație începută:** **Dat fiind** o licitație activă, **când** încerc să o anulez, **atunci** operația este refuzată.

### US-19 · Căutare după titlu
**Prioritate:** Could · **Sprint țintă:** S4 · **Componente:** frontend, auction-service

**Ca** vizitator, **vreau** să caut licitații după titlu, **pentru ca** să găsesc rapid un obiect.

**Criterii de acceptanță**
- **Rezultate:** **Dat fiind** licitații cu „camera” în titlu, **când** caut „camera”, **atunci** le văd doar pe acestea (fără diferențe între majuscule și minuscule).
