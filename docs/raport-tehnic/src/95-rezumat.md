# Rezumat {-}

**Ce este proiectul.** Raportul prezintă proiectarea aplicației Live Auction App, o platformă web de licitații în timp real cu monede virtuale, realizată la disciplina Proiect de Software pentru Telecomunicații. Utilizatorii își creează conturi, primesc un sold inițial, creează licitații și licitează. Toți cei care urmăresc o licitație văd instantaneu ofertele noi și cronometrul.

**Cum se mișcă banii:**
- fondurile se rezervă la licitare și se eliberează la depășire;
- o ofertă în ultimele 30 de secunde prelungește licitația;
- la final, câștigătorul plătește, iar vânzătorul încasează automat.

**Arhitectura** are cinci microservicii Spring Boot 4:
- un API gateway, care validează identitatea utilizatorilor;
- serviciile pentru utilizatori și portofel, pentru licitații, pentru oferte și pentru notificări prin WebSocket.

Serviciile comunică prin REST. Fiecare își păstrează datele într-o schemă MySQL proprie.

**Corectitudinea ofertelor simultane** este asigurată de un lock pesimist pe starea fiecărei licitații, de constrângeri de integritate și de operații financiare idempotente.

**Infrastructura:** aplicația rulează în containere Docker, orchestrate cu Docker Compose, cu integrare continuă în GitHub Actions și cu implementare planificată pe o mașină virtuală în cloud.

**Metodologia:** echipa de cinci studenți lucrează după Scrum, în sprinturi de două săptămâni. Fiecare membru are un rol de coordonare (Project Manager, Technical Lead, Scrum Master, Product Owner, DevOps Engineer) și deține o componentă a aplicației.

**Conținutul raportului:**
- descrierea aplicației;
- metodologia;
- rolurile;
- arhitectura;
- diagramele de cazuri de utilizare și de clase;
- structura bazei de date;
- infrastructura;
- securitatea;
- planul de implementare.
