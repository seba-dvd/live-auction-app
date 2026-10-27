package ro.unitbv.liveauction.bidding;

import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.boot.testcontainers.service.connection.ServiceConnection;
import org.springframework.context.annotation.Bean;
import org.testcontainers.mysql.MySQLContainer;
import org.testcontainers.utility.DockerImageName;

/**
 * Throw-away MySQL 8.4 (same version as Docker Compose) for integration tests; requires Docker.
 * {@code @ServiceConnection} points the DataSource at the container, so Flyway and {@code ddl-auto=validate} run
 * exactly as in production.
 */
@TestConfiguration(proxyBeanMethods = false)
class TestcontainersConfiguration {

    @Bean
    @ServiceConnection
    MySQLContainer mysqlContainer() {
        return new MySQLContainer(DockerImageName.parse("mysql:8.4"));
    }
}
