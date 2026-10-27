-- auction_db: items, item photos, auctions.
-- Owner: K. Editable until 30.11.2026, then only new V<n>__*.sql files.
-- seller_id, highest_bidder_id, winner_id are logical references to user_db.users.id (no cross-schema FK).

CREATE TABLE items (
    id          BIGINT        NOT NULL AUTO_INCREMENT,
    seller_id   BIGINT        NOT NULL,
    title       VARCHAR(120)  NOT NULL,
    description VARCHAR(2000) NOT NULL,
    created_at  DATETIME(6)   NOT NULL,
    CONSTRAINT pk_items PRIMARY KEY (id),
    INDEX ix_items_seller (seller_id)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

CREATE TABLE item_photos (
    id       BIGINT      NOT NULL AUTO_INCREMENT,
    item_id  BIGINT      NOT NULL,
    filename VARCHAR(64) NOT NULL, -- random UUID + extension, never the client's file name
    position INT         NOT NULL, -- 0 = main photo, max 5 photos (0..4)
    CONSTRAINT pk_item_photos PRIMARY KEY (id),
    CONSTRAINT uq_item_photos_filename UNIQUE (filename),
    CONSTRAINT uq_item_photos_item_position UNIQUE (item_id, position),
    CONSTRAINT fk_item_photos_item FOREIGN KEY (item_id) REFERENCES items (id) ON DELETE CASCADE,
    CONSTRAINT ck_item_photos_position CHECK (position BETWEEN 0 AND 4)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

CREATE TABLE auctions (
    id                BIGINT      NOT NULL AUTO_INCREMENT,
    item_id           BIGINT      NOT NULL,
    seller_id         BIGINT      NOT NULL,
    starting_price    BIGINT      NOT NULL,
    min_increment     BIGINT      NOT NULL,
    current_price     BIGINT      NOT NULL, -- = starting_price until the first bid
    highest_bidder_id BIGINT      NULL,
    bid_count         INT         NOT NULL DEFAULT 0,
    start_time        DATETIME(6) NOT NULL,
    end_time          DATETIME(6) NOT NULL, -- moves forward with anti-sniping
    original_end_time DATETIME(6) NOT NULL,
    extension_count   INT         NOT NULL DEFAULT 0,
    status            VARCHAR(20) NOT NULL,
    winner_id         BIGINT      NULL,
    final_price       BIGINT      NULL,
    settlement_status VARCHAR(20) NOT NULL DEFAULT 'NONE',
    version           BIGINT      NOT NULL DEFAULT 0,
    created_at        DATETIME(6) NOT NULL,
    CONSTRAINT pk_auctions PRIMARY KEY (id),
    CONSTRAINT uq_auctions_item UNIQUE (item_id),
    CONSTRAINT fk_auctions_item FOREIGN KEY (item_id) REFERENCES items (id),
    CONSTRAINT ck_auctions_status CHECK (status IN ('SCHEDULED', 'ACTIVE', 'ENDED')),
    CONSTRAINT ck_auctions_settlement CHECK (settlement_status IN ('NONE', 'PENDING', 'DONE')),
    CONSTRAINT ck_auctions_prices CHECK (starting_price >= 1 AND min_increment >= 1 AND current_price >= starting_price),
    CONSTRAINT ck_auctions_times CHECK (end_time > start_time AND end_time >= original_end_time),
    INDEX ix_auctions_status_start (status, start_time),
    INDEX ix_auctions_status_end (status, end_time),
    INDEX ix_auctions_seller (seller_id)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;
