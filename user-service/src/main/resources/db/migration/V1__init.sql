-- user_db: users, wallets, reservations, transactions, settlements.
-- Owner: D (design reviewed by K, see docs/database/README.md). Editable until 30.11.2026, then only new V<n>__*.sql files.
-- Conventions: InnoDB, utf8mb4, BIGINT AUTO_INCREMENT ids, DATETIME(6) instants stored in UTC, coins as BIGINT.

CREATE TABLE users (
    id            BIGINT       NOT NULL AUTO_INCREMENT,
    username      VARCHAR(30)  NOT NULL,
    email         VARCHAR(254) NOT NULL,
    password_hash VARCHAR(100) NOT NULL,
    display_name  VARCHAR(60)  NOT NULL,
    role          VARCHAR(20)  NOT NULL DEFAULT 'USER',
    created_at    DATETIME(6)  NOT NULL,
    CONSTRAINT pk_users PRIMARY KEY (id),
    CONSTRAINT uq_users_username UNIQUE (username),
    CONSTRAINT uq_users_email UNIQUE (email),
    CONSTRAINT ck_users_role CHECK (role IN ('USER', 'ADMIN'))
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

CREATE TABLE wallets (
    id         BIGINT      NOT NULL AUTO_INCREMENT,
    user_id    BIGINT      NOT NULL,
    balance    BIGINT      NOT NULL DEFAULT 0,
    reserved   BIGINT      NOT NULL DEFAULT 0,
    version    BIGINT      NOT NULL DEFAULT 0,
    updated_at DATETIME(6) NOT NULL,
    CONSTRAINT pk_wallets PRIMARY KEY (id),
    CONSTRAINT uq_wallets_user UNIQUE (user_id),
    CONSTRAINT fk_wallets_user FOREIGN KEY (user_id) REFERENCES users (id),
    -- Wallet invariant: 0 <= reserved <= balance (available = balance - reserved).
    CONSTRAINT ck_wallets_reserved CHECK (reserved >= 0 AND reserved <= balance)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

CREATE TABLE wallet_reservations (
    id         BIGINT      NOT NULL AUTO_INCREMENT,
    wallet_id  BIGINT      NOT NULL,
    auction_id BIGINT      NOT NULL, -- logical reference to auction_db.auctions.id (no cross-schema FK)
    amount     BIGINT      NOT NULL,
    created_at DATETIME(6) NOT NULL,
    updated_at DATETIME(6) NOT NULL,
    CONSTRAINT pk_wallet_reservations PRIMARY KEY (id),
    CONSTRAINT uq_wallet_reservations_wallet_auction UNIQUE (wallet_id, auction_id),
    CONSTRAINT fk_wallet_reservations_wallet FOREIGN KEY (wallet_id) REFERENCES wallets (id),
    CONSTRAINT ck_wallet_reservations_amount CHECK (amount > 0),
    INDEX ix_wallet_reservations_auction (auction_id)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

CREATE TABLE wallet_transactions (
    id         BIGINT      NOT NULL AUTO_INCREMENT,
    wallet_id  BIGINT      NOT NULL,
    type       VARCHAR(20) NOT NULL,
    amount     BIGINT      NOT NULL, -- always positive; the type gives the direction (PAYMENT decreases the balance)
    auction_id BIGINT      NULL,     -- set for PAYMENT / PAYOUT
    created_at DATETIME(6) NOT NULL,
    CONSTRAINT pk_wallet_transactions PRIMARY KEY (id),
    CONSTRAINT fk_wallet_transactions_wallet FOREIGN KEY (wallet_id) REFERENCES wallets (id),
    CONSTRAINT ck_wallet_transactions_type CHECK (type IN ('SIGNUP_BONUS', 'TOP_UP', 'PAYMENT', 'PAYOUT')),
    CONSTRAINT ck_wallet_transactions_amount CHECK (amount > 0),
    INDEX ix_wallet_transactions_wallet_created (wallet_id, created_at)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- One row per settled auction: makes POST /internal/wallet/settlements idempotent.
CREATE TABLE wallet_settlements (
    auction_id BIGINT      NOT NULL,
    winner_id  BIGINT      NULL, -- NULL when the auction ended without bids
    seller_id  BIGINT      NOT NULL,
    amount     BIGINT      NULL,
    created_at DATETIME(6) NOT NULL,
    CONSTRAINT pk_wallet_settlements PRIMARY KEY (auction_id),
    CONSTRAINT fk_wallet_settlements_winner FOREIGN KEY (winner_id) REFERENCES users (id),
    CONSTRAINT fk_wallet_settlements_seller FOREIGN KEY (seller_id) REFERENCES users (id)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;
