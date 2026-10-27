-- bidding_db: bid history and the per-auction bidding state (lock target of the place-bid flow).
-- Owner: M (design reviewed by K). Editable until 30.11.2026, then only new V<n>__*.sql files.
-- auction_id and bidder_id are logical references to auction_db / user_db (no cross-schema FK).

CREATE TABLE bids (
    id              BIGINT      NOT NULL AUTO_INCREMENT,
    auction_id      BIGINT      NOT NULL,
    bidder_id       BIGINT      NOT NULL,
    bidder_username VARCHAR(30) NOT NULL, -- denormalized for the public bid history
    amount          BIGINT      NOT NULL,
    created_at      DATETIME(6) NOT NULL,
    CONSTRAINT pk_bids PRIMARY KEY (id),
    -- Accepted amounts strictly increase per auction: a duplicate amount means a lost-update bug.
    CONSTRAINT uq_bids_auction_amount UNIQUE (auction_id, amount),
    CONSTRAINT ck_bids_amount CHECK (amount > 0),
    INDEX ix_bids_auction_created (auction_id, created_at),
    INDEX ix_bids_bidder_created (bidder_id, created_at)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- One row per auction, locked with SELECT ... FOR UPDATE while a bid is processed.
-- Created (idempotently) before the first bid, hence the NULL leader columns.
CREATE TABLE auction_bid_state (
    auction_id        BIGINT      NOT NULL,
    highest_amount    BIGINT      NULL,
    highest_bidder_id BIGINT      NULL,
    bid_count         INT         NOT NULL DEFAULT 0,
    updated_at        DATETIME(6) NOT NULL,
    CONSTRAINT pk_auction_bid_state PRIMARY KEY (auction_id),
    CONSTRAINT ck_auction_bid_state_leader CHECK ((bid_count = 0 AND highest_amount IS NULL AND highest_bidder_id IS NULL)
        OR (bid_count > 0 AND highest_amount IS NOT NULL AND highest_bidder_id IS NOT NULL))
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;
