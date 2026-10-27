package ro.unitbv.liveauction.auction.config;

import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.EnableScheduling;

/**
 * Enables {@code @Scheduled} jobs. Disabled in the "test" profile ({@code app.scheduling.enabled=false}) so tests
 * call the lifecycle job directly with a fixed {@code Clock}.
 * <p>
 * TODO(K) S2: the lifecycle job ({@code @Scheduled(fixedDelay = 1000)}: SCHEDULED -> ACTIVE -> ENDED, settlement
 * retry) lives in the service package, see docs/team/K.md.
 */
@Configuration
@EnableScheduling
@ConditionalOnProperty(name = "app.scheduling.enabled", havingValue = "true", matchIfMissing = true)
public class SchedulingConfig {
}
