# Abstract {-}

This report presents the design of Live Auction App, a real-time auction web platform that uses virtual coins. It was built for the course Software Project for Telecommunications. Users register, receive an initial balance, create auctions and bid. Everyone following an auction sees new bids and the countdown instantly.

Funds are reserved when a user bids and released when someone outbids them. A bid placed in the last 30 seconds extends the auction. When the auction ends, the winner is charged and the seller is credited automatically.

The architecture consists of five Spring Boot 4 microservices:
- an API gateway that validates user identity;
- services for users and wallets, auctions, bids, and WebSocket notifications.

The services communicate over REST, and each one stores its data in its own MySQL schema. Concurrent bids stay correct thanks to a pessimistic lock on the state of each auction, database integrity constraints and idempotent financial operations.

The application runs in Docker containers orchestrated with Docker Compose. GitHub Actions provides continuous integration, and deployment to a cloud virtual machine is planned.

The team of five students follows Scrum with two-week sprints. Each member has a coordination role (Project Manager, Technical Lead, Scrum Master, Product Owner, DevOps Engineer) and owns one component of the application.

The report covers:
- the application;
- the development methodology;
- the team roles;
- the architecture;
- the use case and class diagrams;
- the database structure;
- the infrastructure;
- security;
- the implementation plan.
