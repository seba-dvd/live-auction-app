package ro.unitbv.liveauction.auction;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;

/**
 * Context-load test that needs neither MySQL nor Docker: the "test" profile uses H2 in MySQL mode,
 * disables Flyway and generates the schema from the entities (see src/test/resources/application-test.yml).
 */
@SpringBootTest
@ActiveProfiles("test")
class AuctionServiceApplicationTests {

    @Test
    void contextLoads() {
    }
}
