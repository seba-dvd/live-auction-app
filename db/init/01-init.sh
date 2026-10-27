#!/bin/bash
# Runs ONCE, on the first start of the MySQL container (empty "mysql-data" volume).
# Creates one schema + one user per service; each user only has privileges on its own schema
# (database-per-service on a single MySQL instance, see docs/decisions/ADR-004-database-per-service.md).
# To run it again: docker compose down -v (deletes ALL data!) and then docker compose up -d.
#
# Executed in a subshell so it works whether the MySQL entrypoint runs or sources it.
(
  set -e

  USER_DB_USERNAME="${USER_DB_USERNAME:-user_service}"
  AUCTION_DB_USERNAME="${AUCTION_DB_USERNAME:-auction_service}"
  BIDDING_DB_USERNAME="${BIDDING_DB_USERNAME:-bidding_service}"

  for var in MYSQL_ROOT_PASSWORD USER_DB_PASSWORD AUCTION_DB_PASSWORD BIDDING_DB_PASSWORD; do
    if [ -z "${!var}" ]; then
      echo "01-init.sh: $var is not set (copy .env.example to .env)" >&2
      exit 1
    fi
  done

  mysql --protocol=socket -uroot -p"${MYSQL_ROOT_PASSWORD}" <<EOSQL
CREATE DATABASE IF NOT EXISTS user_db    CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
CREATE DATABASE IF NOT EXISTS auction_db CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
CREATE DATABASE IF NOT EXISTS bidding_db CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

CREATE USER IF NOT EXISTS '${USER_DB_USERNAME}'@'%'    IDENTIFIED BY '${USER_DB_PASSWORD}';
CREATE USER IF NOT EXISTS '${AUCTION_DB_USERNAME}'@'%' IDENTIFIED BY '${AUCTION_DB_PASSWORD}';
CREATE USER IF NOT EXISTS '${BIDDING_DB_USERNAME}'@'%' IDENTIFIED BY '${BIDDING_DB_PASSWORD}';

GRANT ALL PRIVILEGES ON user_db.*    TO '${USER_DB_USERNAME}'@'%';
GRANT ALL PRIVILEGES ON auction_db.* TO '${AUCTION_DB_USERNAME}'@'%';
GRANT ALL PRIVILEGES ON bidding_db.* TO '${BIDDING_DB_USERNAME}'@'%';
FLUSH PRIVILEGES;
EOSQL

  echo "01-init.sh: created user_db, auction_db, bidding_db and one user per service"
)
