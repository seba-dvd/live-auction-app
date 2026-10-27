package ro.unitbv.liveauction.bidding;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.context.annotation.Import;
import org.testcontainers.junit.jupiter.Testcontainers;

/**
 * Starts the context against a real MySQL 8.4: runs the Flyway migrations and validates the JPA entities against them
 * ({@code ddl-auto=validate}). Skipped automatically when Docker is not available (CI always has Docker).
 */
@SpringBootTest
@Import(TestcontainersConfiguration.class)
@Testcontainers(disabledWithoutDocker = true)
class MySqlSchemaTests {

    @Test
    void migrationsMatchEntities() {
    }
}
